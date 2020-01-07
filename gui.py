import pygame
import pygame_gui

from time import time
from math import sqrt

from graph import Color, Graph
import algorithms


class Gui:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graph = Graph()
        self.nr_of_nodes = 20
        self.nr_of_edges = 30

        self.graph.random_fill(self.nr_of_nodes, self.nr_of_edges, (100, self.screen_width-300), (50, self.screen_height-50))

        self.available_algorithms = ["Dfs", "Bfs", "Boruvkas", "Prims", "Color"]
        self.selected_nodes = []
        self.currently_visualizing = False
        self.moving_node = None

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Graph theory")

        self.window = pygame.display.set_mode(size=(screen_width, screen_height))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(name="Gill Sans Nova", size=25)

        self.gui_manager = pygame_gui.UIManager(window_resolution=(screen_width, screen_height))
        self.visualize_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width-120, 100), (100, 50)), text="Visualize", manager=self.gui_manager)

        self.algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=self.available_algorithms, starting_option=self.available_algorithms[0],
            relative_rect=pygame.Rect((screen_width - 120, 50), (100, 30)), manager=self.gui_manager)

        self.reset_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width-120, 400), (100, 50)), text="Reset graph", manager=self.gui_manager)

    def run(self):
        while True:
            self.refresh()

    def refresh(self):
        self.check_events()
        delta_time = self.clock.tick(30) / 1000
        self.gui_manager.update(delta_time)

        if not self.currently_visualizing:
            self.color_entire_graph()
            for node in self.graph.nodes:
                if node.value in self.selected_nodes:
                    node.color_element(Color.BLUE)
        self.draw_items()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == 'ui_button_pressed':
                    if event.ui_element == self.visualize_button:
                        if not self.currently_visualizing:
                            self.visualize_algorithm(self.algorithms_dropdown.selected_option)
                        else:
                            print("Already visualizing")

                    elif event.ui_element == self.reset_graph_button:
                        if not self.currently_visualizing:
                            self.graph.random_fill(self.nr_of_nodes, self.nr_of_edges, (100, self.screen_width - 300), (50, self.screen_height - 50))
                        else:
                            print("Cannot reset graph")

            self.gui_manager.process_events(event)
        self.handle_mouse()

    def handle_mouse(self):
        left, middle, right = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if right:
            for node in self.graph.nodes:
                if self.calculate_distance(node.position, mouse_pos) < 10:
                    if node.value not in self.selected_nodes:
                        if len(self.selected_nodes) == 2:
                            self.selected_nodes.pop(0)
                        self.selected_nodes.append(node.value)

        if left:
            if not self.moving_node:
                for node in self.graph.nodes:
                    if self.calculate_distance(node.position, mouse_pos) < 10:
                        self.moving_node = node
                        pygame.mouse.get_rel()
            else:
                pos_change = pygame.mouse.get_rel()
                self.moving_node.position = self.moving_node.position[0]+pos_change[0], self.moving_node.position[1]+pos_change[1]

        else:
            self.moving_node = None

    def draw_items(self):
        self.window.fill((255, 255, 255))
        self.gui_manager.draw_ui(self.window)

        for edge in self.graph.edges:
            edge.draw(self.window, self.font)

        for node in self.graph.nodes:
            node.draw(self.window)

        pygame.display.update()

    def wait(self, seconds):
        t = 0
        while t < seconds:
            t1 = time()
            self.refresh()
            t += time() - t1

    def visualize_algorithm(self, algorithm):
        self.currently_visualizing = True

        if algorithm == "Dfs":
            if len(self.selected_nodes) == 2:
                algorithms.dfs(self, self.graph[self.selected_nodes[0]], self.graph[self.selected_nodes[1]])
            else:
                algorithms.dfs(self, self.graph.nodes[0], self.graph.nodes[-1])

        elif algorithm == "Bfs":
            if len(self.selected_nodes) == 2:
                algorithms.bfs(self, [(None, self.graph[self.selected_nodes[0]])], self.graph[self.selected_nodes[1]])
            else:
                algorithms.bfs(self, [(None, self.graph.nodes[0])], self.graph.nodes[-1])

        elif algorithm == "Boruvkas":
            print(algorithms.boruvkas(self))

        elif algorithm == "Prims":
            print(algorithms.prims(self))

        elif algorithm == "Color":
            algorithms.color_graph(self)

        self.color_entire_graph()
        self.currently_visualizing = False

    def color_entire_graph(self, color=Color.BLACK):
        self.color_array(self.graph.nodes, color)
        self.color_array(self.graph.edges, color)

    @staticmethod
    def color_array(array, color):
        for element in array:
            element.color_element(color)

    @staticmethod
    def calculate_distance(pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
