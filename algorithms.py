import numpy as np

def douglas_peucker(pointList, epsilon):
    # Find point with the maximum distance
    max = 0
    index = 0
    p1 = np.array([pointList[0][0], pointList[1][0]])
    p2 = np.array([(pointList[0][-1], pointList[1][-1])])
    # x, y lists without first and last point
    x_list = pointList[0][1:-1]
    y_list = pointList[1][1:-1]
    # Loop through points except fist and last one
    for i, point in enumerate(zip(x_list, y_list)):
        # Calc distance between point and line from first to last in pointList
        dist = np.cross(p2 - p1, np.array([*point]) - p1) / np.linalg.norm(p2 - p1)
        if dist > max:
            max = dist
            index = i

    resultList = [[], []]

    if max > epsilon:
        r1 = douglas_peucker((pointList[:index]), epsilon)
        r2 = douglas_peucker((pointList[index:], epsilon))

        resultList.append(r1)
        resultList.append(r2)

    return resultList