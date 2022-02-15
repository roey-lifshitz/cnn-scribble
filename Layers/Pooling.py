from typing import Tuple
from Layers.Layer import Layer
import numpy as np


class Pooling(Layer):

    def __init__(self, filter_size: int, stride: int = 2) -> None:

        self.filter_size = filter_size
        self.stride = stride

        self.input = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:

        self.input = inputs

        # Unpack shapes
        n_c, h_in, w_in = inputs.shape
        f_h, f_w = self.filter_size, self.filter_size

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride

        # Initialize output
        output = np.zeros((n_c, h_out, w_out))

        # foreach channel
        for i in range(n_c):
            # Slide filters vertically across image
            for h in range(h_out):
                top = h * self.stride
                bottom = top + f_h
                # Slide filters horizontally across image
                for w in range(w_out):
                    left = w * self.stride
                    right = left + f_w

                    output[i, h, w] = \
                        np.max(inputs[i, top:bottom, left:right])

        return output

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:

        # Unpack shapes
        n_c, h_in, w_in = self.input.shape
        f_h, f_w = self.filter_size, self.filter_size

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride

        # Initialize output
        output_gradient_out = np.zeros(self.input.shape)

        # For each image
        for i in range(n_c):
            # Slide filters vertically
            for h in range(h_out):
                # Calculate coordinates for image slice
                top = h * self.stride
                bottom = top + f_h
                # Slide filters horizontally
                for w in range(w_out):
                    # Calculate coordinates for input image slice
                    left = w * self.stride
                    right = left + f_w

                    # Obtain index of largest value in image slice
                    index = np.nanargmax(self.input[i, top:bottom, left:right])

                    a, b = np.unravel_index(index, self.input[i, top:bottom, left:right].shape)
                    output_gradient_out[i, h + a, w + b] = output_gradient[i, h, w]

        return output_gradient_out

