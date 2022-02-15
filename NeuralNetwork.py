from typing import List
from Layers.Layer import Layer
import numpy as np
import pickle
from datetime import datetime as dt


class NeuralNetwork:

    def __init__(self):

        self.model = None

    # Categorical cross-entropy loss function
    @staticmethod
    def cross_entropy_loss(y_pred, y_true):
        n = y_pred.shape[1]
        loss = -np.sum(y_true * np.log(y_pred)) / n
        return loss

    def initialize(self, layers : List[Layer]):
        self.model = layers

    def predict(self, inputs):
        output = inputs
        for layer in self.model:
            output = layer.forward_propagate(output)

        # limit the values in the array to avoid log(0)
        output = np.clip(output, 1e-15, None)

        return output

    def evaluate(self, test_x, test_y):
        accuracy = 0
        for x, y, in zip(test_x, test_y):
            output = self.predict(x)

            if (accuracy == y[np.argmax(output)]):
                accuracy += 1
                print(y, output)


        return accuracy / len(test_x) * 100

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, file):
        with open(file, 'rb') as f:
            self.model = pickle.load(f)

    def train(self, train_x, train_y, test_x, test_y, epochs=400, learning_rate=0.01, verbose= True):

        for epoch in range(epochs):
            cost_history = []
            start_time = dt.now()
            for x, y, in zip(train_x, train_y):

                output = self.predict(x)

                output_gradient = output - y
                #print(output_gradient)
                cost_history.append(self.cross_entropy_loss(output, y))

                # back propagate
                for layer in reversed(self.model):
                    output_gradient = layer.backward_propagate(output_gradient, learning_rate)


            accuracy = self.evaluate(test_x, test_y)
            cost = sum(cost_history) / len(cost_history)

            if verbose:
                epoch_time = (dt.now() - start_time).seconds
                print(f"Epoch: {epoch + 1} / {epochs} | cost: {cost} | accuracy: {accuracy} | time: {epoch_time}")

            if epoch % 50 == 0:
                self.save("Models/tmp.pkl")