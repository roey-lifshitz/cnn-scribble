import matplotlib.pyplot as plt
import numpy as np


from math import exp
from abc import ABC, abstractmethod


class Layer(ABC):

    @abstractmethod
    def initialize_weights(self, dim_in, dim_out):
        pass

    @abstractmethod
    def forward_propagate(self):
        pass

    @abstractmethod
    def backwards_propagate(self):
        pass

    @abstractmethod
    def update(self):
        pass

class Convolutional(Layer):

    def __init__(self, dim_in, dim_out, activation):
        self.activations = activation
        self.weights = np.rand.random(dim_out, dim_in) * 0.1
        self.biases = np.rand.random(dim_out, 1) * 0.1

    def forward_propagate(self, inputs):
        self.node = np.dot(self.weights, inputs) + self.biases
        self.neuron = self.activation[0](self.node)

        return self.neuron

    def backwards_propagate(self, error, prev_node):
        pass


class MaxPooling(Layer):

    def __init__(self, length):
        self.length = length
        self.neurons = np.empty(self.length)
        self.biases = np.random.rand(self.length)
        self.weights = np.array()

    def initialize_weights(self, next_layer_length):
        amount_of_weights = self.length * next_layer_length
        self.weights = np.random.ones(amount_of_weights)


class Flatten(Layer):

    def __init__(self, length):
        self.length = length
        self.neurons = np.empty(self.length)
        self.biases = np.random.rand(self.length)
        self.weights = np.array()

    def initialize_weights(self, next_layer_length):
        amount_of_weights = self.length * next_layer_length
        self.weights = np.random.ones(amount_of_weights)


class Dense(Layer):

    def __init__(self):
        pass


class NeuralNetwork:

    def __init__(self, ):

        """
        The Neural Network will consist of the following Layers
        1. Convolutional Layer
        2. Max Pooling Layer
        3  Convolutional Layer
        4. Max Pooling Layer
        5. Flatter Layer
        6. Softmax Activation Layer
        """

        self.model_architecture = [
            {"input_dim": 256 * 256, "output_dim": 256, "activation": "sigmoid"},
            {"input_dim": 256, "output_dim": 128, "activation": "sigmoid"},
            {"input_dim": 128, "output_dim": 64, "activation": "sigmoid"},
            {"input_dim": 64, "output_dim": 3, "activation": "sigmoid"},
        ]
        self.model = {}

        self.init_layers()