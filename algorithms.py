from math import sqrt
from math import sqrt, inf

# distance between 2 points
def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

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


def douglas_peucker(point_list, epsilon):
    if not point_list:
        return
    dmax = 0.0
    index = 0
    for i in range(1, len(point_list) - 1):
        d = perpendicular_distance(point_list[i], point_list[0], point_list[-1])
        if d > dmax:
            index = i
            dmax = d

    if dmax >= epsilon:
        result_list = douglas_peucker(point_list[:index + 1], epsilon)[:-1] + douglas_peucker(point_list[index:], epsilon)
    else:
        result_list = [point_list[0], point_list[-1]]

    return result_list


def bounds(point_list):

    # Find edges of drawing
    min_x, min_y = inf, inf
    max_x, max_y = -inf, -inf

    for line in point_list:
        for point in line:
            if point[0] < min_x:
                min_x = point[0]
            elif point[0] > max_x:
                max_x = point[0]

            if point[1] < min_y:
                min_y = point[1]
            elif point[1] > max_y:
                max_y = point[1]

    return min_x, min_y, max_x - min_x, max_y - min_y


def relocate(point_list, bounds):

    # put top left of drawing at 0, 0
    result_list = []
    for line in point_list:
        new_line = []
        for point in line:
            new_point = (point[0] - bounds[0], point[1] - bounds[1])
            new_line.append(new_point)

        result_list.append(new_line)

    return result_list
