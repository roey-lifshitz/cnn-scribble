from NeuralNetwork.base import Layer
import numpy as np


class Convolutional(Layer):

    def __init__(self, filters_num: int, filter_size: int, channels: int = 1, stride: int = 1) -> None:
        """

        :param filters_num: Number of filter in layer
        :param filter_size: Width/Height of filters kernel
        :param channels: depth of input channel
        :param stride: jump size of filters movement
        """
        self.filters_num = filters_num
        self.filter_size = filter_size
        self.channels = channels
        self.stride = stride

        self.filters = np.random.randn(filters_num, channels, filter_size, filter_size) * 0.1
        self.biases = np.random.randn(filters_num, 1) * 0.1

        self.delta_filters = np.zeros(self.filters.shape)
        self.delta_biases = np.zeros(self.biases.shape)

        self.input = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
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

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        # Unpack Shapes
        n_c, h_in, w_in = self.input.shape
        n_f, n_c, f_h, f_w = self.filters.shape

        # Compute output shape
        h_out = 1 + (h_in - f_h) // self.stride
        w_out = 1 + (w_in - f_w) // self.stride

        # Initialize gradients
        output_gradient_out = np.zeros(self.input.shape)
        self.delta_filters = np.zeros(self.filters.shape)
        self.delta_biases = np.zeros(self.biases.shape)

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

                    self.delta_filters[i] += \
                        output_gradient[i, h, w] * self.input[:, top:bottom, left:right]

                    output_gradient_out[:, top:bottom, left:right] += \
                        output_gradient[i, h, w] * self.filters[i]

            self.delta_biases[i] = np.sum(output_gradient[i])

        return output_gradient_out

    def get_params(self):
        return (self.filters, self.biases), (self.delta_filters, self.delta_biases)

    def set_params(self, weights, biases):
        self.filters = weights
        self.biases = biases


class Pooling(Layer):

    def __init__(self, filter_size: int, stride: int = 2) -> None:
        self.filter_size = filter_size
        self.stride = stride

        self.input = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
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

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
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


class Flatten(Layer):

    def __init__(self):
        self.input_shape = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input_shape = inputs.shape
        return np.ravel(inputs).reshape(-1, 1)

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        return output_gradient.reshape(self.input_shape)


class Dense(Layer):

    def __init__(self, dim_in, dim_out):
        self.dim_in = dim_in
        self.dim_out = dim_out

        self.weights = np.random.rand(dim_out, dim_in) * 0.1
        self.biases = np.random.rand(dim_out, 1) * 0.1

        self.delta_weights = None
        self.delta_biases = None

        self.input = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:
        self.input = inputs

        return np.dot(self.weights, inputs) + self.biases

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        n = self.input.shape[0]

        self.delta_weights = np.dot(output_gradient, self.input.T) / n
        self.delta_biases = np.sum(output_gradient, axis=1, keepdims=True) / n

        output_gradient_out = np.dot(self.weights.T, output_gradient)

        return output_gradient_out

    def get_params(self):
        return (self.weights, self.biases), (self.delta_weights, self.delta_biases)

    def set_params(self, weights, biases):

        self.weights = weights
        self.biases = biases


class Dropout(Layer):

    def __init__(self, prob):
        """
        :param prob - probability that given unit will not be dropped out
        """
        self.prob = prob
        self._mask = None

    def forward_propagate(self, inputs: np.ndarray, training: bool) -> np.ndarray:

        if training:
            # mask of number values with same shape of input
            self._mask = (np.random.rand(*inputs.shape) < self.prob)
            # return only values that their position in the mask is smaller than some prob
            return self._apply_mask(inputs, self._mask)
        else:
            return inputs

    def backward_propagate(self, output_gradient: np.ndarray) -> np.ndarray:
        output_gradient_out = self._apply_mask(output_gradient, self._mask)

        return output_gradient_out

    def _apply_mask(self, array: np.array, mask: np.array) -> np.array:
        array *= mask
        array /= self.prob

        return array

