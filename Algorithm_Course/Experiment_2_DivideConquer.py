import random
import numpy as np
import time
import matplotlib
from math import atan2


class Point:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key

    def __str__(self):
        """Returns a string containing instance information."""
        f = lambda n: int(n)
        return str(self.key) + ',\t' + str(f(self.x)) + ',\t' + str(f(self.y))


def generate_points(num_of_points):
    start = time.clock()

    graph_list = []
    point_num = 0

    while point_num < num_of_points:
        point_info = (random.randint(0, 100), random.randint(0, 100))
        while point_info not in graph_list:
            graph_list.append(point_info)
            point_num += 1

    graph = [Point(point_info[0], point_info[1], str(point_idx)) \
             for point_idx, point_info in enumerate(graph_list)]

    _out = []
    for point in graph:
        _out.append('\t'.join([str(point.key), str(point.x), str(point.y)]))

    """Prints the output file containing the the points"""
    with open(str(num_of_points) + '.txt', 'wb') as f:
        f.write('\n'.join(_out))

    elapsed = (time.clock() - start)
    print("generated %s points time used:%s" % (num_of_points, elapsed))

    return graph


def read_input_file(num_of_points):
    """Returns an array of points from the input file.
    Assumes that points will be floats.
    """
    graph = []
    with open(str(num_of_points) + '.txt', 'r') as f:
        for line in f:
            key, x, y = line.split('\t')
            graph.append(Point(int(x), int(y), key))

    return graph


def sort_points(graph):
    """Return graph sorted by leftmost first, then by slope, ascending."""

    def slope(a):
        """returns the slope of the 2 points."""

        return atan2(graph[0].x - a.x, a.y - graph[0].y)

    def polar(a, b):
        if ((a.x - graph[0].x) * (b.y - graph[0].y) - (b.x - graph[0].x) * (a.y - graph[0].y) == 0): #if the angle of two points are same, then select the one with smaller x-value
            return a.x < b.x
        else:
            return (a.x - graph[0].x) * (b.y - graph[0].y) - (b.x - graph[0].x) * (a.y - graph[0].y) > 0

    def compare_position(a,b):
        if a.y != b.y:
            return a.y - b.y
        else:
            return a.x - b.x

    graph=sorted(graph,cmp=compare_position)  # put leftmost first

    # print 'graph[0]:', graph[0]
    # graph = graph[:1] + sorted(graph[1:], cmp=polar)
    graph = graph[:1] + sorted(graph[1:], key=slope)

    for p in graph:
        print p

    return graph


def graham_scan(graph):
    """Takes an array of points to be scanned.
    Returns an array of points that make up the convex hull surrounding the points passed in in graph.
    """

    def compare_position(a, b):
        if (a.y < b.y) or (a.y == b.y and a.x < b.x):
            return a
        else:
            return b

    # OA x OB
    # greater than 0 -> counterclockwise from OA->OB
    def cross_product(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    start = time.clock()
    # convex_hull is a stack of points beginning with the leftmost point.
    convex_hull = []
    sorted_points = sort_points(graph)

    for p in sorted_points:
        while len(convex_hull) > 1 and cross_product(convex_hull[-2], convex_hull[-1], p) < 0:
            convex_hull.pop()
        convex_hull.append(p)
    elapsed = (time.clock() - start)
    print("graham_scan time used:%s" % (elapsed))

    convex_hull_key_list = []
    for point in convex_hull:
        convex_hull_key_list.append(point.key)

    return convex_hull, sorted(convex_hull_key_list)


def brute_force(graph):
    start = time.clock()
    # convex_hull is a stack of points beginning with the leftmost point.
    convex_hull = []

    def cross_product(a, b, c):
        value = a.x * b.y + c.x * a.y + b.x * c.y - c.x * b.y - b.x * a.y - a.x * c.y
        return np.sign(value)

    for point1 in graph:
        for point2 in graph:
            convex_hull_flag = True
            if point1.key == point2.key:
                continue
            direction_flag = None

            for point3 in graph:
                if point3.key != point2.key and point3.key != point1.key:
                    if cross_product(point1, point2, point3) != direction_flag and direction_flag != None:
                        convex_hull_flag = False
                        break
                    else:
                        direction_flag = cross_product(point1, point2, point3)

            if convex_hull_flag:
                convex_hull.append(point1)
                convex_hull.append(point2)

    convex_hull=list(set(convex_hull))

    elapsed = (time.clock() - start)
    print("brute_force time used:%s" % (elapsed))

    convex_hull_key_list = []
    for point in convex_hull:
        convex_hull_key_list.append(point.key)

    return convex_hull, sorted(convex_hull_key_list)


if __name__ == "__main__":
    # graph=generate_points(10)

    # for point in graph:
    #     print point

    graph = read_input_file(10)
    # for point in graph:
    #     print point

    # sort_points(graph)
    # for point in sort_points(graph):
    #     print point


    g_graph, g_graph_list = graham_scan(graph)
    b_graph, b_graph_list = brute_force(graph)

    print g_graph_list
    print b_graph_list
    print g_graph_list == b_graph_list
    #
    #
    #
    # import matplotlib.pyplot as plt
    # import numpy as np
    #
    # xValue = [p.x for p in graph]
    # yValue = [p.y for p in graph]
    # keyValue = [p.key for p in graph]
    #
    # fig, ax = plt.subplots()
    # ax.scatter(xValue, yValue)
    #
    # for i, txt in enumerate(keyValue):
    #     ax.annotate(txt, (xValue[i], yValue[i]))
    #
    # # plt.title('point')
    # #
    # # plt.xlabel('x-value')
    # # plt.ylabel('y-label')
    # # plt.legend()
    # #
    # # plt.scatter(xValue, yValue, s=20, c="#ff1212", marker='o')
    # plt.show()
