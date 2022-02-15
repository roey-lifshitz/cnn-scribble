from typing import Tuple
from Layers.Layer import Layer
import numpy as np


class Convolutional(Layer):

    def __init__(self, filters_num: int = 8, kernel_shape: Tuple[int, int] = (2, 2), stride: int = 1,
                 padding: int = 0) -> None:

        self.filters_num = filters_num
        self.kernel_shape = kernel_shape
        self.stride = stride
        self.padding = padding

        # Initialize weights and biases

        self.weights = None
        self.biases = None

        self.input = None
        self.output = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        self.input = inputs
        # Pad input if needed using numpy built-in function
        if self.padding != 0:
            # array, (top, bottom), (left, right), mode constant= pad with zeros
            #self.input = np.pad(inputs, (self.padding, self.padding), (self.padding, self.padding), mode='constant')
            shape = ((0, 0), (self.padding, self.padding), (self.padding, self.padding), (0, 0))
            self.input = np.pad(inputs, shape, mode='constant', constant_values=(0, 0))

        # Unpack shapes
        n, in_h, in_w, filters = self.input.shape
        kernel_h, kernel_w = self.kernel_shape
        # Initialize weighs and biases
        if self.weights is None:
            self.weights = np.random.randn(*self.kernel_shape, filters, self.filters_num) * 0.01
        if self.biases is None:
            self.biases = np.random.randn(self.filters_num) * 0.01

        # Compute output shape
        out_h = 1 + (in_h - kernel_h + 2 * self.padding) // self.stride
        out_w = 1 + (in_w - kernel_w + 2 * self.padding) // self.stride
        # Initialize output
        self.output = np.zeros((n, out_h, out_w, self.filters_num))

        # Loop through amount of inputs
        for i in range(n):
            # Loop through output height
            for y in range(out_h):
                # Calculate coordinates for input image slice
                top = y * self.stride
                bottom = top + kernel_h
                # Loop though output width
                for x in range(out_w):
                    # Calculate coordinates for input image slice
                    left = x * self.stride
                    right = left + kernel_w
                    # Loop through amount of filters
                    for f in range(self.filters_num):
                        # Calculate output
                        self.output[i, y, x, f] = np.sum(
                            self.input[i, top:bottom, left:right, :] * self.weights[:, :, :, f])
                        self.output[:, :, :, f] += self.biases[f]

        return self.output

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        # Unpack shapes
        n, in_h, in_w, _ = self.input.shape
        kernel_h, kernel_w = self.kernel_shape
        # Compute output shape
        out_h = 1 + (in_h - kernel_h + 2 * self.padding) // self.stride
        out_w = 1 + (in_w - kernel_w + 2 * self.padding) // self.stride
        # Initialize output
        output_gradient_out = np.zeros((n, in_h, in_h, self.filters_num))
        delta_weights = np.zeros(self.weights.shape)
        delta_biases = np.zeros(self.biases.shape)
        # Loop through amount of inputs
        for i in range(n):
            # Loop through output height
            for y in range(out_h):
                # Calculate coordinates for input image slice
                top = y * self.stride
                bottom = top + kernel_h
                # Loop though output width
                for x in range(out_w):
                    # Calculate coordinates for input image slice
                    left = x * self.stride
                    right = left + kernel_w
                    # Loop through amount of filters
                    for f in range(self.filters_num):
                        delta_biases[f] += output_gradient[i, y, x, f]

                        delta_weights[:, :, :, f] += \
                            output_gradient[i, y, x, f] * self.input[i, top:bottom, left:right, :]

                        output_gradient_out[i, top:bottom, left:right, :] += \
                            output_gradient[i, y, x, f] * self.weights[:, :, :, f]

        # Update weights and biases according to gradient descent
        self.weights -= delta_weights * learning_rate
        self.biases -= delta_biases * learning_rate

        # Remove padding
        if self.padding > 0:
            output_gradient_out = output_gradient_out[:, self.padding:-self.padding, self.padding:-self.padding, :]

        return output_gradient_out
