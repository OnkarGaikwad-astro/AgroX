# CNN Model

This is a simple CNN model made using PyTorch for image classification.

The model takes an RGB image of size `224 x 224` and gives output for **5 classes**.

## Classes

The model classifies the following 5 classes:

```text
0 → Alternaria
1 → Anthracnose
2 → Bacterial_Blight
3 → Cercospora
4 → Healthy
```

## Model

The model architecture is:

```text
Sequential(
  (0): Conv2d(3, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (1): ReLU()
  (2): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (3): Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
  (4): ReLU()
  (5): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
  (6): Flatten(start_dim=1, end_dim=-1)
  (7): Linear(in_features=100352, out_features=100, bias=True)
  (8): ReLU()
  (9): Linear(in_features=100, out_features=32, bias=True)
  (10): ReLU()
  (11): Linear(in_features=32, out_features=5, bias=True)
)
```

## Model Parameters

The model contains approximately **10.04 million trainable parameters**.

```text
Total Parameters = 10,043,785
                 ≈ 10.04 Million
```

The majority of the parameters are in the first `Linear` layer:

```text
Linear(100352 → 100)

100352 × 100 + 100
= 10,035,300 parameters
```

## Input Shape

The model expects an input tensor of size:

```text
(1, 3, 224, 224)
```

Here:

- `1` = batch size
- `3` = RGB channels
- `224` = image height
- `224` = image width

## Architecture Flow

The input image passes through the model as follows:

```text
224 x 224
    ↓
Conv2d
    ↓
16 x 224 x 224
    ↓
MaxPool
    ↓
16 x 112 x 112
    ↓
Conv2d
    ↓
32 x 112 x 112
    ↓
MaxPool
    ↓
32 x 56 x 56
    ↓
Flatten
    ↓
32 x 56 x 56 = 100352
    ↓
Linear
    ↓
100
    ↓
Linear
    ↓
32
    ↓
Linear
    ↓
5
```

## Training

The model was trained using:

```text
Framework      → PyTorch
Optimizer      → Adam
Learning Rate  → 0.001
Loss Function  → CrossEntropyLoss
Batch Size     → 32
Epochs         → 10
Image Size     → 224 x 224
```

The training preprocessing was:

```python
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
```

## Training Loss

The training loss over 10 epochs was:

```text
Epoch 1  → 0.8160
Epoch 2  → 0.3626
Epoch 3  → 0.1925
Epoch 4  → 0.0997
Epoch 5  → 0.0413
Epoch 6  → 0.0157
Epoch 7  → 0.0033
Epoch 8  → 0.0009
Epoch 9  → 0.0005
Epoch 10 → 0.0004
```

## Performance

The model achieved:

```text
Test Accuracy  → 96.18%
Macro F1 Score  → 0.96
Weighted F1     → 0.96
```

### Classification Report

```text
                    precision    recall  f1-score   support

Alternaria             0.95      0.95      0.95       179
Anthracnose            0.96      0.96      0.96       242
Bacterial_Blight       0.94      0.96      0.95       183
Cercospora             0.96      0.91      0.93       117
Healthy                0.99      0.99      0.99       299

accuracy                                  0.96      1020
macro avg             0.96      0.95      0.96      1020
weighted avg          0.96      0.96      0.96      1020
```

## Confusion Matrix

```text
                  Predicted

                A   An   B   C   H

Actual A      [170   1   3   3   2]
       An     [  1 233   6   2   0]
       B      [  4   3 175   0   1]
       C      [  2   6   2 107   0]
       H      [  2   0   1   0 296]
```

Where:

```text
A  = Alternaria
An = Anthracnose
B  = Bacterial_Blight
C  = Cercospora
H  = Healthy
```

## How to Use the Model

To use the trained model, follow these steps.

### Step 1: Define the Model

First define the model:

```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Conv2d(
        in_channels=3,
        out_channels=16,
        kernel_size=3,
        padding=1
    ),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Conv2d(
        in_channels=16,
        out_channels=32,
        kernel_size=3,
        padding=1
    ),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Flatten(),

    nn.Linear(32 * 56 * 56, 100),
    nn.ReLU(),

    nn.Linear(100, 32),
    nn.ReLU(),

    nn.Linear(32, 5)
)
```

### Step 2: Load the Model

Load the trained weights using:

