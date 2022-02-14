from typing import Tuple
from Layers.Layer import Layer
import numpy as np


class Pooling(Layer):

    def __init__(self, pool_shape: Tuple[int, int] = (2, 2), stride: int = 1) -> None:

        self.pool_shape = pool_shape
        self.stride = stride

        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs

        # Unpack shapes
        n, in_h, in_w, filters_num = self.input.shape
        pool_h, pool_w, _ = self.pool_shape
        # Compute output shape
        out_h = 1 + (in_h - pool_h) // self.stride
        out_w = 1 + (in_w - pool_w) // self.stride
        # Initialize output
        self.output = np.zeros((n, out_h, out_w, filters_num))

        # Loop through amount of inputs
        for i in range(n):
            # Loop through output height
            for y in range(out_h):
                # Calculate coordinates for input image slice
                top = y * self.stride
                bottom = top + pool_h
                # Loop though output width
                for x in range(out_w):
                    # Calculate coordinates for input image slice
                    left = x * self.stride
                    right = left + pool_w
                    # Loop through amount of filters
                    for f in range(filters_num):
                        # find max in each image slice
                        self.output[i, y, x, f] = np.max(self.input[i, top:bottom, left:right, f])

        return self.output

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        # Unpack shapes
        n, in_h, in_w, filters_num = self.input.shape
        pool_h, pool_w, _ = self.pool_shape
        # Compute output shape
        out_h = 1 + (in_h - pool_h) // self.stride
        out_w = 1 + (in_w - pool_w) // self.stride
        # Initialize output
        output_gradient_out = np.zeros((n, in_h, in_h, filters_num))

        # Loop through amount of inputs
        for i in range(n):
            # Loop through output height
            for y in range(out_h):
                # Calculate coordinates for input image slice
                top = y * self.stride
                bottom = top + pool_h
                # Loop though output width
                for x in range(out_w):
                    # Calculate coordinates for input image slice
                    left = x * self.stride
                    right = left + pool_w
                    # Loop through amount of filters
                    for f in range(filters_num):
                        image_slice = self.input[i, top:bottom, left:right, f]
                        # Puts zero in indices that arent max in each images slice
                        output_gradient_out[i, top:bottom, left:right] += \
                            output_gradient[i, y, x, f] * (image_slice == np.max(slice))

        return output_gradient_out
