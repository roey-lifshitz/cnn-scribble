from typing import List, Tuple
from Layers.Layer import Layer
import numpy as np
import pickle
from datetime import datetime as dt


class NeuralNetwork:

    def __init__(self):

        self.model = None
        self.cost_history = []
        self.accuracy_history = []

    @staticmethod
    def _shuffle(x: np.ndarray, y: np.ndarray, seed: int = 99) -> Tuple[np.ndarray, np.ndarray]:
        """
        Randomizes two nd.arrays with the same length in unison
        :param x: images
        :param y: hot one encoding of y
        :param seed:
        :return: Randomized x, y
        """
        if len(x) != len(y):
            raise ValueError('x, y cannot have different lengths!')

        # Allocate space
        shuffled_x = np.empty(x.shape, dtype=x.dtype)
        shuffled_y = np.empty(y.shape, dtype=x.dtype)
        # All indexes in random order
        permutation = np.random.permutation(len(x))
        # Shuffle
        for old_index, new_index in enumerate(permutation):
            shuffled_x[new_index] = x[old_index]
            shuffled_y[new_index] = y[old_index]

        return shuffled_x, shuffled_y

    # Categorical cross-entropy loss function
    @staticmethod
    def cross_entropy_loss(labels, predictions, epsilon=1e-8):
        predictions /= np.sum(predictions)
        predictions = np.clip(predictions, epsilon, 1. - epsilon)
        return -np.sum(labels * np.log(predictions))

    def initialize(self, layers: List[Layer]):
        self.model = layers

    def evaluate(self, test_x, test_y):
        losses = []
        predictions = []
        i = 0
        for x, y, in zip(test_x, test_y):

            output = self.predict(x)

            losses.append(self.cross_entropy_loss(y, output))

            predictions.append(int(np.argmax(y) == np.argmax(output)))

        return np.mean(losses) * 100, np.mean(predictions) * 100

    def predict(self, inputs):
        output = inputs
        for layer in self.model:
            output = layer.forward_propagate(output)

        # limit the values in the array to avoid log(0)
        output = np.clip(output, 1e-15, None)
        return output

    def _backpropagate(self, output_gradient, learning_rate):
        # back propagate
        for layer in reversed(self.model):
            output_gradient = layer.backward_propagate(output_gradient, learning_rate)

    def train(self, train_x, train_y, test_x, test_y, epochs=1000, learning_rate=1, verbose=True, seed= 99):
        np.random.seed(seed)
        print("Started Training!")
        for epoch in range(epochs):
            start_time = dt.now()



            for x, y, in zip(*self._shuffle(train_x, train_y)):
                # Feed forwards
                output = self.predict(x)

                # Compute Error
                output_gradient = output - y

                # Feed backwards
                self._backpropagate(output_gradient, learning_rate)

            cost, accuracy = self.evaluate(test_x, test_y)
            self.cost_history.append(cost)
            self.accuracy_history.append(accuracy)

            if verbose:
                epoch_time = (dt.now() - start_time).seconds
                print(f"Epoch: {epoch + 1} / {epochs} | cost: {cost} | accuracy: {accuracy} | time: {epoch_time}")

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.model = pickle.load(f)
