from NeuralNetwork.base import Layer
import numpy as np


class Relu(Layer):

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input = inputs
        return np.maximum(0, inputs)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient * (self.input > 0.0)

    def get_params(self):
        return None

    def set_params(self, filters, biases):
        return None

class Sigmoid(Layer):

    def __init__(self):
        self.input = None
        self.output = None


    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input = inputs
        return 1.0 / (1.0 + np.exp(-inputs))

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return self.input * (1.0 - self.input)

    def get_params(self):
        return None

    def set_params(self, filters, biases):
        return None


class Softmax(Layer):

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        # Subtract every value by the maximum value to avoid overflow error
        e = np.exp(inputs - inputs.max(keepdims=True))
        return e / np.sum(e, axis=0)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        return output_gradient

    def get_params(self):
        return None

    def set_params(self, filters, biases):
        return None
