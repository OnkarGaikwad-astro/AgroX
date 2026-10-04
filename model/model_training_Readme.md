# CNN Model Training

This folder contains the code used to train the CNN model for the **Pomegranate Diseases Dataset**.

The model is trained to classify pomegranate images into 5 classes:

- Alternaria
- Anthracnose
- Bacterial Blight
- Cercospora
- Healthy

## Dataset

The dataset is stored in:

```text
dataset/pomegranate_diseases_dataset
```

The dataset used for training can be downloaded from the following link:

[Download Dataset](https://example.com/pomegranate-diseases-dataset)

After downloading the dataset, extract it and place it inside the `dataset` folder.

The folder structure is:

```text
dataset/
└── pomegranate_diseases_dataset/
    ├── Alternaria/
    ├── Anthracnose/
    ├── Bacterial_Blight/
    ├── Cercospora/
    └── Healthy/
```

The dataset is loaded using `ImageFolder`.

## Libraries Used

The model is trained using PyTorch.

```python
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from torch.utils.data import random_split
from torch.utils.data import DataLoader

from torchvision import datasets, transforms
```

## Image Preprocessing

All images are resized to `224 x 224` and converted into tensors.

```python
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
```

The dataset is loaded using:

```python
dataset = datasets.ImageFolder(
    root=dataset_path,
    transform=transform
)
```

## Train and Test Split

The dataset is divided into:

- **80% training data**
- **20% testing data**

```python
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(
    dataset,
    [train_size, test_size]
)
```

## DataLoader

The batch size used is `32`.

```python
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)
```

The training data is shuffled and the test data is not shuffled.

## Model

The CNN model used for training is:

```python
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

    nn.Linear(32*56*56, 100),
    nn.ReLU(),

    nn.Linear(100, 32),
    nn.ReLU(),

    nn.Linear(32, 5)
)
```

The model has approximately **10.04 million parameters**.

```text
Total Parameters = 10,043,785
                 ≈ 10.04 Million
```

## Loss Function and Optimizer

I used Cross Entropy Loss and Adam optimizer.

```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

criterion = nn.CrossEntropyLoss()
```

The learning rate is:

```text
0.001
```

## Training

The model is trained for **10 epochs**.

The training function is:

```python
def train(x, y):

    output = model(x)

    loss = criterion(output, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()
```

Training is done using:

```python
epoch = 10

for k in range(epoch):

    batches = 0
    imgs = 0
    total_loss = 0

    for images, labels in train_loader:

        x = images
        y = labels

        total_loss = total_loss + train(x, y)

        batches = batches + 1
        imgs = imgs + images.size(0)

        print("\rImages:", imgs, end="")

    print(
        f"\nEpoch : {k+1} || Loss : {total_loss / batches}"
    )
```

The training loss after each epoch was:

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

## Testing the Model

For testing a single image:

```python
image, label = test_dataset[112]

model.eval()

with torch.no_grad():

    output = model(
        image.unsqueeze(0)
    )

    prediction = torch.argmax(
        output,
        dim=1
    )

print(
    "Actual:",
    test_dataset.dataset.classes[label]
)

print(
    "Predicted:",
    test_dataset.dataset.classes[prediction.item()]
)
```

## Test Accuracy

The test accuracy is calculated using:

```python
model.eval()

correct = 0
total = 0

with torch.no_grad():

    for images, labels in test_loader:

        output = model(images)

        predictions = torch.argmax(
            output,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

accuracy = correct / total * 100

print(f"Test Accuracy: {accuracy:.2f} %")
```

The model achieved:

```text
Test Accuracy: 96.18%
```

## Classification Report

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

## Saving the Model

The trained model is saved using:

```python
torch.save(
    model.state_dict(),
    "agrox_model.pth"
)
```

The saved file is:

```text
agrox_model.pth
```

This file can be loaded later using the same model architecture.

## Model Information

```text
Dataset        : Pomegranate Diseases Dataset
Classes        : 5
Image Size     : 224 x 224
Batch Size     : 32
Train Split    : 80%
Test Split     : 20%
Epochs         : 10
Optimizer      : Adam
Learning Rate  : 0.001
Loss Function  : CrossEntropyLoss
Framework      : PyTorch
Parameters     : 10.04 Million
Test Accuracy  : 96.18%
Model File     : agrox_model.pth
```

## Resolution Comparison

I first trained the model using `128 x 128` images.

```text
128 x 128 → 92.65% Test Accuracy
```

Then I changed the image size to `224 x 224`.

```text
224 x 224 → 96.18% Test Accuracy
```

So the accuracy improved by:

```text
96.18% - 92.65%
= 3.53%
```

The model performed better with the higher image resolution.

## Files

The project structure is:

```text
.
├── dataset/
│   └── pomegranate_diseases_dataset/
│       ├── Alternaria/
│       ├── Anthracnose/
│       ├── Bacterial_Blight/
│       ├── Cercospora/
│       └── Healthy/
│
├── train.py
├── agrox_model.pth
└── README.md
```

## Note

The same model architecture and image preprocessing should be used when loading `agrox_model.pth`.

The model expects an input tensor of:

```text
(1, 3, 224, 224)
```

Here:

- `1` = batch size
- `3` = RGB channels
- `224` = image height
- `224` = image width

The model was built from scratch using PyTorch and does not use a pretrained model or transfer learning.