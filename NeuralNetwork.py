import matplotlib.pyplot as plt
import numpy as np


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
        return 1.0 / (1.0 + np.exp(-inputs))

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
        cost = predictions - wanted
        cost = np.square(cost)
        return np.sum(cost)

    @staticmethod
    def get_accuracy_value(predictions, wanted):
        p_cpy = np.copy(predictions)
        p_cpy[p_cpy > 0.5] = 1
        p_cpy[p_cpy <= 0.5] = 0
        return (p_cpy == wanted).all(axis=0).mean()

    def init_layers(self, seed=99):
        np.random.seed(seed)

        # Loop through all Layers
        for i, layer in enumerate(self.model_architecture):
            # Number the layers from 1
            idx = str(i + 1)

            # Getting the dimensions of each layer
            layer_input_dim = layer['input_dim']
            layer_output_dim = layer['output_dim']

            # Initializing Weights Matrix and Biases Vector for layer
            self.model['w' + idx] = np.random.randn(
                layer_output_dim, layer_input_dim) * 0.1
            self.model['b' + idx] = np.random.randn(
                layer_output_dim, 1) * 0.1

    def singe_layer_forward_propagate(self, prev_neurons, weights, biases, activation):
        """
        Given the neurons of a previous layer, compute the neurons of the current layer
        :param prev_neurons: vector of previous layer neurons
        :param weights: matrix of weights connecting between previous layer to this layer
        :param biases: vector of biases for this layer
        :param activation: activation for this layer
        :return: vector of neurons for this layer, neurons before activation
        """
        # z = Weights * Inputs + Biases
        z = np.dot(weights, prev_neurons) + biases
        return self.sigmoid(z), z

    def forward_propagate(self, inputs):
        """
        Forward propagate the full model using the single_layer_forward_propagate function
        :param inputs: vector of inputs of the neural network
        :return: vector of outputs of the neural network, dictionary of neurons value each layer
        """

        # Temporary memory to store valuable information for the backwards propagation
        memory = {}

        # Inputs vector is the input neurons of the model ("Layer 0")
        neurons = inputs

        # Loop through all layers
        for i, layer in enumerate(self.model_architecture):
            # Number the layers from 1
            prev_idx = str(i)
            idx = str(i + 1)

            prev_neurons = neurons

            # Get information of current layer
            activation = layer['activation']
            weights = self.model['w' + idx]
            biases = self.model['b' + idx]

            # Calculate neurons of next layer
            neurons, z = self.singe_layer_forward_propagate(prev_neurons, weights, biases, activation)

            # Store values in memory
            memory['a' + prev_idx] = prev_neurons
            memory['z' + idx] = z

        return neurons, memory

    def single_layer_backward_propagate(self, error, weights, z, prev_neurons):
        """
        Function that calculates the weights and biases delta for a single layer and returns the error of the previous
        layer neurons
        :return: previus layer neurons, weights delta, biases delta
        """

        n = prev_neurons.shape[1]

        delta_error = error * self.sigmoid_derivative(z)

        # Calculate effect of error on each weight and bias
        delta_weights = np.dot(delta_error, prev_neurons.T) / n
        delta_biases = np.sum(delta_error, axis=1, keepdims=True) / n
        # Calc prev layer error
        error = np.dot(weights.T, delta_error)
        return error, delta_weights, delta_biases

    def backwards_propagate(self, outputs, labels, memory):

        gradient = {}

        prev_error = outputs - labels

        # Loop without last layer
        for i, layer in reversed(list(enumerate(self.model_architecture))):
            prev_idx = str(i)
            idx = str(i + 1)

            error = prev_error

            prev_neurons = memory['a' + prev_idx]
            z = memory['z' + idx]

            weights = self.model['w' + idx]

            # Calculate the error of prev_neurons
            prev_error, d_weights, d_biases = self.single_layer_backward_propagate(error, weights, z, prev_neurons)

            gradient['w' + idx] = d_weights
            gradient['b' + idx] = d_biases

        return gradient

    def update(self, gradient, learning_rate):
        for idx, layer in enumerate(self.model_architecture, 1):
            idx = str(idx)
            self.model["w" + idx] -= learning_rate * gradient['w' + idx]
            self.model["b" + idx] -= learning_rate * gradient['b' + idx]


    def train(self, inputs, labels, epochs=500, learning_rate=0.01):

        cost_history = []
        accuracy_history = []

        # Create figure and add axes
        plt.ion()
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        for i in range(epochs):
            output, memory = self.forward_propagate(inputs[i])

            cost = self.get_cost_value(output, labels[i])
            cost_history.append(cost)
            accuracy = self.get_accuracy_value(output, labels[i])
            accuracy_history.append(accuracy)

            gradient = self.backwards_propagate(output, labels[i], memory)

            self.update(gradient, learning_rate)
            idx = 0
            if i % 10:
                print("cost", cost, "accuracy", accuracy)
                ax.plot(cost_history)
                idx += 1

                # function to show the plot
                fig.canvas.draw()
                fig.canvas.flush_events()
                print(output, labels[i])

        print("COST: ", sum(cost_history))
        print("Accuracy: ", sum(accuracy_history))
