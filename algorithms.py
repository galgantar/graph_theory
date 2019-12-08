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


def bfs(graph, node_list, end, path=[], checked_nodes=set(), master=True):
    color_entire_graph(graph, Color.BLACK)
    color_array([node for node in graph.nodes if node.value in checked_nodes], Color.RED)
    refresh(graph)
    wait(1)

    new_node_list = []
    for node in node_list:
        if node[1].value == end.value:
            path.append(node[1].value)
            return path, node[0].value

        elif node[1].value not in checked_nodes:
            new_node_list.extend([(e.start_node, e.end_node) for e in node[1].edges])
            checked_nodes.add(node[1].value)

    if new_node_list:
        path, prev_val = bfs(graph, new_node_list, end, path.copy(), checked_nodes, False)
        path.append(prev_val)
        if master:
            color_entire_graph(graph, Color.BLACK)
            color_array([node for node in graph.nodes if node.value in path], Color.GREEN)
            color_array([e for e in graph.edges if e.start_node in path and e.end_node in path], Color.GREEN)
            refresh(graph)
            wait(7)
            return path
        else:
            for node in node_list:
                if node[1].value == prev_val:
                    return path, node[0].value
    return None


def boruvkas(graph):
    forest = [[node] for node in graph.nodes]

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

        color_array([e for e in graph.edges if e in cheapest_edges], Color.RED)
        refresh(graph)
        wait(1)

        forest.clear()
        for conn in cheapest_edges:
            forest.append(conn)

        involved_nodes = set()
        for conn in forest:
            involved_nodes.add(conn.start_node.value)
            involved_nodes.add(conn.end_node.value)

        color_entire_graph(graph, Color.BLACK)
        color_array([n for n in graph.nodes if n.value in involved_nodes], Color.BLUE)
        color_array([e for e in graph.edges if e in forest], Color.BLUE)
        refresh(graph)
        wait(10)

        return [(conn.start_node, conn.end_node) for conn in forest]
