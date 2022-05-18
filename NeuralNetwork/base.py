from typing import Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np


class Layer(ABC):
    """ Base class for a layer in the Convolutional Neural Network """

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
    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        """
        Backward pass logic of a Layer
        :param output_gradient: gradient of previous layer
        :return: Output gradient for previous layer
        """
        pass

    def get_params(self) -> Optional[Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]]:
        """
        Returns trainable params and their deltas for optimizer
        if layers has no trainable values it returns None otherwise
        it returns a tuple that contains (weights, biases), delta_weights, delta_biases)
        :return: None or (weights, biases), delta_weights, delta_biases)
        """

        return None

    def set_params(self, weights: np.ndarray, biases: np.ndarray) -> None:
        """
        Updates the trainable data of a layer
        :param weights: filters/weights of layer
        :param biases: bias of layer
        :return:
        """
        pass


class Loss(ABC):
    """ Base class for a lose function of a Neural Network"""

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


class Optimizer(ABC):
    """ Base class for a Optimizer of a Neural Network"""

    @abstractmethod
    def update(self) -> None:
        """
        Updates the values of the trainable parameters
        :return: None
        """
        pass
