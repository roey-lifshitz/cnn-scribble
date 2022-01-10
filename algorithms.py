from math import sqrt
import numpy as np
from math import sqrt

# distance between 2 points
def dist(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# distance between point and line
def perpendicular_distance(point, start, end):
    if (start == end):
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



def douglas_peucker(pointList, epsilon):
    if not pointList:
        return
    dmax = 0.0
    index = 0
    for i in range(1, len(pointList) - 1):
        d = perpendicular_distance(pointList[i], pointList[0], pointList[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        resultList = douglas_peucker(pointList[:index + 1], epsilon)[:-1] + douglas_peucker(pointList[index:], epsilon)
    else:
        resultList = [pointList[0], pointList[-1]]

    return resultList