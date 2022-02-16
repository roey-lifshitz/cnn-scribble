from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Dense(Layer):

    def __init__(self, dim_in, dim_out):

        self.dim_in = dim_in
        self.dim_out = dim_out

        self.weights = np.random.rand(dim_out, dim_in) * 0.1
        self.biases = np.random.rand(dim_out, 1) * 0.1

        self.input = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:

        self.input = inputs
        return np.dot(self.weights, inputs) + self.biases

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:

        n = self.input.shape[0]

        delta_weights = np.dot(output_gradient, self.input.T) / n
        delta_biases = np.sum(output_gradient, axis=1, keepdims=True) / n

        self.weights -= delta_weights * learning_rate
        self.biases -= delta_biases * learning_rate

        output_gradient_out = np.dot(self.weights.T, output_gradient)

        return output_gradient_out
