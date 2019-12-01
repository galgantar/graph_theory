from graph import Graph
from GUI import draw_graph
import algorithms

def main():
    g1 = Graph()
    g1.add_node("A")
    g1.add_node("B")
    g1.add_node("C")
    g1.add_node("D")
    g1.add_node("E")
    g1.connect_nodes("A", "B", 10)
    g1.connect_nodes("A", "D", 10)
    g1.connect_nodes("B", "C", 10)
    g1.connect_nodes("B", "E", 10)
    g1.connect_nodes("C", "D", 10)



    print(algorithms.dfs(g1, "A", "D"))
    # print(bfs(g1, "A", "D"))

    # print(algorithms.boruvkas(g1))
    draw_graph(g1)


if __name__ == "__main__":
    main()
