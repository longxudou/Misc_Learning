import random
import numpy as np
import time
import matplotlib
import sys
from math import atan2


class Point:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key

    def __str__(self):
        """Returns a string containing instance information."""
        f = lambda n: int(n)
        # return str(self.key) + ',\t' + str(f(self.x)) + ',\t' + str(f(self.y))
        return str(self.key)


def generate_points(num_of_points):
    start = time.clock()

    graph_list = []
    point_num = 0

    x_list = []
    y_list = []
    while point_num < num_of_points:
        x_info = random.randint(0, 10000)
        y_info = random.randint(0, 10000)
        # if x_info not in x_list and y_info not in y_list:
        if (x_info, y_info) not in graph_list:
            graph_list.append((x_info, y_info))
            # x_list.append(x_info)
            # y_list.append(y_info)
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

    def compare_position(a, b):
        if a.y != b.y:
            return a.y - b.y
        else:
            return a.x - b.x

    def length2(a, b):
        return (a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)

    def slope_with_distance(a,b):
        """returns the slope of the 2 points."""
        angle_a=atan2(graph[0].x - a.x, a.y - graph[0].y)
        angle_b=atan2(graph[0].x - b.x, b.y - graph[0].y)

        if angle_a!=angle_b:
            return int(angle_a-angle_b+0.5)
        else:
            return length2(graph[0],a)-length2(graph[0],b)

    graph = sorted(graph, cmp=compare_position)  # put leftmost first
    graph = graph[:1] + sorted(graph[1:], key=slope)
    return graph


def graham_scan(graph):
    """Takes an array of points to be scanned.
    Returns an array of points that make up the convex hull surrounding the points passed in in graph.
    """
    # OA x OB
    # greater than 0 -> counterclockwise from OA->OB
    def cross_product(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)

    # convex_hull is a stack of points beginning with the leftmost point.
    convex_hull = []
    sorted_points = sort_points(graph)

    for p in sorted_points:
        while len(convex_hull) > 1 and cross_product(convex_hull[-2], convex_hull[-1], p) < 0:
            convex_hull.pop()
        convex_hull.append(p)

    convex_hull_key_list = []
    for point in convex_hull:
        convex_hull_key_list.append(point.key)

    return convex_hull, sorted(convex_hull_key_list, key=lambda x:int(x))


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

    convex_hull = list(set(convex_hull))

    elapsed = (time.clock() - start)
    print("brute_force time used:%s" % (elapsed))

    convex_hull_key_list = []
    for point in convex_hull:
        convex_hull_key_list.append(point.key)

    return convex_hull, sorted(convex_hull_key_list)


def brute_force2(graph):
    start = time.clock()

    def compare_position(a, b):
        if a.y != b.y:
            return a.y - b.y
        else:
            return a.x - b.x
    graph = sorted(graph, cmp=compare_position)  # put leftmost first
    # convex_hull is a stack of points beginning with the leftmost point.
    no_convex_hull = []

    def cross_product(a, b, c):
        value = a.x * b.y + c.x * a.y + b.x * c.y - c.x * b.y - b.x * a.y - a.x * c.y
        return np.sign(value)

    def isPointInTriangle(p0,point1,point2,point3):
        return cross_product(p0, point1, point3) * cross_product(p0, point1, point2) > 0 and \
        cross_product(p0, point2, point3) * cross_product(p0, point2, point1) > 0 and \
        cross_product(point1, point2, point3) * cross_product(point1, point2, p0) > 0 and \
               cross_product(p0, point1, point2)!= 0 and \
               cross_product(p0, point2, point1)!=0 and \
               cross_product(point1, point2, p0) !=0

    p0=graph[0]
    # print 'graph0',p0
    for point1_idx in range(1,len(graph)-2):
        point1=graph[point1_idx]
        for point2_idx in range(point1_idx+1,len(graph)-1):
            point2=graph[point2_idx]
            for point3_idx in range(point2_idx+1,len(graph)):
                point3=graph[point3_idx]
                if isPointInTriangle(p0,point1,point2,point3):
                    no_convex_hull.append(point3)
                if isPointInTriangle(p0,point1,point3,point2):
                    no_convex_hull.append(point2)
                if isPointInTriangle(p0,point3,point2,point1):
                    no_convex_hull.append(point1)

    convex_hull = list(set(graph)-set(no_convex_hull))
    elapsed = (time.clock() - start)
    print("brute_force time used:%s" % (elapsed))
    convex_hull_key_list = []
    for point in convex_hull:
        convex_hull_key_list.append(point.key)
    return convex_hull, sorted(convex_hull_key_list, key=lambda x:int(x))

MinYPoint,PolePoint=Point(0,0,0),Point(0,0,0)

