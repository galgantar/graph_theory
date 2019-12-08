import pygame
from enum import Enum
from random import randint

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    WHITE = 4
    BLACK = 5


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.mark = None

        self.color = (0, 0, 0)
        #self.text_pos = self.calculate_text_pos()
        self.text_color = (0, 0, 0)

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return (self.start_node == other.start_node and self.end_node == other.end_node) or (self.end_node == other.start_node and self.start_node == other.end_node)

    def __repr__(self):
        return self.start_node.value, self.end_node.value

    def make_mark(self, mark):
        self.mark = mark

    """def calculate_text_pos(self):
        move_constant = 50

        line_c = 1 if self.start_pos[0] - self.end_pos[0] == 0 else (self.start_pos[1] - self.end_pos[1]) // (self.start_pos[0] - self.end_pos[0])
        move_c = 1 if line_c > 0 else -1

        x = (self.start_pos[0] + self.end_pos[0]) // 2 + move_constant * move_c
        y = (self.start_pos[1] + self.end_pos[1]) // 2 - move_constant
        return x, y"""

    def draw(self, window, font):
        pygame.draw.line(window, self.color, self.start_node.position, self.end_node.position, 2)
        font_surface = font.render(str(self.weight), False, self.text_color)
        #window.blit(font_surface, (self.text_pos[0]-font_surface.get_width()//2, self.text_pos[1]-font_surface.get_height()//2))

    def color_element(self, color):
        if color == Color.RED:
            new_color = (255, 0, 0)
        elif color == Color.GREEN:
            new_color = (0, 255, 0)
        elif color == Color.BLUE:
            new_color = (0, 0, 255)
        elif color == Color.WHITE:
            new_color = (255, 255, 255)
        elif color == Color.BLACK:
            new_color = (0, 0, 0)

        self.color = new_color
        self.text_color = new_color


class Node:
    def __init__(self, value, position):
        self.edges = []
        self.value = value

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
            raise ValueError("Invalid comparison")

    def __repr__(self):
        return self.value

    def add_edge(self, edge):
        self.edges.append(edge)

    def color_element(self, color):
        if color == Color.RED:
            new_color = (255, 0, 0)
        elif color == Color.GREEN:
            new_color = (0, 255, 0)
        elif color == Color.BLUE:
            new_color = (0, 0, 255)
        elif color == Color.WHITE:
            new_color = (255, 255, 255)
        elif color == Color.BLACK:
            new_color = (0, 0, 0)

        self.color = new_color
        self.text_color = new_color

    def draw(self, window, font):
        pygame.draw.circle(window, self.color, self.position, 20)
        pygame.draw.circle(window, (255, 255, 255), self.position, 18)
        font_surface = font.render(self.value, False, self.text_color)

        window.blit(font_surface, (self.position[0]-font_surface.get_width()//2, self.position[1]-font_surface.get_height()//2))


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
        from random import randint
        self.nodes.append(Node(name, (randint(100, 900), randint(100, 400))))

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        return len(self.edges)

    def connect_nodes(self, node1, node2, weight):
        self[node1].add_edge(Edge(self[node1], self[node2], weight))
        self[node2].add_edge(Edge(self[node2], self[node1], weight))

        if Edge(self[min(node1, node2)], self[max(node1, node2)], weight) not in self.edges:
            self.edges.append(Edge(self[min(node1, node2)], self[max(node1, node2)], weight))

    def pretty_print(self):
        for n in self.nodes:
            print(f"Node {n.value}: ", end="")
            for e in n.edges:
                print(f"({e.start_node.value} {e.end_node.value})", end="")
            print()

    def random_fill(self):
        self.nodes.clear()
        self.edges.clear()

        start = ord("A")
        nr_of_nodes = 10
        nr_of_connections = 15

        for i in range(nr_of_nodes):
            self.add_node(chr(start + i))

        for i in range(nr_of_connections):
            r1, r2 = 1, 1
            while r1 == r2:
                r1 = randint(start, start + nr_of_nodes-1)
                r2 = randint(start, start + nr_of_nodes-1)

            self.connect_nodes(chr(r1), chr(r2), randint(1, 99))
