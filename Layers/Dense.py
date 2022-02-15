from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Dense(Layer):

    def __init__(self, out_dim):
        self.out_dim = out_dim

        self.weights = None
        self.biases = np.random.rand(1, out_dim)

        self.input = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs

        if self.weights is None:
            n = inputs.shape[1]
            self.weights = np.random.rand(self.out_dim, n)

        return np.dot(inputs, self.weights.T) + self.biases

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        n = self.input.shape[1]
        delta_weights = np.dot(output_gradient.T, self.input) / n
        delta_biases = np.sum(output_gradient, axis=0, keepdims=True) / n

        self.weights -= delta_weights * learning_rate
        self.biases -= delta_biases * learning_rate

        output_gradient_out = np.dot(output_gradient, self.weights)
        return output_gradient_out
