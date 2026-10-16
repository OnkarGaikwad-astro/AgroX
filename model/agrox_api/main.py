import io
import numpy as np
import tensorflow as tf
from PIL import Image
from fastapi import FastAPI, File, HTTPException, UploadFile


app = FastAPI(title="AgroX Disease Detection API")
MODEL = "agrox_model.tflite"

classes = [
    "Alternaria",
    "Anthracnose",
    "Bacterial Blight",
    "Cercospora",
    "Healthy"
]
# Load the model once when the API starts
interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


@app.get("/")
def home():
    return {
        "message": "AgroX Disease Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "agrox_model.tflite"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check the uploaded file type
    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, PNG or WEBP image"
        )

    try:
        # Read the uploaded image
        contents = await file.read()

        image = Image.open(
            io.BytesIO(contents)
        ).convert("RGB")

        # Preprocess the image
        image = image.resize((224, 224))

        image = np.array(
            image,
            dtype=np.float32
        ) / 255.0

        image = np.expand_dims(image, axis=0)

        # Run inference
        interpreter.set_tensor(
            input_details[0]["index"],
            image
        )

        interpreter.invoke()

        output = interpreter.get_tensor(
            output_details[0]["index"]
        )[0]

        output = tf.nn.softmax(output).numpy()

        # Get prediction and confidence
        prediction = int(np.argmax(output))
        confidence = float(np.max(output)) * 100

        return {
            "predicted_class": classes[prediction],
            "confidence": round(confidence, 2),
            "scores": {
                classes[i]: round(float(output[i]), 4)
                for i in range(len(classes))
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process image: {str(e)}"
        )