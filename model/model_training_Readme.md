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

The expected folder structure is:

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

All images are resized to `128 x 128` and converted into PyTorch tensors.

```python
transform = transforms.Compose([
    transforms.Resize((128, 128)),
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

The training and testing data are loaded in batches of `32`.

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

The training data is shuffled, while the test data is not shuffled.

## Model

The CNN used for training is:

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

    nn.Linear(32*32*32, 100),
    nn.ReLU(),

    nn.Linear(100, 32),
    nn.ReLU(),

    nn.Linear(32, 5)
)
```

## Loss Function and Optimizer

I used **Cross Entropy Loss** for the classification problem and **Adam** as the optimizer.

```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

criterion = nn.CrossEntropyLoss()
```

The learning rate used is:

```text
0.001
```

## Training

The model is trained for **5 epochs**.

For each batch:

1. The images are passed through the model.
2. The loss is calculated.
3. Gradients are calculated using backpropagation.
4. The optimizer updates the model parameters.

The training function used is:

```python
def train(x, y):
    output = model(x)
    loss = criterion(output, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()
```

Training is performed using:

```python
epoch = 5

for k in range(epoch):
    batches = 0
    imgs = 0
    total_loss = 0

    for images, labels in train_loader:
        x = images
        y = labels

        total_loss = total_loss + train(x, y)

        batches = batches + 1
        imgs = imgs + 32

        print("\rImages:", imgs, end="")

    print(
        f"\nEpoch : {k+1} || Loss : {total_loss/(batches)}"
    )
```

The loss printed after every epoch is the average training loss for that epoch.

## Testing the Model

After training, the model is tested using the test dataset.

For a single image:

```python
image, label = test_dataset[112]

model.eval()

with torch.no_grad():
    output = model(image.unsqueeze(0))
    prediction = torch.argmax(output, dim=1)

print("Actual:", test_dataset.dataset.classes[label])
print("Predicted:", test_dataset.dataset.classes[prediction.item()])
```

This prints the actual class and the class predicted by the model.

## Test Accuracy

The accuracy is calculated by comparing the predicted labels with the actual labels.

```python
model.eval()

correct = 0
total = 0

with torch.no_grad():
    for images, labels in test_loader:

        output = model(images)

        predictions = torch.argmax(output, dim=1)

        correct += (predictions == labels).sum().item()
        total += labels.size(0)

accuracy = correct / total * 100

print(f"Test Accuracy: {accuracy:.2f} %")
```

The accuracy is calculated using:

```text
Accuracy = Correct Predictions / Total Predictions × 100
```

## Saving the Model

After training, the model weights are saved as:

```python
torch.save(
    model.state_dict(),
    "model.pth"
)
```

The saved file is:

```text
model.pth
```

This file can later be loaded into the same model architecture and used for prediction without training the model again.

## Model Information

```text
Dataset       : Pomegranate Diseases Dataset
Classes       : 5
Image Size    : 128 x 128
Batch Size    : 32
Train Split   : 80%
Test Split    : 20%
Epochs        : 5
Optimizer     : Adam
Learning Rate : 0.001
Loss Function : CrossEntropyLoss
Framework     : PyTorch
Model File    : model.pth
```

## Files

A simple project structure can be:

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
├── model.pth
└── README.md
```

## Note

The same image preprocessing and model architecture should be used when loading `model.pth` for prediction.

The trained model expects an input tensor with the shape:

```text
(1, 3, 128, 128)
```