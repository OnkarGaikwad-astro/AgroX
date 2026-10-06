# ============  Convert model.pth  to  model.tflite  ============= #

import os
import shutil
import tempfile
import subprocess
import sys
import torch
import torch.nn as nn

# =========================
# 1. Define the model
# =========================

model = nn.Sequential(
    nn.Conv2d(3, 16, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Conv2d(16, 32, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2),

    nn.Flatten(),

    nn.Linear(32 * 56 * 56, 100),
    nn.ReLU(),

    nn.Linear(100, 32),
    nn.ReLU(),

    nn.Linear(32, 5)
)


# =========================
# 2. Load .pth
# =========================

model.load_state_dict(
    torch.load(
        "model/models/agrox_model.pth",
        map_location="cpu"
    )
)
model.eval()
print("✅ PyTorch model loaded")


# =========================
# 3. Temporary directory
# =========================

temp_dir = tempfile.mkdtemp()
onnx_path = os.path.join(
    temp_dir,
    "model.onnx"
)
tflite_dir = os.path.join(
    temp_dir,
    "tflite"
)
os.makedirs(tflite_dir, exist_ok=True)

try:
    # =========================
    # 4. PyTorch → ONNX
    # =========================

    dummy_input = torch.randn(
        1, 3, 224, 224
    )
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        input_names=["input"],
        output_names=["output"],
        opset_version=17
    )
    print("✅ PyTorch → ONNX")

    # =========================
    # 5. ONNX → TFLite
    # =========================

    subprocess.run(
        [
            sys.executable,
            "-m",
            "onnx2tf",
            "-i",
            onnx_path,
            "-o",
            tflite_dir
        ],
        check=True
    )

    print("✅ ONNX → TFLite")

    # =========================
    # 6. Find Float32 model
    # =========================

    tflite_file = None
    for root, dirs, files in os.walk(tflite_dir):

        for file in files:

            if (
                file.endswith(".tflite")
                and "float32" in file.lower()
            ):
                tflite_file = os.path.join(
                    root,
                    file
                )
                break

        if tflite_file:
            break

    # ========================
    # 7. Save final model
    # =========================

    if tflite_file:
        output_path = "model/models/agrox_model.tflite"
        shutil.copy2(
            tflite_file,
            output_path
        )
        print()
        print("================================")
        print("✅ TFLite model created!")
        print(f"📦 {output_path}")
        print("================================")

    else:
        print("❌ Float32 TFLite model not found")


finally:
    # =========================
    # 8. Delete temporary files
    # =========================

    shutil.rmtree(
        temp_dir,
        ignore_errors=True
    )

    print("🧹 Temporary files deleted")