import pygame
import pygame_gui
from time import time
from math import sqrt

from graph import Color, Graph
import algorithms


class Gui:
    def __init__(self, screen_width, screen_height):
        self.graph = Graph()
        self.graph.random_fill((100, screen_width-300), (50, screen_height-50))
        self.available_algorithms = ["Dfs", "Bfs", "Bovurkas"]
        self.selected_nodes = []
        self.currently_visualizing = False

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Graph theory")

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = pygame.display.set_mode((screen_width, screen_height))

        self.clock = pygame.time.Clock()
        self.font1 = pygame.font.SysFont("Comic Sans MS", 25)
        self.font2 = pygame.font.SysFont("Comic Sans MS", 20)

        self.gui_manager = pygame_gui.UIManager((screen_width, screen_height))
        self.visualize_button = pygame_gui.elements.UIButton(pygame.Rect((self.screen_width-120, 100), (100, 50)), "Visualize", self.gui_manager)
        self.algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(self.available_algorithms, self.available_algorithms[0], pygame.Rect((screen_width - 120, 50), (100, 30)), self.gui_manager)

    def run(self):
        while True:
            self.refresh()

    def refresh(self):
        self.check_events()
        delta_time = self.clock.tick(30) / 1000
        self.gui_manager.update(delta_time)
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

            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_click()

            self.gui_manager.process_events(event)

    def handle_click(self):
        pos = pygame.mouse.get_pos()
        for node in self.graph.nodes:
            if self.calculate_distance(node.position, pos) < 10:
                if len(self.selected_nodes) == 2:
                    self.selected_nodes.pop()
                self.selected_nodes.append(node.value)

    def draw_items(self):
        self.window.fill((255, 255, 255))
        self.gui_manager.draw_ui(self.window)

        for edge in self.graph.edges:
            edge.draw(self.window, self.font2)

        for node in self.graph.nodes:
            node.draw(self.window, self.font1)

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
            algorithms.dfs(self, self.graph["A"], self.graph["D"])
            # algorithms.dfs(main_graph, main_graph[selected_nodes[0]], main_graph[selected_nodes[1]])
            self.color_entire_graph()

        elif algorithm == "Bfs":
            algorithms.bfs(self, [[None, self.graph["A"]]], self.graph["E"])
            self.color_entire_graph()

        elif algorithm == "Bovurkas":
            algorithms.boruvkas(self)
            self.color_entire_graph()

        self.currently_visualizing = False

    def color_entire_graph(self, color=Color.BLACK):
        self.color_array(self.graph.nodes, color)
        self.color_array(self.graph.edges, color)

    @staticmethod
    def calculate_distance(pos1, pos2):
        return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    @staticmethod
    def color_array(array, color):
        for element in array:
            element.color_element(color)
