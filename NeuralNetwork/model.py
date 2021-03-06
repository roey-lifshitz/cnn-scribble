from typing import List, Tuple
from NeuralNetwork.base import Layer, Loss
from utils import shuffle
from NeuralNetwork.optimizers import Adam
from matplotlib import pyplot as plt
import numpy as np
import pickle
from datetime import datetime as dt


class Model:

    def __init__(self, layers: List[Layer], loss: Loss, optimizer: Adam, objects):

        self.model = layers
        self.loss = loss
        self.optimizer = optimizer
        self.objects = objects

        self.cost_history = []
        self.accuracy_history = []

    def evaluate(self, test_x, test_y):
        losses = []
        predictions = []

        for x, y, in zip(test_x, test_y):
            output = self.predict(x)
            losses.append(self.loss.compute_cost(y, output))
            predictions.append(int(np.argmax(y) == np.argmax(output)))

        return np.mean(losses), np.mean(predictions) * 100

    def predict(self, inputs, training= False):
        output = inputs

        for layer in self.model:
            output = layer.forward_propagate(output, training)

        return output

    def _back_propagate(self, output_gradient):

        for layer in reversed(self.model):
            output_gradient = layer.backward_propagate(output_gradient)

    def _update(self, learning_rate):

        for layer in self.model:
            layer.update(learning_rate)

    def train(self, train_x, train_y, test_x, test_y, epochs=1000, verbose=True, seed=99):
        np.random.seed(seed)

        self.optimizer.layers = self.model

        print("Started Training!")
        idx = 0

        for epoch in range(epochs):
            start_time = dt.now()

            train_x, train_y = shuffle(train_x, train_y, seed)

            for x, y in zip(train_x, train_y):
                # Feed forwards
                output = self.predict(x, True)
                # Compute Error
                output_gradient = self.loss.compute_derivative(y, output)
                # Feed backwards
                self._back_propagate(output_gradient)
                # Optimize network- update params
                self.optimizer.update()

            cost, accuracy = self.evaluate(test_x, test_y)

            self.cost_history.append(cost)
            self.accuracy_history.append(accuracy)

            if verbose:
                epoch_time = (dt.now() - start_time).seconds
                print(f"Epoch: {epoch + 1} / {epochs} | cost: {cost} | accuracy: {accuracy} | time: {epoch_time}")

            if epoch % 50 == 0:
                self.save(f"NeuralNetwork/Models/tmp{idx}.pkl")
                idx += 1

    def compute_graph(self):

        plt.figure(1)
        x = np.arange(1, len(self.cost_history) + 1)
        y1 = self.cost_history
        plt.xlabel("Epoch")
        plt.ylabel("Cost")
        plt.title("Cost History")
        plt.plot(x, y1, label="Cost History")

        plt.figure(2)
        y2 = self.accuracy_history
        plt.xlabel("Epoch")
        plt.ylabel("Cost")
        plt.title("Accuracy History")
        plt.plot(x, y2, label="Accuracy History")

        plt.show()

    def save(self, file):

        with open(file, 'wb') as f:
            pickle.dump(self, f)

    def update(self, file):

        with open(file, 'rb') as f:
            self.__dict__.update(pickle.load(f))

    @classmethod
    def load(cls, file):

        with open(file, 'rb') as f:
            cls = pickle.load(f)

        return cls
