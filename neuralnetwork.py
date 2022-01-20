import matplotlib.pyplot as plt
import numpy as np

from math import exp
from abc import ABC, abstractmethod


class Layer(ABC):

    @abstractmethod
    def initialize_weights(self, next_layer_length):
        pass


class Convolutional(Layer):

    def __init__(self, length):

        self.length = length
        self.neurons = np.empty(self.length)
        self.biases = np.random.rand(self.length)
        self.weights = np.array()

    def initialize_weights(self, next_layer_length):
        amount_of_weights = self.length * next_layer_length
        self.weights = np.random.rand(amount_of_weights)


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
            {"input_dim": 64, "output_dim": 2, "activation": "sigmoid"},
        ]
        self.model = {}
        self.memory = {}

        self.init_layers()


    @staticmethod
    def sigmoid(activation):
        return 1.0 / (1.0 + exp(-activation))


    def sigmoid_backward(self, dA, Z):
        sig = self.sigmoid(Z)
        return dA * sig * (1 - sig)

    @staticmethod
    def get_cost_value(predictions, wanted):
        cost = np.subtract(predictions - wanted)
        cost = np.square(cost)
        return np.sum(cost)

    @staticmethod
    def get_accuracy_value(predictions, wanted):
        success = np.sum(predictions == wanted)
        total = wanted.size
        return success / total

    def init_layers(self, seed=99):
        np.random.seed(seed)

        for index, layer in enumerate(self.model_architecture):
            layer_index = index + 1
            layer_input_size = layer["input_dim"]
            layer_output_size = layer["output_dim"]

            # Add to dictionary the weights and biases between each layer
            self.model['w' + str(layer_index)] = np.random.randn(
                layer_output_size, layer_input_size)
            self.model['b' + str(layer_index)] = np.random.randn(
                layer_output_size, 1)

    def singe_layer_forward_propagate(self, neurons, weights, biases, activation):

        # z = Weights * Inputs + Biases
        z = np.dot(weights, neurons) + biases

        return self.sigmoid(z), z

    def forward_propagate(self, inputs):

        neurons = inputs
        for index, layer in enumerate(self.model_architecture):

            layer_index = index + 1
            prev_neurons = neurons

            activation = layer['activation']
            weights = self.model['w' + str(layer_index)]
            biases = self.model['b' + str(layer_index)]

            neurons, z = self.singe_layer_forward_propagate(prev_neurons, weights, biases, activation)

            self.memory["a" + str(index)] = prev_neurons
            self.memory["z" + str(layer_index)] = z

        # returns the values of the last hidden Layer
        return inputs

    def single_layer_backward_propagation(self, a, weights, biases, neurons, a_prev):
        m = a_prev.shape[1]

        b_z = self.sigmoid_backward(a, neurons)
        b_weights = np.dot(b_z, neurons.T) / m
        b_biases = np.sum(b_z, axis=1, keepdims=True) / m
        a_prev = np.dot(weights.T, b_z)

        return a_prev, b_weights, b_biases



