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
            {"input_dim": 64, "output_dim": 3, "activation": "sigmoid"},
        ]
        self.model = {}

        self.init_layers()



    @staticmethod
    def sigmoid(inputs):
        return 1.0 / (1.0 + exp(-inputs))

    @staticmethod
    def sigmoid_derivative(inputs):
        """
        Given an array of neuron values, we need to calculate each neuron's slope.
        We are doing so by calculating the derivative of sigmoid (to find slop) and plotting the neuron value:

        :param inputs: numpy.array of neurons
        :return: numpy.array of slopes
        """
        return inputs * (1.0 - inputs)

    @staticmethod
    def get_cost_value(predictions, wanted):
        cost = predictions- wanted
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
                layer_output_size, layer_input_size) * 0.1
            self.model['b' + str(layer_index)] = np.random.randn(
                layer_output_size) * 0.1
            #print("Weights: ", self.model['w' + str(layer_index)].shape, "Biases: ", self.model['b' + str(layer_index)].shape)

    def singe_layer_forward_propagate(self, neurons, weights, biases, activation):

        # z = Weights * Inputs + Biases
        z = np.dot(weights, neurons) + biases
        sigmoid = np.vectorize(self.sigmoid)
        return sigmoid(z), z

    def forward_propagate(self, inputs):

        memory = {}

        # neurons of input layer
        neurons = inputs

        # Loop through all layers
        for index, layer in enumerate(self.model_architecture):
            layer_index = index + 1

            # Get information regarding current layer
            activation = layer['activation']
            weights = self.model['w' + str(layer_index)]
            biases = self.model['b' + str(layer_index)]

            # update neurons to neurons in next layer
            neurons, z = self.singe_layer_forward_propagate(neurons, weights, biases, activation)

            # save neuron value before activation function for back propagation
            memory['a' + str(layer_index)] = neurons
            memory['z' + str(layer_index)] = z

        # returns output layer neurons
        return neurons, memory

    def single_layer_backward_propagate(self, prev_neurons, errors, weights):

        # Error of neuron = sum(error of neurons in nextlayer * weight that connects neuron in next layer and current layer) * sigmoid derivative(current neuron)

        sigmoid_derivative = np.vectorize(self.sigmoid_derivative)

        # returns error of neurons in previous layer
        return np.dot(weights.T, errors) * sigmoid_derivative(prev_neurons)


    def backwards_propagate(self, outputs, labels, memory):

        error = {}

        # Error of neurons in input layer

        e = outputs - labels * self.sigmoid_derivative(outputs)
        #e = 0.5 * np.power(outputs - labels, 2) Mean Squared error

        # Calculate the error of the output layer
        error['l' + str(len(self.model_architecture))] = e

        # Loop without last layer
        for index, layer in reversed(list(enumerate(self.model_architecture[:-1]))):
            layer_index = index + 1

            # Get information regarding current layer
            activation = layer['activation']
            weights = self.model['w' + str(layer_index + 1)]
            prev_neurons = memory['z' + str(layer_index)]

            # Calculate the error of prev_neurons
            e = self.single_layer_backward_propagate(prev_neurons, e, weights)
            error['l' + str(layer_index)] = np.outer(e, prev_neurons)

        return error

    def update(self, error, learning_rate):

        for index, layer in enumerate(self.model_architecture):
            layer_index = index + 1

            print(self.model['w' + str(layer_index)].shape, error['l' + str(layer_index)].shape)
            # weight = weight - learning_rate * error * input
            self.model['w' + str(layer_index)] -= learning_rate * error['l' + str(layer_index)]

    def update(self, error, learning_rate):
        for index, layer in enumerate(self.model_architecture):
            layer = index + 1
            #self.model["w" + str(layer)] -= learning_rate * error["w" + str(layer)]
            #self.model["b" + str(layer)] -= learning_rate * error["b" + str(layer)]

    def train(self, inputs, labels, epochs=24, learning_rate= 0.01):
        cost_history = []
        accuracy_history = []

        for i in range(epochs):
            output, memory = self.forward_propagate(inputs[i].ravel())
            cost = self.get_cost_value(output, labels[i])
            cost_history.append(cost)
            accuracy = self.get_accuracy_value(output, labels[i])
            accuracy_history.append(accuracy)

            error = self.backwards_propagate(output, labels[i], memory)
            params_values = self.update(error, learning_rate)


        print("COST: ", cost_history)
        print("Accuracy: ", accuracy_history)
        print("Labels", labels)

