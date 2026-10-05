import torch
import torch.nn as nn

model =nn.Sequential(
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
model.load_state_dict(torch.load("model/agrox_model.pth", map_location="cpu"))
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)

torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    opset_version=17
)