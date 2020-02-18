import pygame
import pygame_gui

from time import time
from math import sqrt
import pickle

from graph import Color, Graph
import algorithms


class Gui:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graph = Graph()
        self.nr_of_nodes = 20
        self.nr_of_edges = 30
        #self.graph.random_fill(self.nr_of_nodes, self.nr_of_edges, (100, self.screen_width-300), (50, self.screen_height-50))

        self.selected_nodes = []
        self.currently_visualizing = False
        self.moving_node = None
        self.prev_click_backspace = None
        self.prev_click_left_mouse = 0

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Graph theory")

        self.window = pygame.display.set_mode(size=(screen_width, screen_height))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(name="Gill Sans Nova", size=25)

        self.gui_manager = pygame_gui.UIManager(window_resolution=(screen_width, screen_height))
        self.visualize_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width-120, 100), (100, 50)), text="Visualize", manager=self.gui_manager)

        self.load_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 120, 250), (100, 50)), text="Load",
            manager=self.gui_manager)

        self.available_algorithms = ["Dfs", "Bfs", "Boruvkas", "Prims", "Color", "TSP"]
        self.algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=self.available_algorithms, starting_option=self.available_algorithms[0],
            relative_rect=pygame.Rect((screen_width - 120, 50), (100, 30)), manager=self.gui_manager)

        self.loadable_graphs = ["Tree"]
        self.load_graphs_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=self.loadable_graphs, starting_option=self.loadable_graphs[0],
            relative_rect=pygame.Rect((screen_width - 120, 200), (100, 30)), manager=self.gui_manager)

        self.reset_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width-120, 400), (100, 50)), text="Reset graph", manager=self.gui_manager)

    def run(self):
        while True:
            self.refresh()

    def refresh(self):
        self.check_events()
        delta_time = self.clock.tick(30) / 1000
        self.handle_mouse()
        self.handle_keys()
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

            if event.type == pygame.USEREVENT and event.user_type == "ui_button_pressed":
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

                elif event.ui_element == self.load_graph_button:
                    self.save_graph_to_a_file("tree.pkl")
                    self.load_graph_from_a_file("tree.pkl")


            self.gui_manager.process_events(event)

    def handle_mouse(self):
        left, middle, right = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if right and time() - self.prev_click_left_mouse > 0.5:
            for node in self.graph.nodes:
                if self.calculate_distance(node.position, mouse_pos) < 10:
                    if node.value not in self.selected_nodes:
                        if len(self.selected_nodes) == 2:
                            self.selected_nodes.pop(0)
                        self.selected_nodes.append(node)

                    else:
                        self.selected_nodes.remove(node)

                self.prev_click_left_mouse = time()

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

        if middle:
            for node in self.graph.nodes:
                if self.calculate_distance(node.position, mouse_pos) < 10:
                    self.graph.remove_node(node)
                    break

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if not self.prev_click_backspace or time() - self.prev_click_backspace > 0.5:
                self.graph.add_node(pygame.mouse.get_pos())
                self.prev_click_backspace = time()

        if keys[pygame.K_SPACE] and len(self.selected_nodes) == 2:
            self.graph.connect_nodes(self.selected_nodes[0], self.selected_nodes[1], 10)
            self.selected_nodes = []

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
        it = iter(self.graph.nodes)

        if algorithm == "Dfs":
            if self.selected_nodes:
                algorithms.dfs(self, self.selected_nodes[0])
            else:
                algorithms.dfs(self, next(it))

        elif algorithm == "Bfs":
            if self.selected_nodes:
                algorithms.bfs(self, self.selected_nodes[0])
            else:
                algorithms.bfs(self, next(it))

        elif algorithm == "Boruvkas":
            print(algorithms.boruvkas(self))

        elif algorithm == "Prims":
            print(algorithms.prims(self))

        elif algorithm == "Color":
            algorithms.color_graph(self)

        elif algorithm == "TSP":
            start = next(it)
            print(algorithms.TSP(self, start, start, self.graph.nodes))

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

    def save_graph_to_a_file(self, filename):
        with open(f"saved_graphs/{filename}", "wb") as file:
            pickle.dump(self.graph, file)

    def load_graph_from_a_file(self, filename):
        with open(f"saved_graphs/{filename}", "rb") as file:
            self.graph = pickle.load(file)
