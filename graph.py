class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.mark = None

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node or self.end_node == other.start_node and self.start_node == other.end_node

    def make_mark(self, mark):
        self.mark = mark


class Node:
    def __init__(self, value):
        self.edges = []
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def add_edge(self, edge):
        self.edges.append(edge)


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []

    def __getitem__(self, item):
        for node in self.nodes:
            if node.value == item:
                return node

    def __contains__(self, item):
        for node in self.nodes:
            if node.value == item:
                return True
        return False

    def add_node(self, name):
        self.nodes.append(Node(name))

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        return len(self.edges)

    def connect_nodes(self, node1, node2, weight):
        self[node1].add_edge(Edge(self[node1], self[node2], weight))
        self[node2].add_edge(Edge(self[node2], self[node1], weight))
        self.edges.append(Edge(self[node1], self[node2], weight))
