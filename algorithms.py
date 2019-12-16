from graph import Color, Graph, Node
from main import wait, color_array, color_entire_graph


def one_after_another(element1, element2, array):
    if element1 not in array or element2 not in array:
        return False

    return abs(array.index(element1) - array.index(element2)) == 1


def dfs(graph, current, end, path=[]):
    path.append(current.value)

    color_entire_graph(graph)
    color_array([e for e in graph.edges if one_after_another(e.start_node.value, e.end_node.value, path)], Color.RED)
    color_array([n for n in graph.nodes if n.value in path], Color.RED)
    wait(1, graph)

    if current.value == end.value:
        color_entire_graph(graph)
        color_array([e for e in graph.edges if one_after_another(e.start_node.value, e.end_node.value, path)], Color.GREEN)
        color_array([n for n in graph.nodes if n.value in path], Color.GREEN)
        wait(5, graph)

        return path

    for e in current.edges:
        if e.end_node.value not in path:
            new_path = dfs(graph, e.end_node, end, path.copy())
            if new_path:
                return new_path

    return None


def bfs(graph: Graph, node_list: list, end: Node, path: list=[], checked_nodes: list=[], master: bool=True):
    color_entire_graph(graph)
    color_array([node for node in graph.nodes if node.value in [pair[1] for pair in checked_nodes]], Color.RED)
    color_array([e for e in graph.edges if (e.start_node.value, e.end_node.value) in checked_nodes], Color.RED)
    wait(1, graph)

    new_node_list = []
    for node in node_list:
        if node[1].value == end.value:
            path.append(node[1].value)
            return path, node[0].value

        elif node[1].value not in [pair[1] for pair in checked_nodes]:
            new_node_list.extend([(e.start_node, e.end_node) for e in node[1].edges])
            if not master:
                checked_nodes.append((node[0].value, node[1].value))
            else:
                checked_nodes.append((node[0], node[1].value))

    if new_node_list:
        path, prev_val = bfs(graph, new_node_list, end, path.copy(), checked_nodes, False)
        if path and prev_val:
            path.append(prev_val)
            if master:
                color_entire_graph(graph)
                color_array([node for node in graph.nodes if node.value in path], Color.GREEN)
                color_array([e for e in graph.edges if e.start_node in path and e.end_node in path], Color.GREEN)
                wait(7, graph)
                return path[::-1]
            else:
                for node in node_list:
                    if node[1].value == prev_val:
                        return path, node[0].value
    return None, None


def boruvkas(graph):
    if not graph.is_connected():
        print("Cannot run Bovurkas on unconnected graph")
        return None
    involved_edges = []
    forest = [[node] for node in graph.nodes]

    while len(forest) > 1:
        color_entire_graph(graph)
        colored_edges = []
        for e in graph.edges:
            for comp in forest:
                if e.start_node in comp and e.end_node in comp:
                    colored_edges.append(e)
        color_array(colored_edges, Color.RED)  # Later RANDOM
        wait(1, graph)

        for i in range(len(forest)):
            for node in forest[i]:
                node.make_mark(i)

        cheapest_edges = [None for _ in range(len(forest))]

        for edge in graph.edges:
            if edge.start_node.mark != edge.end_node.mark:
                if not cheapest_edges[edge.start_node.mark] or edge.weight < cheapest_edges[edge.start_node.mark].weight:
                    cheapest_edges[edge.start_node.mark] = edge
                if not cheapest_edges[edge.end_node.mark] or edge.weight < cheapest_edges[edge.end_node.mark].weight:
                    cheapest_edges[edge.end_node.mark] = edge

        involved_edges.extend(cheapest_edges)

        new_forest = []
        for edge_index in range(len(cheapest_edges)):
            new_component = []
            for component_index in range(len(forest)):
                if cheapest_edges[edge_index].start_node in forest[component_index] or cheapest_edges[edge_index].end_node in forest[component_index]:
                    new_component.extend(forest[component_index])

            new_index = -1
            for component in new_forest:
                if cheapest_edges[edge_index].start_node in component or cheapest_edges[edge_index].end_node in component:
                    new_index = new_forest.index(component)
                    break

            if new_index == -1:
                new_forest.append(new_component)
            else:
                new_forest[new_index].extend(new_component)

        forest = new_forest

    color_entire_graph(graph)
    color_array([e for e in graph.edges if e in involved_edges], Color.GREEN)
    wait(5, graph)

    return involved_edges
