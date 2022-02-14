from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Flatten(Layer):

    def __init__(self):
        self.input_shape = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input_shape = inputs.shape
        n = inputs.shape[0]
        return np.ravel(inputs).reshape(n, -1)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient.reshape(self.input_shape)