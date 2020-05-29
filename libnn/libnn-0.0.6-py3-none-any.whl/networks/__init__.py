from .resnets import *
from .lstms import *

neuralnets = {
    "ResNet18": ResNet18, 
    "ResNet34": ResNet34, 
    "ResNet50": ResNet50, 
    "ResNet101": ResNet101, 
    "ResNet152": ResNet152, 
    "lstm": LSTM
}

__all__ = ["neuralnets"]
