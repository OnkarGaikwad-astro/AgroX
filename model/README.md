model = Sequential(
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

and to use that model do these following steps:

step 1:-
define model first as 

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
    nn.Linear(32*32*32,100),
    nn.ReLU(),
    nn.Linear(100,32),
    nn.ReLU(),
    nn.Linear(32,5)
)

step 2:-

model.load_state_dict(
    torch.load("model.pth")
)

step 3:-
for prediction use -

output = model.eval(x)

output will be an tensor of 5 elements and to find the correct class use torch.argmax
and x must be of size (1,3,128,128)