def divide_conquer(graph):
    def cross_product(o, a, b):
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
    def getPolePoint(graph):
        ConvexHull_points, _=graham_scan(graph)
        # print 'ConvexHull_Points--', [i.key for i in ConvexHull_points]
        for point in graph:
            if point not in ConvexHull_points:
                return point
    def getMinYPoint(graph):
        min_point=graph[0]
        min_point_idx = 0
        min_point_y = min_point.y
        for point_idx in range(len(graph[1:])):
            point=graph[point_idx]
            if point.y<min_point_y:
                min_point_idx=point_idx
                min_point_y=point.y
                min_point=point
        return point, min_point_idx
    def getMaxYPoint(graph):
        max_point=graph[0]
        max_point_idx = 0
        max_point_y = max_point.y
        for point_idx in range(len(graph[1:])):
            point=graph[point_idx]
            if point.y<max_point_y:
                max_point_idx=point_idx
                max_point_y=point.y
                max_point=point
        return point, max_point_idx
    def TwowayMergeSort(left_ConvexHull_points, right_ConvexHull_points):
        return list(set(left_ConvexHull_points + right_ConvexHull_points))
    def TwowayMergeSort2(left_ConvexHull_points,right_ConvexHull_points):
        n1=len(left_ConvexHull_points)
        n2=len(right_ConvexHull_points)

        Left_Max_Point, Left_Max_Point_idx =getMaxYPoint(left_ConvexHull_points)
        Right_Min_Point, Right_Min_Point_idx=getMinYPoint(right_ConvexHull_points)

        print Left_Max_Point.key,Left_Max_Point_idx
        print Right_Min_Point.key,Right_Min_Point_idx
        #finding the upper tangent
        inda=Left_Max_Point_idx
        indb=Right_Min_Point_idx
        Done=False

        while not Done:
            Done = True
            while cross_product(right_ConvexHull_points[indb],left_ConvexHull_points[inda],left_ConvexHull_points[(inda+1)%n1])>=0:
                inda = (inda+1)%n1

            while cross_product(left_ConvexHull_points[inda],right_ConvexHull_points[indb],right_ConvexHull_points[(n2+indb-1)%n2])<=0:
                indb = (n2+indb-1)%n2
                Done=False

        upper_left=inda
        upper_right=indb


        #finding the lowest tangent
        inda=Left_Max_Point_idx
        indb=Right_Min_Point_idx
        Done=False
        while not Done:
            Done = True
            while cross_product(left_ConvexHull_points[inda],right_ConvexHull_points[indb],right_ConvexHull_points[(indb+1)%n2])>=0:
                indb = (indb + 1) % n2
            while cross_product(right_ConvexHull_points[indb],left_ConvexHull_points[inda],left_ConvexHull_points[(n1+inda-1)%n1])<=0:
                inda = (n1+inda - 1) % n1
                Done=True

        lower_left=inda
        lower_right=indb

        print upper_right,lower_right,upper_left,lower_left
        # ret=[]
        # ind=upper_left
        # ret.append(left_ConvexHull_points[ind])
        # while ind!=lower_left:
        #     ind = (ind+1) % n1
        #     ret.append(left_ConvexHull_points[ind])
        #
        # ind=lower_right
        # ret.append(left_ConvexHull_points[ind])
        # while ind!=upper_right:
        #     ind = (ind+1) % n1
        #     ret.append(left_ConvexHull_points[ind])

        return list(set(left_ConvexHull_points+right_ConvexHull_points))
    #bound
    if len(graph) <= 3:
        return graph

    #divide
    left_candidata_points = graph[:len(graph)/2]
    right_candidata_points = graph[len(graph)/2:]

    #solve
    if len(left_candidata_points)!=0 and len(right_candidata_points)!=0:
        left_ConvexHull_points = divide_conquer(left_candidata_points)
        right_ConvexHull_points = divide_conquer(right_candidata_points)

    #conquer
    g_graph, g_graph_list = graham_scan(TwowayMergeSort(left_ConvexHull_points,right_ConvexHull_points))
    return g_graph

if __name__ == "__main__":
    for num_points in [100,200,300,400,500]:
        # graph = generate_points(num_points)

        print '\n----num of points:%s----'%(num_points)
        graph = read_input_file(num_points)


        start = time.clock()

        #sorting the set of points according to the x-coordinate

        graph=sorted(graph,key=lambda p:p.x)
        d_graph=divide_conquer(graph)
        elapsed = (time.clock() - start)
        print("divide_conquer time used:%s" % (elapsed))

        d_graph_list = []
        for point in d_graph:
            d_graph_list.append(point.key)
        d_graph_list=sorted(d_graph_list, key=lambda x:int(x))

        # sort_points(graph)
        # for point in sort_points(graph):
        #     print point

        start = time.clock()
        g_graph, g_graph_list = graham_scan(graph)
        elapsed = (time.clock() - start)
        print("graham_scan time used:%s" % (elapsed))
        b_graph, b_graph_list = brute_force2(graph)
    #
    # print g_graph_list
    #
    # print b_graph_list
    # print d_graph_list
    #
    # print g_graph_list == d_graph_list
    #
    #
    # print g_graph_list == b_graph_list == d_graph_list
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
