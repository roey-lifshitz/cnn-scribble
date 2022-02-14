from typing import Tuple
from Layers.Layer import Layer
import numpy as np


class Relu(Layer):

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs
        return np.maximum(0, inputs)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * (self.input > 0.0)


class Softmax(Layer):

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs
        tmp = np.exp(1.0 / (1.0 + np.exp(-inputs)))
        return tmp / np.expand_dims(np.sum(tmp, axis=1), 1)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient / (1.0 + np.exp(-self.input)) * (1.0 - (1.0 / (1.0 + np.exp(-self.inputs))))
    