import io
from pathlib import Path
import numpy as np
import tensorflow as tf
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
interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Verify the expected input shape
expected_shape = tuple(input_details[0]["shape"])

if expected_shape != (1, 224, 224, 3):
    raise RuntimeError(
        f"Unexpected model input shape: {expected_shape}"
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
        "input_shape": input_details[0]["shape"].tolist(),
        "output_shape": output_details[0]["shape"].tolist(),
        "classes": classes
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Validate the declared file type
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
        # Read the uploaded image
        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty"
            )

        # Decode and convert the image to RGB
        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        # Preprocess the image
        image = image.resize((224, 224))

        image = np.asarray(
            image,
            dtype=np.float32
        ) / 255.0

        image = np.expand_dims(image, axis=0)

        # Check the model's expected input dtype
        input_dtype = input_details[0]["dtype"]

        if input_dtype != np.float32:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Model input is not float32. "
                    "Update preprocessing for this model."
                )
            )

        # Run inference
        interpreter.set_tensor(
            input_details[0]["index"],
            image
        )

        interpreter.invoke()

        output = interpreter.get_tensor(
            output_details[0]["index"]
        )[0]

        # Convert raw logits to probabilities.
        # This assumes the TFLite model outputs logits.
        probabilities = tf.nn.softmax(output).numpy()

        # Find the highest-scoring class
        prediction = int(np.argmax(probabilities))
        confidence = float(probabilities[prediction]) * 100

        # Return JSON
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
