class DisjointSet(dict):
    def __init__(self, dict):
        pass

    def add(self, item):
        self[item] = item

    def find(self, item):
        if self[item] != item:
            self[item] = self.find(self[item])
        return self[item]

    def unionset(self, item1, item2):
        self[item2] = self[item1]


def Kruskal_1(nodes, edges):
    forest = DisjointSet(nodes)
    MST = []
    for item in nodes:
        print(item)
        forest.add(item)
    edges = sorted(edges, key=lambda element: element[2])
    num_sides = len(nodes) - 1
    for e in edges:
        node1, node2, _ = e
        parent1 = forest.find(node1)
        parent2 = forest.find(node2)
        if parent1 != parent2:
            MST.append(e)
            num_sides -= 1
            if num_sides == 0:
                return MST
            else:
                forest.unionset(parent1, parent2)
    pass


def Kruskal(nodes, edges):
    all_nodes = nodes  # set(nodes)
    used_nodes = set()
    MST = []
    edges=sorted(edges,key=lambda element: element[2], reverse=True)
    while used_nodes != all_nodes and edges:
        element = edges.pop(-1)
        if element[0] in used_nodes and element[1] in used_nodes:
            continue
        MST.append(element)
        used_nodes.update(element[:2])
    print(used_nodes)
    return MST


def Kruskal_own(nodes, edges):
    all_nodes=nodes
    used_nodes=set()
    edges=sorted(edges,key=lambda element:element[-1])
    MST=[]

    while(used_nodes!=all_nodes):
        element=edges.pop(0)
        if element[0] in used_nodes and element[1] in used_nodes:
            continue
        MST.append(element)
        used_nodes.update(element[:2])

    print used_nodes
    return MST

def main():
    nodes = set(list('ABCDEFGHI'))
    edges = [("A", "B", 4), ("A", "H", 8),
             ("B", "C", 8), ("B", "H", 11),
             ("C", "D", 7), ("C", "F", 4),
             ("C", "I", 2), ("D", "E", 9),
             ("D", "F", 14), ("E", "F", 10),
             ("F", "G", 2), ("G", "H", 1),
             ("G", "I", 6), ("H", "I", 7)]
    print("\n\nThe undirected graph is :", edges)
    print("\n\nThe minimum spanning tree by Kruskal is : ")
    print(Kruskal(nodes, edges))
    Kruskal_own(nodes, edges)

if __name__ == '__main__':
    main()