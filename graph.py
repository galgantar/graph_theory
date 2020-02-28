import pygame
from random import randint
from math import sqrt


class Edge:
    def __init__(self, first_node, second_node, weight):
        self.first_node = first_node
        self.second_node = second_node
        self.weight = weight

        self.color = (0, 0, 0)
        self.text_pos = None
        self.text_color = (0, 0, 0)

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return (self.first_node == other.first_node and self.second_node == other.second_node) or \
               (self.second_node == other.first_node and self.first_node == other.second_node)

    def __repr__(self):
        return f"({self.first_node}, {self.second_node}): {self.weight}"

    def __hash__(self):
        first, second = self.first_node.value, self.second_node.value
        if second > first:
            first, second = second, first
        return hash(first + second)

    def contains(self, item):
        return self.first_node == item or self.second_node == item

    def calculate_text_pos(self):
        move_constant = 20
        vector = (self.first_node.position[0]-self.second_node.position[0], self.first_node.position[1]-self.second_node.position[1])
        vec_len = sqrt(vector[0]**2+vector[1]**2) + 0.001
        normalized_vec = (vector[0]/vec_len, vector[1]/vec_len)
        perpendicular_vec = (normalized_vec[1], -normalized_vec[0])

        x = (self.first_node.position[0] + self.second_node.position[0]) // 2 + round(move_constant*perpendicular_vec[0])
        y = (self.first_node.position[1] + self.second_node.position[1]) // 2 + round(move_constant*perpendicular_vec[1])
        self.text_pos = x, y

    def draw(self, window, font):
        pygame.draw.line(window, self.color, self.first_node.position, self.second_node.position, 2)

        self.calculate_text_pos()
        font_surface = font.render(str(self.weight), False, self.text_color)
        window.blit(font_surface, (self.text_pos[0]-font_surface.get_width()//2, self.text_pos[1]-font_surface.get_height()//2))

    def color_element(self, color):
        self.color = color


class Node:
    def __init__(self, value, position):
        self.value = value
        self.mark = None

        self.position = position
        self.color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.radius = 5

    def __eq__(self, other):
        if type(other) == int:
            return self.value == other
        elif type(other) == Node:
            return self.value == other.value
        else:
            raise ValueError(f"Invalid comparison of type: {type(other)}")

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)

    def make_mark(self, mark):
        self.mark = mark

    def add_edge(self, edge):
        self.edges.add(edge)

    def color_element(self, color):
        self.color = color

    def draw(self, window):
        pygame.draw.circle(window, self.color, self.position, 7)


class Graph:
    def __init__(self):
        self.edges = set()
        self.nodes = set()

    def __getitem__(self, item):
        for node in self.nodes:
            if node.value == item:
                return node

    def __repr__(self):
        string = "Graph: {\n"
        for n in self.nodes:
            string += f"\tNode {n}: ("
            string += ", ".join(str(e.second_node.value) for e in self.get_edges_from_node(n))
            string += ")\n"
        string += "}"
        return string

    def get_edges_from_node(self, node):
        for e in self.edges:
            if e.first_node == node:
                yield Edge(node, e.second_node, e.weight)
            elif e.second_node == node:
                yield Edge(node, e.first_node, e.weight)

    def get_edge(self, node1, node2):
        for e in self.edges:
            if e.contains(node1) and e.contains(node2):
                return e
        return None

    def add_node(self, position):
        self.nodes.add(Node(len(self.nodes), position))

    def connect_nodes(self, node1, node2, weight=0):
        if Edge(self[node1], self[node2], weight) not in self.edges:
            self.edges.add(Edge(self[node1], self[node2], weight))
            return True

        return False

    def remove_node(self, node):
        self.nodes.remove(node)
        self.edges = set((e for e in self.edges if not e.contains(node)))

    def are_connected(self, node1, node2):
        for e in self.get_edges_from_node(node1):
            if e.second_node == node2:
                return True
        return False

    def cost_of_edge(self, node1, node2):
        e = self.get_edge(node1, node2)
        if not e:
            return 0
        else:
            return e.weight

    @property
    def empty(self):
        return not bool(self.nodes)

    @property
    def order(self):
        return len(self.nodes)

    @property
    def size(self):
        return len(self.edges)

    @property
    def weakly_connected(self):
        start = next(iter(self.nodes))
        next_to_check = [start]
        checked_nodes = set()

        while next_to_check:
            new_check_arr = []
            for node in next_to_check:
                if node.value not in checked_nodes:
                    checked_nodes.add(node)
                    new_check_arr.extend([e.second_node for e in self.get_edges_from_node(node)])
            next_to_check = new_check_arr

        return len(checked_nodes) == self.order

    @property
    def totally_connected(self):
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 is not node2 and not self.are_connected(node1, node2):
                    print(node1, node2, "not connected")
                    print(self)
                    return False
        return True

    def random_fill(self, nr_of_nodes, nr_of_connections, width_range, height_range):
        if nr_of_connections > nr_of_nodes*(nr_of_nodes-1)//2:
            raise ValueError("Number of connections if too big")

        self.nodes.clear()
        self.edges.clear()

        for i in range(nr_of_nodes):
            self.add_node((randint(*width_range), randint(*height_range)))

        while nr_of_connections:
            r1, r2 = 1, 1
            while r1 == r2:
                r1 = randint(0, nr_of_nodes-1)
                r2 = randint(0, nr_of_nodes-1)

            if self.connect_nodes(r1, r2, randint(1, 99)):
                nr_of_connections -= 1
