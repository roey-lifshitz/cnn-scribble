from typing import List
from Layers.Layer import Layer
import numpy as np
import pickle
import time


class NeuralNetwork:

    def __init__(self):

        self.model = None

    # Categorical cross-entropy loss function
    @staticmethod
    def get_cost(true_y, pred_y):
        return -np.sum(true_y * np.log(pred_y)) / true_y.shape[0]

    def initialize(self, layers : List[Layer]):
        self.model = layers

    def predict(self, inputs):
        output = inputs
        for layer in self.model:
            output = layer.forward_propagate(output)
            # limit the values in the array to avoid log(0)
        output = np.clip(output, 1e-15, None)
            # small amount of noise to break ties
        output += np.random.random(output.shape) * 0.00001

        return output

    def evaluate(self, test_x, test_y):
        cost = 0
        accuracy = 0
        for x, y, in zip(test_x, test_y):
            output = self.predict(x)

            cost += self.get_cost(y, output)
            accuracy += y[np.argmax(output)]

        return cost / len(test_x), accuracy / len(test_x)

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.model = pickle.load(f)

    def train(self, train_x, train_y, test_x, test_y, epochs=400, learning_rate=0.01, verbose= True):

        for epoch in range(epochs):
            start_time = time.time()
            for x, y, in zip(train_x, train_y):

                output = self.predict(x)

                output_gradient = output - y

                # back propagate
                for layer in reversed(self.model):
                    output_gradient = layer.backward_propagate(output_gradient, learning_rate)


            cost, accuracy = self.evaluate(test_x, test_y)

            if verbose:
                epoch_time = time.gmtime(time.time() - start_time)
                print(f"Epoch: {epoch + 1} / {epochs} | cost: {cost} | accuracy: {accuracy} | time: {epoch_time}")

            if epoch % 50:
                self.save("Models/tmp.pkl")