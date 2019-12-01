import pygame
from math import sqrt

from graph import Node
from graph import Edge


class DrawableNode(Node):
    def __init__(self, value, position: tuple):
        Node.__init__(self, value)

        self.position = position
        self.color = (0, 0, 0)
        self.text_color = (0, 0, 0)
        self.radius = 5

    def color_red(self):
        self.color = (255, 0, 0)
        self.text_color = (255, 0, 0)

    def color_green(self):
        self.color = (0, 255, 0)
        self.text_color = (0, 255, 0)

    def color_black(self):
        self.color = (0, 0, 0)
        self.text_color = (0, 0, 0)

    def draw(self, window, font):
        pygame.draw.circle(window, self.color, self.position, 20)
        pygame.draw.circle(window, (255, 255, 255), self.position, 18)
        font_surface = font.render(self.value, False, self.text_color)

        window.blit(font_surface, (self.position[0]-font_surface.get_width()//2, self.position[1]-font_surface.get_height()//2))


class DrawableEdge(Edge):
    def __init__(self, start_node: Node, end_node: Node, weight : int, start_pos: tuple, end_pos: tuple):

        Edge.__init__(self, start_node, end_node, weight)

        self.color = (0, 0, 0)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.text_pos = self.calculate_text_pos()
        self.text_color = (0, 0, 0)

    def calculate_text_pos(self):
        move_constant = 50

        line_c = 1 if self.start_pos[0] - self.end_pos[0] == 0 else (self.start_pos[1] - self.end_pos[1]) // (self.start_pos[0] - self.end_pos[0])
        move_c = 1 if line_c > 0 else -1

        x = (self.start_pos[0] + self.end_pos[0]) // 2 + move_constant * move_c
        y = (self.start_pos[1] + self.end_pos[1]) // 2 - move_constant
        return x, y

    def draw(self, window, font):
        pygame.draw.line(window, self.color, self.start_pos, self.end_pos, 2)
        font_surface = font.render(str(self.weight), False, self.text_color)
        window.blit(font_surface, (self.text_pos[0]-font_surface.get_width()//2, self.text_pos[1]-font_surface.get_height()//2))


def normalize_vector(x, y):
    length = sqrt(x**2 + y**2)
    return x/length, y/length


def make_drawable(graph):
    from random import randint
    drawable_nodes = []
    drawable_edges = []
    l = []

    for node in graph.nodes:
        drawable_nodes.append(DrawableNode(node.value, (randint(100,900), randint(100,400))))
        l.append(node.value)
    for edge in graph.edges:
        drawable_edges.append(DrawableEdge(edge.start_node, edge.end_node, edge.weight, drawable_nodes[l.index(edge.start_node.value)].position, drawable_nodes[l.index(edge.end_node.value)].position))

    return drawable_nodes, drawable_edges


def draw_graph(graph):
    screen_width = 1000
    screen_height = 500
    gui_on = True

    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Graph theory")

    pygame.font.init()
    node_font = pygame.font.SysFont("Comic Sans MS", 25)
    edge_weight_font = pygame.font.SysFont("Comic Sans MS", 20)

    drawable_nodes, drawable_edges = make_drawable(graph)

    while gui_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gui_on = False

        window.fill((255,255,255))

        for edge in drawable_edges:
            edge.draw(window, edge_weight_font)

        for node in drawable_nodes:
            node.draw(window, node_font)

        pygame.display.update()

    pygame.quit()
    exit()
