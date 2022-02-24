from abc import ABC, abstractmethod
import numpy as np

class Layer(ABC):

    @abstractmethod
    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        """
        Forward pass logic of a Layer
        :param inputs: Output of previous layer
        :param training: bool if forward_propagate is for training
        :return: Output of this layer
        """
        pass

    @abstractmethod
    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """
        Backward pass logic of a Layer
        :param output_gradient: gradient of previous layer
        :param learning_rate: jump size for trainable data manipulation
        :return: Output gradient for previous layer
        """
        pass

    @abstractmethod
    def update(self):
        pass


class Loss(ABC):

    @abstractmethod
    def compute_cost(self, labels: np.ndarray, predictions: np.ndarray) -> np.float:
        """
        Calculates the cost of a single output
        :param labels: hot one encoding of answer
        :param predictions: output of forward propagate
        :return: cost of single output
        """
        pass

    @abstractmethod
    def compute_derivative(self, labels: np.ndarray, predictions: np.ndarray) -> np.ndarray:
        """
        Calculated the error of a single output
        :param labels: hot one encoding of answer
        :param predictions: output of forward propagate
        :return: error of a single output
        """
        pass