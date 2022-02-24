from math import sqrt
from typing import Optional, Tuple
from matplotlib import pyplot as plt

import pygame
import numpy as np


def dist(a, b):
    """
    Calculates distance between two points
    :param a: point
    :param b: point
    :return: distance
    """
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def perpendicular_distance(point, start, end):
    """
    Calculates distacne between point and line
    :param point: point
    :param start: line start
    :param end: line end
    :return: distance
    """
    # if line is actually a point
    if start == end:
        return dist(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) -
            (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d


def douglas_peucker(point_list, epsilon):
    """
    Algorithm that transforms a curve composed of points to a similar curve with fewer points
    :param point_list: list of points [(x, y), (x2, y2)]
    :param epsilon:
    :return: list with fewer points
    """
    if not point_list:
        return

    dmax = 0.0
    index = 0
    # Loop through points except start and end
    for i in range(1, len(point_list) - 1):

        # Find the point farthest from line
        d = perpendicular_distance(point_list[i], point_list[0], point_list[-1])
        if d > dmax:
            index = i
            dmax = d

    # point farthest from line bigger than user given epsilon
    if dmax >= epsilon:
        # call recursive call on point list where furthest point will be either start/end in next calls
        result_list = douglas_peucker(point_list[:index + 1], epsilon) + douglas_peucker(point_list[index:], epsilon)
    else:
        # Return start and end
        result_list = [point_list[0], point_list[-1]]

    return result_list


def shuffle(x: np.ndarray, y: np.ndarray, seed: int = 99) -> Tuple[np.ndarray, np.ndarray]:
    np.random.seed(seed)
    """
    Randomizes two nd.arrays with the same length in unison
    :param x: images
    :param y: hot one encoding of y
    :param seed:
    :return: Randomized x, y
    """
    if len(x) != len(y):
        raise ValueError('x, y cannot have different lengths!')

    # Allocate space
    shuffled_x = np.empty(x.shape, dtype=x.dtype)
    shuffled_y = np.empty(y.shape, dtype=y.dtype)
    # All indexes in random order
    permutation = np.random.permutation(len(x))
    # Shuffle
    for old_index, new_index in enumerate(permutation):
        shuffled_x[new_index] = x[old_index]
        shuffled_y[new_index] = y[old_index]

    return shuffled_x, shuffled_y


def crop_whitespaces(image: np.ndarray) -> np.ndarray:
    """
    Crops the white border (Represented with zeros) from an image
    represented by a 2D numpy array
    :param image: shape (width, height)
    :return: Cropped image
    """

    # np.where Returns a tuple:
    # [0]-> x pixel location of all pixels with value != 0
    # [1]-> y pixel location of all pixels with value != 0
    pixels_x, pixels_y = np.where(image != 0)

    # Find image border
    min_x = np.min(pixels_x)
    max_x = np.max(pixels_x)

    min_y = np.min(pixels_y)
    max_y = np.max(pixels_y)

    cropped_image = image[min_x:max_x, min_y:max_y]

    return cropped_image


def add_border(image: np.ndarray, padding: Optional[Tuple[int, int]] = (0, 0),
               same_scale: Optional[bool] = False) -> np.ndarray:
    """
    Adds a border to an image represented by a 2d numpy array
    :param image: shape (width, height)
    :param padding: (width, height) of padding to add to the image
    :param same_scale: if we want the width and height of image to be the same before padding
    :return: Image with border
    """

    width, height = image.shape

    width_out = width + padding[0]
    height_out = height + padding[1]

    if same_scale:
        width_out = max(width, height) + padding[0]
        height_out = max(width, height) + padding[1]

    # Allocate space for new image with padding
    border_image = np.zeros((width_out, height_out), dtype='float32')

    # compute center offset
    x_start = (width_out - width) // 2
    y_start = (height_out - height) // 2

    # copy img image into center of result image
    border_image[x_start:x_start + width, y_start:y_start + height] = image

    return border_image


def down_sample(image: np.ndarray, size: Tuple[int, int], threshold: float = 1) -> np.ndarray:
    """
    Down samples an image represented by a numpy 2d array recursively.
    Every time down samples an image by two until it reaches a (width, height) that is <= than size
    then add adds a border if image is smaller than size

    does the down sampling by:
        calculating the average of the three largest pixels in each 2x2 slice
    :param image: shape (width, height)
    :param size: (width, height) to downscale
    :param threshold: effects the calculation of each output pixel
    :return: Down sampled image
    """
    width, height = image.shape

    if threshold > 1:
        raise ValueError('Threshold bigger than one')

    # if image has different width and height then we pad it
    # can only be true in the first call of the function
    if width != height:
        # Add padding to image
        image = add_border(image, same_scale=True)

    if width <= size[0] and height <= size[1]:
        return add_border(image, padding=(size[0] - width, size[1] - height))
    else:
        down_sample_image = np.empty((width // 2, (height // 2)))
        for i in range(width // 2):
            for j in range(height // 2):
                # list of all values in image slice in decreasing order
                pixels = np.sort(image[i*2:i*2+2, j*2:j*2+2].ravel())[::-1]
                # average the largest 3 values
                value = min(np.mean(pixels[0:3]) / threshold, 1)

                down_sample_image[i, j] = value

        # Call recursively to down sample again
        return down_sample(down_sample_image, size)



