import pygame
import pygame_gui

import time
from math import sqrt
from graph import Graph, Color
import algorithms


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == visualize_button:
                    visualize_algorithm()

        if event.type == pygame.MOUSEBUTTONUP:
            handle_click()
        
        gui_manager.process_events(event)


def visualize_algorithm():
    if algorithms_dropdown.selected_option == "Dfs":
        print("visualizing dfs")
        print(algorithms.dfs(main_graph, main_graph["A"], main_graph["D"]))
        #algorithms.dfs(main_graph, main_graph[selected_nodes[0]], main_graph[selected_nodes[1]])
        color_entire_graph(main_graph)
    elif algorithms_dropdown.selected_option == "Bfs":
        print("visualizing bfs")
        print(algorithms.bfs(main_graph, [[None, main_graph["A"]]], main_graph["E"]))
    elif algorithms_dropdown.selected_option == "Bovurkas":
        print("visualizing Bovurkas")
        print(algorithms.boruvkas(main_graph))


def refresh(g):
    check_events()
    delta_time = clock.tick(30)/1000
    gui_manager.update(delta_time)
    draw_items(g)


def handle_click():
    pos = pygame.mouse.get_pos()
    for node in main_graph.nodes:
        if calculate_distance(node.position, pos) < 10:
            if len(selected_nodes) == 2:
                selected_nodes.pop()
            selected_nodes.append(node.value)


def calculate_distance(pos1, pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def wait(seconds, g):
    t = 0
    while t < seconds:
        t1 = time.time()
        refresh(g)
        t += time.time()-t1


def draw_items(graph):
    window.fill((255, 255, 255))
    gui_manager.draw_ui(window)

    for edge in graph.edges:
        edge.draw(window, font2)

    for node in graph.nodes:
        node.draw(window, font1)

    pygame.display.flip()


def color_array(array, color):
    for element in array:
        element.color_element(color)


def color_entire_graph(graph, color=Color.BLACK):
    color_array(graph.nodes, color)
    color_array(graph.edges, color)


screen_width = 1000
screen_height = 500

pygame.init()
pygame.display.set_caption("Graph theory")
window = pygame.display.set_mode((screen_width, screen_height))

pygame.font.init()
font1 = pygame.font.SysFont("Comic Sans MS", 25)
font2 = pygame.font.SysFont("Comic Sans MS", 20)

clock = pygame.time.Clock()

gui_manager = pygame_gui.UIManager((screen_width, screen_height))
visualize_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screen_width-120, 100), (100, 50)), text="Visualize", manager=gui_manager)
algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(["Dfs", "Bfs", "Bovurkas"], "Dfs", pygame.Rect((screen_width-120, 50), (100, 30)), gui_manager)
main_graph = Graph()

selected_nodes = []


def main():
    main_graph.random_fill()

    while True:
        refresh(main_graph)


if __name__ == "__main__":
    main()
