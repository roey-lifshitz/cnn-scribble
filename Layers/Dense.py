from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Dense(Layer):

    def __init__(self, num_neurons):
        self.num_neurons = num_neurons;
        self.W = None

    def forward_propagate(self, input):
        if self.W is None:
            self.W = np.random.random((self.num_neurons, input.shape[1] + 1)) * 0.1
        self.input = np.hstack([input, np.ones((input.shape[0], 1))])  # add bias inputs
        self.Z = np.dot(self.input, self.W.transpose())
        return self.Z

    def backward_propagate(self, dA, learning_rate):
        dZ = dA
        dW = np.dot(self.input.transpose(), dZ).transpose() / dA.shape[0]
        dA_prev = np.dot(dZ, self.W)
        dA_prev = np.delete(dA_prev, dA_prev.shape[1] - 1, 1)  # remove bias inputs
        self.W = self.W - learning_rate * dW
        return dA_prev
