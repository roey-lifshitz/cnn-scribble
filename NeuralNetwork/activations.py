from NeuralNetwork.base import Layer
import numpy as np


class Relu(Layer):
    """ Relu Activation Function """

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input = inputs
        return np.maximum(0, inputs)

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        return output_gradient * (self.input > 0.0)


class Sigmoid(Layer):
    """ Sigmoid Activation Function """

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input = inputs
        return 1.0 / (1.0 + np.exp(-inputs))

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        return self.input * (1.0 - self.input)


class Softmax(Layer):
    """ Softmax Activation Function"""

    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        # Subtract every value by the maximum value to avoid overflow error
        e = np.exp(inputs - inputs.max(keepdims=True))
        return e / np.sum(e, axis=0)

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        return output_gradient
