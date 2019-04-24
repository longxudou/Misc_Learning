import random
import numpy as np
import time

class Point:
    def __init__(self,x,y,key):
        self.x=x
        self.y=y
        self.key=key

    def __str__(self):
        """Returns a string containing instance information."""
        f = lambda n: int(n)
        return str(self.key) + ',\t' + str(f(self.x)) + ',\t' + str(f(self.y))

def generate_points(num_of_points):

    graph_list=[]
    point_num=0

    while point_num < num_of_points:
        point_info=(random.randint(0, 100), random.randint(0, 100))
        while point_info not in graph_list:
            graph_list.append(point_info)
            point_num+=1

    graph=[Point(point_info[0], point_info[1], str(point_idx)) \
           for point_idx, point_info in enumerate(graph_list)]

    _out=[]
    for point in graph:
        _out.append('\t'.join([str(point.key),str(point.x),str(point.y)]))

    """Prints the output file containing the the points"""
    with open(str(num_of_points)+'.txt', 'wb') as f:
        f.write('\n'.join(_out))

    return graph

def read_input_file(num_of_points):
    """Returns an array of points from the input file.
    Assumes that points will be floats.
    """
    graph = []
    with open(str(num_of_points)+'.txt', 'r') as f:
        for line in f:
            key, x, y = line.split('\t')
            graph.append(Point(float(x), float(y), key))

    return graph

def sort_points(graph):
    """Return graph sorted by leftmost first, then by slope, ascending."""

    def slope(a):
        """returns the slope of the 2 points."""
        return (graph[0].y - y.y) / (graph[0].x - y.x)

    def polar(a, b):
        if ((a.x - graph[0].x) * (b.y - graph[0].y) - (b.x - graph[0].x) * (a.y - graph[0].y) == 0):
            return a.x < b.x
        else:
            return (a.x - graph[0].x) * (b.y - graph[0].y) - (b.x - graph[0].x) * (a.y - graph[0].y) > 0

    graph.sort()  # put leftmost first
    graph = graph[:1] + sorted(graph[1:], cmp=polar)
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
        while len(convex_hull) > 1 and cross_product(convex_hull[-2], convex_hull[-1], p) >= 0:
            convex_hull.pop()
        convex_hull.append(p)
    elapsed = (time.clock() - start)
    print("graham_scan time used:%s"%(elapsed))

    return convex_hull

if __name__=="__main__":
    graph=generate_points(1000)
    # for point in graph:
    #     print point

    # graph=read_input_file(10)
    # for point in graph:
    #     print point

    # for point in sort_points(graph):
    #     print point

    graham_scan(graph)

