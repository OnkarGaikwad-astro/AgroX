# CNN Model

This is a simple CNN model made using PyTorch for image classification.

The model takes an RGB image of size `128 x 128` and gives output for **5 classes**.

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
  (7): Linear(in_features=32768, out_features=100, bias=True)
  (8): ReLU()
  (9): Linear(in_features=100, out_features=32, bias=True)
  (10): ReLU()
  (11): Linear(in_features=32, out_features=5, bias=True)
)
```

## How to use the model

To use the trained model, follow these steps.

### Step 1: Define the model

First define the model:

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

### Step 2: Load the model

Load the trained weights using:

```python
model.load_state_dict(
    torch.load("model.pth")
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
predicted_class = torch.argmax(output, dim=1)
```

The input `x` must be of size:

```text
(1, 3, 128, 128)
```

Here:

- `1` = batch size
- `3` = RGB channels
- `128` = image height
- `128` = image width

### Complete prediction

```python
model.eval()

with torch.no_grad():
    output = model(x)

predicted_class = torch.argmax(output, dim=1)

print(predicted_class)
```

## Note

The `Linear` layer has `32*32*32` input features because the model expects an input image of size `128 x 128`.

```text
128 x 128
    ↓
MaxPool
    ↓
64 x 64
    ↓
MaxPool
    ↓
32 x 32
    ↓
32 channels
    ↓
32 x 32 x 32 = 32768
```