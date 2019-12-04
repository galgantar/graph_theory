import pygame
import time
from graph import Graph
import algorithms


def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def wait(seconds):
    t = 0
    while t < seconds:
        t1 = time.time()
        check_quit()
        time.sleep(0.001)
        t += time.time()-t1


def refresh(graph):
    check_quit()
    window.fill((255, 255, 255))

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

window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Graph theory")

pygame.font.init()
font1 = pygame.font.SysFont("Comic Sans MS", 25)
font2 = pygame.font.SysFont("Comic Sans MS", 20)


def main():
    g1 = Graph()
    g1.add_node("A")
    g1.add_node("B")
    g1.add_node("C")
    g1.add_node("D")
    g1.add_node("E")
    g1.add_node("F")
    g1.add_node("G")
    g1.add_node("H")
    g1.connect_nodes("A", "B", 10)
    g1.connect_nodes("B", "E", 10)
    g1.connect_nodes("C", "G", 10)
    g1.connect_nodes("A", "H", 10)
    g1.connect_nodes("H", "G", 10)
    g1.connect_nodes("F", "G", 10)
    g1.connect_nodes("G", "F", 10)

    print(algorithms.bfs(g1, [g1["A"]], g1["D"]))
    #print([x.value for x in algorithms.bfs(g1, [g1["A"]], g1["D"])])


if __name__ == "__main__":
    main()
