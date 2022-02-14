from abc import ABC, abstractmethod
import numpy as np

class Layer(ABC):

    @abstractmethod
    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass logic of a Layer
        :param inputs: Output of previous layer
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
