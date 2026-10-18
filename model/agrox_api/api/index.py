import io
from pathlib import Path
import numpy as np
from ai_edge_litert.interpreter import Interpreter
from PIL import Image, UnidentifiedImageError
from fastapi import FastAPI, File, HTTPException, UploadFile


app = FastAPI(title="AgroX Disease Detection API")


# Model path
MODEL = str(
    Path(__file__).resolve().parent.parent
    / "agrox_model.tflite"
)


# Class names in training index order
classes = [
    "Alternaria",
    "Anthracnose",
    "Bacterial Blight",
    "Cercospora",
    "Healthy"
]


# Load the model once when the application starts
interpreter = Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Verify model input metadata
expected_shape = tuple(input_details[0]["shape"])
input_dtype = input_details[0]["dtype"]

if expected_shape != (1, 224, 224, 3):
    raise RuntimeError(
        f"Unexpected model input shape: {expected_shape}"
    )

if input_dtype != np.float32:
    raise RuntimeError(
        f"Expected float32 input, got {input_dtype}"
    )


@app.get("/")
def home():
    return {
        "message": "AgroX Disease Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "agrox_model.tflite",
        "input_shape": list(expected_shape),
        "output_shape": output_details[0]["shape"].tolist(),
        "classes": classes
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Validate declared file type
    if file.content_type not in {
        "image/jpeg",
        "image/png",
        "image/webp"
    }:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, PNG or WEBP image"
        )

    try:
        # Read uploaded image
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        # Decode image and convert to RGB
        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        # Resize to the model's expected dimensions
        image = image.resize((224, 224))

        # Convert pixels to float32 and normalize to [0, 1]
        image = np.asarray(
            image,
            dtype=np.float32
        ) / 255.0

        # Add batch dimension: (1, 224, 224, 3)
        image = np.expand_dims(image, axis=0)

        # Set model input
        interpreter.set_tensor(
            input_details[0]["index"],
            image
        )

        # Run inference
        interpreter.invoke()

        # Get model output for this image
        output = interpreter.get_tensor(
            output_details[0]["index"]
        )[0].astype(np.float32)

        if output.size != len(classes):
            raise HTTPException(
                status_code=500,
                detail="Model output does not match the class list"
            )

        # Convert raw logits to probabilities.
        # Only use this softmax if the model outputs logits.
        shifted_output = output - np.max(output)
        exp_output = np.exp(shifted_output)
        probabilities = exp_output / np.sum(exp_output)

        # Get predicted class and confidence
        prediction = int(np.argmax(probabilities))
        confidence = float(probabilities[prediction]) * 100

        # Return JSON response
        return {
            "predicted_class": classes[prediction],
            "confidence": round(confidence, 2),
            "scores": {
                classes[i]: round(float(probabilities[i]), 4)
                for i in range(len(classes))
            }
        }

    except HTTPException:
        raise

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image"
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the image"
        )

    finally:
        await file.close()
