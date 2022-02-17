from math import sqrt
from pygame import Rect
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


def bounds(point_list):

    # Find edges of drawing
    #  need to implement- instead of hardcoded min values we can do the width, height of canvas
    min_x, min_y = 1000, 1000
    max_x, max_y = 0, 0

    # find the biggest and smallest x,y values between all points:
    # Loop through lines
    for line in point_list:
        # loop through points in line
        for point in line:
            # find min x
            if point[0] < min_x:
                min_x = point[0]
            # find max x
            elif point[0] > max_x:
                max_x = point[0]
            # find min y
            if point[1] < min_y:
                min_y = point[1]
            # find max y
            elif point[1] > max_y:
                max_y = point[1]

    width = max(max_x - min_x, 1)
    height = max(max_y - min_y, 1)
    return Rect(min_x, min_y, width, height)


def relocate(point_list, bound):

    # put top left of drawing at 0, 0
    result_list = []
    for line in point_list:
        new_line = []
        for point in line:
            new_point = (point[0] - bound[0], point[1] - bound[1])
            new_line.append(new_point)

        result_list.append(new_line)

    return result_list


def rescale(point_list, bound, size=255):

    # find max between image width and image height
    dmax = max(bound.w, bound.h)

    # if we multiply each point by this value, we will receive a scaled image of [MAX_SIZE, MAX_SIZE]
    multiplier = size / dmax

    result_list = []
    for line in point_list:
        new_line = []
        for point in line:
            new_point = (round(point[0] * multiplier), round(point[1] * multiplier))
            new_line.append(new_point)
        result_list.append(new_line)

    new_bounds = bounds(result_list)

    return result_list, new_bounds


def bounding_rect(image: np.ndarray) -> None:

    # returns array
    print(image[0])
    without_zeros = np.where(image != 0)
    print(without_zeros[0])
    print(without_zeros)
    return
