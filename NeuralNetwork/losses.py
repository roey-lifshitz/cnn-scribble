from NeuralNetwork.base import Loss
import numpy as np


class CrossEntropyLoss(Loss):

    def compute_cost(self, labels: np.ndarray, predictions: np.ndarray, epsilon=1e-8) -> np.float:
        predictions /= np.sum(predictions)
        predictions = np.clip(predictions, epsilon, 1. - epsilon)
        return -np.sum(labels * np.log(predictions))

    def compute_derivative(self, labels: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        return predictions - labels
