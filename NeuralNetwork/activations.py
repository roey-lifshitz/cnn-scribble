from NeuralNetwork.base import Layer
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
        e = np.exp(inputs)
        return e / np.sum(e, axis=0)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient
