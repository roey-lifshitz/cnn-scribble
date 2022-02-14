from abc import ABC
import numpy as np

class Layer(ABC):

    def forward_propagate(self, inputs : np.array): -> np.array()
        pass