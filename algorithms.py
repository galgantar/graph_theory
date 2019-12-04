from graph import Color
from main import wait, refresh, color_array, color_entire_graph


def one_after_another(element1, element2, array):
    if element1 not in array or element2 not in array:
        return False

    return abs(array.index(element1) - array.index(element2)) == 1


def dfs(graph, current, end, path=[]):
    path.append(current)

    color_entire_graph(graph, Color.BLACK)
    color_array([e for e in graph.edges if one_after_another(e.start_node, e.end_node, path)], Color.RED)
    color_array([n for n in graph.nodes if n in path], Color.RED)
    refresh(graph)
    wait(1)

    if current.value == end.value:
        color_entire_graph(graph, Color.BLACK)
        color_array([e for e in graph.edges if one_after_another(e.start_node, e.end_node, path)], Color.GREEN)
        color_array([n for n in graph.nodes if n in path], Color.GREEN)
        refresh(graph)
        wait(5)

        return path

    for e in current.edges:
        if e.end_node.value not in [i.value for i in path]:
            new_path = dfs(graph, e.end_node, end, path.copy())
            if new_path:
                return new_path

    return None


def bfs(graph, node_list, end, path=[], checked=set()):
    color_entire_graph(graph, Color.BLACK)
    color_array([node for node in graph.nodes if node.value in checked], Color.RED)
    refresh(graph)
    wait(1)

    new_node_list = []
    for node in node_list:
        if node.value == end.value:
            path.append(node)
            return path

        elif node.value not in checked:
            new_node_list.extend([e.end_node for e in node.edges])

        checked.add(node.value)

    if new_node_list:
        return bfs(graph, new_node_list, end, path)

    return None






def boruvkas(graph):
    forest = [[node] for node in graph.nodes]  # list of components

    while len(forest) > 1:
        cheapest_edges = [None for _ in range(len(forest))]

        for i in range(len(forest)):
            for node in forest[i]:
                for conn in node.edges:
                    conn.make_mark(i)

        for i in range(len(forest)):
            for node in forest[i]:
                for conn in node.edges:
                    if not cheapest_edges[i] or conn < cheapest_edges[i]:
                        cheapest_edges[i] = conn
                    if not cheapest_edges[i] or conn < cheapest_edges[conn.mark]:
                        cheapest_edges[conn.mark] = conn

        forest.clear()
        for conn in cheapest_edges:
            forest.append(conn)

        return [(conn.start_node, conn.end_node) for conn in forest]
