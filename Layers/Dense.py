from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Dense(Layer):

    def __init__(self, input_dim, out_dim):

        self.weights = np.random.randn(input_dim, out_dim) * 0.1
        self.biases = np.random.rand(out_dim, 1)

        self.input = None
        self.output = None


    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs
        return np.dot(self.input, self.weights.T) + self.biases

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        n = self.input.shape[0]

        output_gradient_out = np.dot(output_gradient, self.w)
        delta_weights = np.dot(output_gradient.T, self.input) / n
        delta_biases = np.sum(output_gradient, axis= 0, keepdims=True) / n

        return output_gradient_out
