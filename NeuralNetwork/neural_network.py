from typing import List, Tuple
from NeuralNetwork.base import Layer, Loss
from utils import shuffle, generate_batches
from NeuralNetwork.optimizers import Adam
from matplotlib import pyplot as plt
import numpy as np
import pickle
from datetime import datetime as dt


class NeuralNetwork:

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

        return np.mean(losses) * 100, np.mean(predictions) * 100

    def predict(self, inputs, training= False):
        output = inputs
        for layer in self.model:
            output = layer.forward_propagate(output, training)

        # clip gradient so their wont be log(0)
        #output = np.clip(output, 1e-8, None)

        return output

    def _back_propagate(self, output_gradient, learning_rate):
        # back propagate
        for layer in reversed(self.model):
            output_gradient = layer.backward_propagate(output_gradient, learning_rate)
            # gradient clipping
            # in some instances, after training a long time we get exploding gradients so we clip the gradients to
            # remove that
            output_gradient = np.clip(output_gradient, None, 0.5)


    def train(self, train_x, train_y, test_x, test_y, epochs=1000, learning_rate=0.01, verbose=True, seed=99):
        np.random.seed(seed)
        print("Started Training!")
        for epoch in range(epochs):
            start_time = dt.now()

            for x, y, in zip(*shuffle(train_x, train_y)):
                # Feed forwards
                output = self.predict(x, True)
                # Compute Error
                output_gradient = self.loss.compute_derivative(y, output)
                # Feed backwards
                self._back_propagate(output_gradient, learning_rate)

            cost, accuracy = self.evaluate(test_x, test_y)
            self.cost_history.append(cost)
            self.accuracy_history.append(accuracy)

            if verbose:
                epoch_time = (dt.now() - start_time).seconds
                print(f"Epoch: {epoch + 1} / {epochs} | cost: {cost} | accuracy: {accuracy} | time: {epoch_time}")

            if epoch % 50 == 0:
                self.save("NeuralNetwork/Models/tmp.pkl")


    def compute_graph(self):
        x = np.linspace(0, len(self.cost_history))
        y = self.cost_history
        plt.plot(x, y)
        plt.show()
        y = self.accuracy_history
        plt.plot(x, y)
        plt.show()

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.__dict__, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.__dict__.update(pickle.load(f))
