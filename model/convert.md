# AgroX Model Converter

A lightweight converter that transforms the trained AgroX PyTorch model (`.pth`) into a Float32 TensorFlow Lite (`.tflite`) model for mobile deployment.

## Conversion Pipeline

```text
agrox_model.pth
       │
       ▼
    PyTorch
       │
       ▼
 Temporary ONNX
       │
       ▼
    onnx2tf
       │
       ▼
agrox_model.tflite
```

The ONNX model is created only in a temporary directory during conversion and is automatically deleted when the process finishes.

## Project Structure

```text
model/
├── models/
│   ├── agrox_model.pth
│   └── agrox_model.tflite
├── convert.py
└── README.md
```

## Requirements

Install the required Python packages:

```bash
pip install torch onnx onnx2tf
```

## Usage

Run the converter from the project root:

```bash
python model/convert.py
```

The script will:

1. Load the trained PyTorch model.
2. Create a temporary ONNX representation.
3. Convert the ONNX model to TensorFlow Lite.
4. Extract the Float32 TFLite model.
5. Save the final model to `model/models/agrox_model.tflite`.
6. Delete all temporary conversion files.

## Model Architecture

The converter recreates the same CNN architecture used to train the AgroX model:

```text
Input: 3 × 224 × 224

Conv2D: 3 → 16
ReLU
MaxPool2D

Conv2D: 16 → 32
ReLU
MaxPool2D

Flatten

Linear: 32 × 56 × 56 → 100
ReLU

Linear: 100 → 32
ReLU

Linear: 32 → 5
```

## Model Input

```text
Shape: [1, 224, 224, 3]
Type:  Float32
```

Images should be resized to `224 × 224` and provided as RGB images.

## Model Output

```text
Shape: [1, 5]
Type:  Float32
```

The five output classes are:

| Index | Class |
|------:|-------|
| 0 | Alternaria |
| 1 | Anthracnose |
| 2 | Bacterial Blight |
| 3 | Cercospora |
| 4 | Healthy |

## Output

After successful conversion, the final model is available at:

```text
model/models/agrox_model.tflite
```

The generated TFLite model can be used for on-device inference in the AgroX Flutter/Android application.

## Temporary Files

The converter temporarily creates an ONNX model and other conversion artifacts. These files are stored outside the project and removed automatically after conversion.

No permanent `model.onnx`, `tf_model`, `schema.fbs`, or other conversion files are required.

## Example

A successful conversion produces output similar to:

```text
✅ PyTorch model loaded
✅ PyTorch → ONNX
✅ ONNX → TFLite

================================
✅ TFLite model created!
📦 model/models/agrox_model.tflite
================================

🧹 Temporary files deleted
```

## Notes

- The model architecture in `convert.py` must match the architecture used to train `agrox_model.pth`.
- The input size is `224 × 224`.
- The model uses Float32 precision.
- The ONNX model is only an intermediate format.
- Only the final `.tflite` model needs to be included in the application.

## Result

```text
PyTorch (.pth)
      ↓
Temporary ONNX
      ↓
TFLite Float32
      ↓
Flutter / Android
```
