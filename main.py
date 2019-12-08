import pygame
import pygame_gui

import time
from graph import Graph
import algorithms


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == test_button:
                    print('Hello World!')

        gui_manager.process_events(event)


def refresh():
    check_events()
    delta_time = clock.tick(30)/1000
    gui_manager.update(delta_time)
    draw_items(g1)


def wait(seconds):
    t = 0
    while t < seconds:
        t1 = time.time()
        refresh()
        t += time.time()-t1


def draw_items(graph):
    window.fill((255, 255, 255))
    gui_manager.draw_ui(window)

    for edge in graph.edges:
        edge.draw(window, font2)

    for node in graph.nodes:
        node.draw(window, font1)

    pygame.display.update()


def color_array(array, color):
    for element in array:
        element.color_element(color)


def color_entire_graph(graph, color):
    color_array(graph.nodes, color)
    color_array(graph.edges, color)


screen_width = 1000
screen_height = 500
app_run = True

pygame.init()
pygame.display.set_caption("Graph theory")
window = pygame.display.set_mode((screen_width, screen_height))

pygame.font.init()
font1 = pygame.font.SysFont("Comic Sans MS", 25)
font2 = pygame.font.SysFont("Comic Sans MS", 20)

clock = pygame.time.Clock()

gui_manager = pygame_gui.UIManager((screen_width, screen_height))
test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)), text='Say Hello', manager=gui_manager)
algorithms_dropdown = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(["Gal", "Vid", "Zarja"], "Gal", pygame.Rect((600, 200), (100, 30)), gui_manager)
g1 = Graph()


def main():
    g1.random_fill()

    while True:
        refresh()


if __name__ == "__main__":
    main()
