from typing import Tuple
from Layers.Layer import Layer
from scipy import signal
import numpy as np


class Convolutional(Layer):

    def __init__(self, filters_num: int, filter_size: int, channels: int = 1, stride: int = 1) -> None:

        self.filters_num = filters_num
        self.filter_size = filter_size
        self.channels = channels
        self.stride = stride

        self.filters = np.random.randn(filters_num, channels, filter_size, filter_size) * 0.1
        self.biases = np.random.randn(filters_num, 1)

        self.input = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:

        self.input = inputs

        # Unpack Shapes
        n_c, h_in, w_in = inputs.shape
        n_f, n_c, f_h, f_w = self.filters.shape

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride
        # n_f will be the depth of the filters

        # Initialize output
        output = np.zeros((n_f, h_out, w_out))

        # foreach filter
        for i in range(n_f):
            # Slide filters vertically across image
            for h in range(h_out):
                top = h * self.stride
                bottom = top + f_h
                # Slide filters horizontally across image
                for w in range(w_out):
                    left = w * self.stride
                    right = left + f_w

                    output[i, h, w] = \
                        np.sum(self.filters[i] * inputs[:, top:bottom, left:right])

                    output[i, h, w] += self.biases[i]

        return output

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:

        # Unpack Shapes
        n_c, h_in, w_in = self.input.shape
        n_f, n_c, f_h, f_w = self.filters.shape

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride

        # Initialize gradients
        output_gradient_out = np.zeros(self.input.shape)
        delta_filters = np.zeros(self.filters.shape)
        delta_biases = np.zeros(self.biases.shape)

        # foreach filter
        for i in range(n_f):
            # Slide filters vertically across image
            for h in range(h_out):
                top = h * self.stride
                bottom = top + f_h
                # Slide filters horizontally across image
                for w in range(w_out):
                    left = w * self.stride
                    right = left + f_w

                    delta_filters[i] += \
                        output_gradient[i, h, w] * self.input[:, top:bottom, left:right]

                    output_gradient_out[:, top:bottom, left:right] += \
                        output_gradient[i, h, w] * self.filters[i]

                delta_biases[i] = np.sum(output_gradient[i])

        return output_gradient_out


