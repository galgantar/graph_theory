import pygame
from random import randint
from math import sqrt
from itertools import count


class Color:
    NONE = None
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    available_colors = [RED, GREEN, BLUE, YELLOW]

    @staticmethod
    def infinite_generator():
        for i in count():
            yield Color.available_colors[i] if i < len(Color.available_colors) else Color.generate_random_color()

    @staticmethod
    def finite_generator(limit):
        for i in range(limit):
            yield Color.available_colors[i] if i < len(Color.available_colors) else Color.generate_random_color()

    @staticmethod
    def generate_random_color():
        return randint(30, 255), randint(30, 255), randint(30, 255)


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

        self.color = (0, 0, 0)
        self.text_pos = None
        self.text_color = (0, 0, 0)

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return (self.start_node == other.start_node and self.end_node == other.end_node) or \
               (self.end_node == other.start_node and self.start_node == other.end_node)

    def __repr__(self):
        return f"({self.start_node}, {self.end_node}): {self.weight}"

    def __hash__(self):
        first, second = self.start_node.value, self.end_node.value
        if second > first:
            first, second = second, first
        return hash(first + second)

    def calculate_text_pos(self):
        move_constant = 20
        vector = (self.start_node.position[0]-self.end_node.position[0], self.start_node.position[1]-self.end_node.position[1])
        vec_len = sqrt(vector[0]**2+vector[1]**2)
        normalized_vec = (vector[0]/vec_len, vector[1]/vec_len)
        perpendicular_vec = (normalized_vec[1], -normalized_vec[0])

        x = (self.start_node.position[0] + self.end_node.position[0]) // 2 + round(move_constant*perpendicular_vec[0])
        y = (self.start_node.position[1] + self.end_node.position[1]) // 2 + round(move_constant*perpendicular_vec[1])
        self.text_pos = x, y

    def draw(self, window, font):
        pygame.draw.line(window, self.color, self.start_node.position, self.end_node.position, 2)

        self.calculate_text_pos()
        font_surface = font.render(str(self.weight), False, self.text_color)
        window.blit(font_surface, (self.text_pos[0]-font_surface.get_width()//2, self.text_pos[1]-font_surface.get_height()//2))

    def color_element(self, color):
        self.color = color


class Node:
    def __init__(self, value, position):
        self.edges = set()
        self.value = value
        self.mark = None

        self.position = position
        self.color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.radius = 5

    def __eq__(self, other):
        if type(other) == str:
            return self.value == other
        elif type(other) == Node:
            return self.value == other.value
        else:
            raise ValueError(f"Invalid comparison of type: {type(other)}")

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return self.value

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
            string += ", ".join(e.end_node.value for e in n.edges)
            string += ")\n"
        string += "}"
        return string

    def add_node(self, name, position):
        self.nodes.add(Node(name, position))

    @property
    def order(self):
        return len(self.nodes)

    @property
    def size(self):
        return len(self.edges)

    @property
    def weakly_connected(self):
        start = next(iter(self.nodes))
        next_to_check = [e.end_node for e in start.edges]
        checked_nodes = set()

        while next_to_check:
            new_check_arr = []
            for node in next_to_check:
                if node.value not in checked_nodes:
                    checked_nodes.add(node)
                    new_check_arr.extend([e.end_node for e in node.edges])
            next_to_check = new_check_arr

        return len(checked_nodes) == self.order

    @property
    def strongly_connected(self):
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 is not node2 and (min(node1, node2), max(node1, node2)) not in [(e.start_node, e.end_node) for e in self.edges]:
                    return False
        return True

    def connect_nodes(self, node1, node2, weight):
        self[node1].add_edge(Edge(self[node1], self[node2], weight))
        self[node2].add_edge(Edge(self[node2], self[node1], weight))

        if Edge(self[min(node1, node2)], self[max(node1, node2)], weight) not in self.edges:
            self.edges.add(Edge(self[min(node1, node2)], self[max(node1, node2)], weight))

    def random_fill(self, nr_of_nodes, nr_of_connections, width_range, height_range):
        self.nodes.clear()
        self.edges.clear()

        start = ord("A")
        for i in range(nr_of_nodes):
            self.add_node(chr(start + i), (randint(*width_range), randint(*height_range)))

        for i in range(nr_of_connections):
            r1, r2 = 1, 1
            while r1 == r2:
                r1 = randint(start, start + nr_of_nodes-1)
                r2 = randint(start, start + nr_of_nodes-1)

            self.connect_nodes(chr(r1), chr(r2), randint(1, 99))
