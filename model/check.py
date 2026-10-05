import tensorflow as tf
import numpy as np
from PIL import Image

MODEL = "tf_model/model_float32.tflite"
IMAGE = "test.jpg"

classes = [
    "Alternaria",
    "Anthracnose",
    "Bacterial Blight",
    "Cercospora",
    "Healthy"
]

interpreter = tf.lite.Interpreter(model_path=MODEL)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

image = Image.open(IMAGE).convert("RGB")
image = image.resize((224, 224))

image = np.array(image, dtype=np.float32) / 255.0
image = np.expand_dims(image, axis=0)

interpreter.set_tensor(input_details[0]["index"], image)
interpreter.invoke()

output = interpreter.get_tensor(output_details[0]["index"])[0]

prediction = np.argmax(output)

print("Prediction:", classes[prediction])
print("Scores:", output)