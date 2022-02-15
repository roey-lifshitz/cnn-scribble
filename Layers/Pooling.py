from typing import Tuple
from Layers.Layer import Layer
import numpy as np


class Pooling(Layer):

    def __init__(self, filter_size: int, stride: int = 1) -> None:

        self.filter_size = filter_size
        self.stride = stride

        self.input = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:

        self.input = inputs

        # Unpack shapes
        n, c, h_in, w_in = self.input.shape
        f_h, f_w = self.filter_size, self.filter_size

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride

        # Initialize output
        output = np.zeros((n, c, h_out, w_out))

        # For each image
        for i in range(n):
            # For each channel
            for c in range(c):
                # Slide filters vertically
                for y in range(h_out):
                    # Calculate coordinates for image slice
                    top = y * self.stride
                    bottom = top + f_h
                    # Slide filters horizontally
                    for x in range(w_out):
                        # Calculate coordinates for input image slice
                        left = x * self.stride
                        right = left + f_w

                        output[i, c, y, x] = np.max(inputs[i, c, top:bottom, left:right])

        return output

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:

        # Unpack shapes
        f_h, f_w = self.filter_size, self.filter_size
        n, c, h_out, w_out, = output_gradient.shape

        # Initialize output
        output_gradient_out = np.zeros(self.input.shape)

        # For each image
        for i in range(n):
            # For each channel
            for c in range(c):
                # Slide filters vertically
                for y in range(h_out):
                    # Calculate coordinates for image slice
                    top = y * self.stride
                    bottom = top + f_h
                    # Slide filters horizontally
                    for x in range(w_out):
                        # Calculate coordinates for input image slice
                        left = x * self.stride
                        right = left + f_w

                        image_slice = self.input[i, c, top:bottom, left:right]
                        output_gradient_out[i, c, top:bottom, left:right] = \
                            output_gradient[i, c, y, x] * (image_slice == np.max(image_slice))

        return output_gradient_out