```python
model.load_state_dict(
    torch.load("agrox_model.pth")
)
```

### Step 3: Prediction

Before prediction, put the model in evaluation mode:

```python
model.eval()
```

Then use the input `x`:

```python
output = model(x)
```

The output will be a tensor containing **5 values**.

To find the class with the highest value, use:

```python
predicted_class = torch.argmax(
    output,
    dim=1
)
```

The input `x` must be of size:

```text
(1, 3, 224, 224)
```

Here:

- `1` = batch size
- `3` = RGB channels
- `224` = image height
- `224` = image width

### Complete Prediction

```python
model.eval()

with torch.no_grad():
    output = model(x)

predicted_class = torch.argmax(
    output,
    dim=1
)

print(predicted_class)
```

## Image Preprocessing

The image must be preprocessed in the same way as the images used during training.

The model was trained using:

```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
```

When using OpenCV, the image should be processed as follows:

```python
import cv2

img = cv2.imread("image.jpg")

# OpenCV loads images as BGR
img = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2RGB
)

# Resize image
img = cv2.resize(
    img,
    (224, 224)
)

# Convert to float32 tensor
img = torch.tensor(
    img,
    dtype=torch.float32
)

# Convert pixel values from [0, 255] to [0, 1]
img = img / 255.0

# Convert H x W x C to C x H x W
img = img.permute(
    2, 0, 1
)

# Add batch dimension
img = img.unsqueeze(0)
```

The final input shape will be:

```text
(1, 3, 224, 224)
```

## Complete Prediction Code

```python
import cv2
import torch
import torch.nn as nn


# Define model
model = nn.Sequential(
    nn.Conv2d(
        in_channels=3,
        out_channels=16,
        kernel_size=3,
        padding=1
    ),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Conv2d(
        in_channels=16,
        out_channels=32,
        kernel_size=3,
        padding=1
    ),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Flatten(),

    nn.Linear(32 * 56 * 56, 100),
    nn.ReLU(),

    nn.Linear(100, 32),
    nn.ReLU(),

    nn.Linear(32, 5)
)


# Load trained weights
model.load_state_dict(
    torch.load("model.pth")
)

model.eval()


# Class names
classes = [
    "Alternaria",
    "Anthracnose",
    "Bacterial_Blight",
    "Cercospora",
    "Healthy"
]


# Load image
img = cv2.imread("image.jpg")


# Convert BGR to RGB
img = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2RGB
)


# Resize image
img = cv2.resize(
    img,
    (224, 224)
)


# Convert image to tensor
img = torch.tensor(
    img,
    dtype=torch.float32
)


# Normalize pixel values
img = img / 255.0


# Convert HWC to CHW
img = img.permute(
    2,
    0,
    1
)


# Add batch dimension
img = img.unsqueeze(0)


# Prediction
with torch.no_grad():

    output = model(img)

    predicted_class = torch.argmax(
        output,
        dim=1
    )


# Get class index
class_index = predicted_class.item()


# Print prediction
print("Class index:", class_index)

print(
    "Prediction:",
    classes[class_index]
)
```

## Model Output

The final layer of the model is:

```python
nn.Linear(32, 5)
```

Therefore, the model produces 5 output values:

```text
[logit_0, logit_1, logit_2, logit_3, logit_4]
```

Each output corresponds to one of the five classes:

```text
0 → Alternaria
1 → Anthracnose
2 → Bacterial_Blight
3 → Cercospora
4 → Healthy
```

The predicted class is the class with the highest logit:

```python
predicted_class = torch.argmax(
    output,
    dim=1
)
```

A softmax layer is not required when only the predicted class is needed.

## Resolution Comparison

An earlier version of the model used an input resolution of `128 x 128`.

The results were:

```text
128 x 128 → 92.65% Test Accuracy

224 x 224 → 96.18% Test Accuracy
```

The increase in image resolution improved the test accuracy by approximately:

```text
96.18% - 92.65%
= 3.53 percentage points
```

## Model Status

This model was built **completely from scratch using PyTorch**.

It does not use:

- Transfer learning
- Pretrained models
- Pretrained CNN backbones
- External pretrained weights

The current model achieved a **96.18% test accuracy** on the current test split.

The model is ready for the next stage of the AgroX project, including:

- Testing on completely unseen images
- Real-world validation
- Model deployment
- Integration with the AgroX application