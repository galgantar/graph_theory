import pygame
import pygame_gui

from time import time
from math import sqrt
import pickle
import os
from collections import namedtuple

from graph import Graph
from color import Color
import algorithms


class CustomDropdown(pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu):
    def __init__(self, screen_width, screen_height, rect, options, starting_option, saved_manager):
        self.saved_manager = saved_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bottom_rect = rect

        super().__init__(options, starting_option, rect, self.saved_manager)

    def rebuild(self, new_options_list):
        super().kill()
        super().__init__(new_options_list, new_options_list[0], self.bottom_rect, self.saved_manager)


class Gui:
    def __init__(self, screen_width, screen_height):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.graph = Graph()
        self.nr_of_nodes = 20
        self.nr_of_edges = 30

        self.selected_nodes = []
        self.currently_visualizing = False
        self.moving_node = None
        self.prev_click_tab = None
        self.prev_click_left_mouse = 0
        self.currently_weighting_edge = None

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Graph theory")

        self.window = pygame.display.set_mode(size=(screen_width, screen_height))

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(name="Gill Sans Nova", size=25)

        self.initialize_gui_elements()

    def initialize_gui_elements(self):
        C = namedtuple('C', ["a", "b", "c"])  # representing color with pygame_gui interface
        
        self.gui_manager = pygame_gui.UIManager(window_resolution=(self.screen_width, self.screen_height))
        self.visualize_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 275, 230), (100, 50)), text="Visualize!",
            manager=self.gui_manager)

        self.available_algorithms = ["Dfs", "Bfs", "Boruvkas", "Prims", "Color", "TSP"]
        self.algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=self.available_algorithms, starting_option=self.available_algorithms[0],
            relative_rect=pygame.Rect((self.screen_width - 275, 200), (100, 30)), manager=self.gui_manager)

        self.loadable_graphs = self.list_loadable_graphs()
        starting_option = self.loadable_graphs[0] if self.loadable_graphs else " "
        self.load_graphs_dropdown = CustomDropdown(self.screen_width, self.screen_height, pygame.Rect((self.screen_width - 120, 200), (100, 30)),
                                                   self.loadable_graphs, starting_option, self.gui_manager)

        self.load_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 120, 230), (100, 40)), text="Uvozi",
            manager=self.gui_manager)

        self.save_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 120, 270), (100, 40)), text="Izvozi",
            manager=self.gui_manager)

        self.reset_graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 120, 370), (100, 50)), text="Generiraj!",
            manager=self.gui_manager)

        self.weight_input = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect((self.screen_width - 275, 370), (100, 50)), manager=self.gui_manager)

        self.desc_label = pygame_gui.elements.ui_text_box.UITextBox(
            relative_rect=pygame.Rect((self.screen_width - 275, 10), (250, 130)), html_text=
            """<b>Vizualizator grafov</b> by Gal Gantar\
                kontrole: TAB; ENTER; MIDDLE, LEFT, RIGTH MOUSE\
            """,
            manager=self.gui_manager)

        self.prev_nodes, self.prev_edges = None, None

        self.node_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 280, 470), (132, 20)), text="VOZLIŠČA:", manager=self.gui_manager)
        self.edge_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 280, 500), (132, 20)), text="POVEZAVE:", manager=self.gui_manager)

        self.label1 = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 275, 180), (100, 20)), text="ALGORITMI:", manager=self.gui_manager)
        self.label2 = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 120, 180), (100, 20)), text="UVOZI GRAF:", manager=self.gui_manager)
        self.label3 = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 275, 350), (100, 20)), text="NOVA UTEŽ:", manager=self.gui_manager)
        self.label4 = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((self.screen_width - 130, 350), (130, 20)), text="NAKLJUČNI GRAF:", manager=self.gui_manager)

        self.label1.bg_colour, self.label1.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.label2.bg_colour, self.label2.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.label3.bg_colour, self.label3.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.label4.bg_colour, self.label4.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.node_label.bg_colour, self.node_label.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.edge_label.bg_colour, self.edge_label.text_colour = C(100, 100, 100), C(255, 255, 255)
        self.label1.rebuild()
        self.label2.rebuild()
        self.label3.rebuild()
        self.label4.rebuild()
        self.node_label.rebuild()
        self.edge_label.rebuild()

    def run(self):
        while True:
            self.refresh()

    def refresh(self):
        self.check_events()
        delta_time = self.clock.tick(30) / 1000
        self.handle_mouse()
        self.handle_keys()
        self.update_menus()
        self.update_graph_data()
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
                        self.graph.random_fill(self.nr_of_nodes, self.nr_of_edges, (30, self.screen_width - 400), (30, self.screen_height - 30))
                    else:
                        print("Cannot reset graph")

                elif event.ui_element == self.save_graph_button:
                    self.save_custom_graph()

                elif event.ui_element == self.load_graph_button:
                    try:
                        self.load_graph_from_a_file(f"{self.load_graphs_dropdown.selected_option}.pkl")
                        self.selected_nodes.clear()
                    except FileNotFoundError:
                        pass

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

                    break

            for edge in self.graph.edges:
                if self.calculate_distance(edge.text_pos, mouse_pos) < 20:
                    self.currently_weighting_edge = edge
                    self.weight_input.set_text(str(edge.weight))
                    break

            self.prev_click_left_mouse = time()

        if left:
            if not self.moving_node:
                for node in self.graph.nodes:
                    if self.calculate_distance(node.position, mouse_pos) < 10:
                        self.moving_node = node
                        pygame.mouse.get_rel()
            else:
                pos_change = pygame.mouse.get_rel()

                if self.moving_node.position[0]+pos_change[0] < self.screen_width - 320:
                    self.moving_node.position = self.moving_node.position[0]+pos_change[0], self.moving_node.position[1]

                self.moving_node.position = self.moving_node.position[0], self.moving_node.position[1]+pos_change[1]

        else:
            self.moving_node = None

        if middle:
            for node in self.graph.nodes:
                if self.calculate_distance(node.position, mouse_pos) < 10:
                    self.graph.remove_node(node)
                    break

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            mouse_pos = pygame.mouse.get_pos()
            if (not self.prev_click_tab or time() - self.prev_click_tab > 0.5) and mouse_pos[0] < self.screen_width-300:
                self.graph.add_node(mouse_pos)
                self.prev_click_tab = time()

        if keys[pygame.K_SPACE] and len(self.selected_nodes) == 2:
            self.graph.connect_nodes(self.selected_nodes[0], self.selected_nodes[1], 10)
            self.selected_nodes = []

        if keys[pygame.K_RETURN] and self.currently_weighting_edge:
            try:
                self.currently_weighting_edge.weight = abs(int(self.weight_input.get_text()))
                self.currently_weighting_edge = None

            except ValueError:
                pass

    def draw_items(self):
        self.window.fill((255, 255, 255))
        pygame.draw.rect(self.window, (100, 100, 100), (self.screen_width-300, 0, 300, self.screen_height))
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

    def update_menus(self):
        new_loadable_graphs = self.list_loadable_graphs()
        if self.loadable_graphs != new_loadable_graphs:
            self.load_graphs_dropdown.rebuild(new_loadable_graphs)
            self.loadable_graphs = new_loadable_graphs

    def update_graph_data(self):
        nodes = self.graph.order
        edges = self.graph.size

        if self.prev_nodes != nodes:
            self.node_label.text = f"VOZLIŠČA: {nodes}"
            self.node_label.rebuild()
            self.prev_nodes = nodes

        if self.prev_edges != edges:
            self.edge_label.text = f"POVEZAVE: {edges}"
            self.edge_label.rebuild()
            self.prev_edges = edges

    def visualize_algorithm(self, algorithm):
        if self.graph.empty: return
        self.currently_visualizing = True
        it = iter(self.graph.nodes)

        if algorithm == "Dfs":
            if self.selected_nodes:
                algorithms.dfs(False, self, self.selected_nodes[0])

            else:
                algorithms.dfs(self, next(it))

        elif algorithm == "Bfs":
            if self.selected_nodes:
                algorithms.bfs(self, self.selected_nodes[0])
            else:
                algorithms.bfs(self, next(it))

        elif algorithm == "Boruvkas":
            algorithms.boruvkas(self)

        elif algorithm == "Prims":
            algorithms.prims(self)

        elif algorithm == "Color":
            self.color_array(self.graph.nodes, Color.NONE)
            algorithms.color_with_min(self)

        elif algorithm == "TSP":
            start = next(it)
            algorithms.TSP(self, start, start, self.graph.nodes.copy())

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

    @staticmethod
    def list_loadable_graphs():
        return list(sorted(f.strip(".pkl") for f in os.listdir("saved_graphs")))

    def save_custom_graph(self):
        custom_graphs = len([name for name in self.list_loadable_graphs() if "custom_" in name])
        with open(f"saved_graphs/custom_{custom_graphs+1}.pkl", "wb") as file:
            pickle.dump(self.graph, file)

    def load_graph_from_a_file(self, filename):
        with open(f"saved_graphs/{filename}", "rb") as file:
            self.graph = pickle.load(file)
