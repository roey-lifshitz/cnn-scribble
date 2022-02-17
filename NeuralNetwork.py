from typing import List
from Layers.Layer import Layer
import numpy as np
import pickle
import matplotlib.pyplot as plt
from datetime import datetime as dt


class NeuralNetwork:

    def __init__(self):

        self.model = None
        self.epochs = None
        self.cost_history = []
        self.accuracy_history = []

    # Categorical cross-entropy loss function
    @staticmethod
    def cross_entropy_loss(y_pred, y_true):

        loss = -np.sum(y_true * np.log(y_pred))
        return loss / y_pred.shape[0]

    def initialize(self, layers: List[Layer]):
        self.model = layers

    def compute_graphs(self):

        plt.plot(range(self.epochs), self.accuracy_history, 'g', label='Accuracy')
        plt.plot(range(self.epochs), self.cost_history, 'b', label='Cost')
        plt.title('Training Accuracy and Cost')
        plt.xlabel('Epochs')
        plt.legend()
        plt.show()



    def evaluate(self, test_x, test_y):
        losses = []
        predictions = []
        i = 0
        for x, y, in zip(test_x, test_y):

            output = self.predict(x)

            losses.append(self.cross_entropy_loss(output, y))

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
        self.epochs = epochs
        for epoch in range(epochs):
            start_time = dt.now()

            for x, y, in zip(train_x, train_y):
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

            if epoch % 50 == 0:
                self.save("Models/tmp5.pkl")

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.model = pickle.load(f)
