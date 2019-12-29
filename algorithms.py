from graph import Color

"""Barvanje"""

def one_after_another(element1, element2, array):
    if element1 not in array or element2 not in array:
        return False

    return abs(array.index(element1) - array.index(element2)) == 1


def dfs(gui, current, end, path=None):
    if path is None: path=[]
    path.append(current.value)

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if one_after_another(e.start_node.value, e.end_node.value, path)], Color.RED)
    gui.color_array([n for n in gui.graph.nodes if n.value in path], Color.RED)
    gui.wait(1)

    if current.value == end.value:
        gui.color_entire_graph()
        gui.color_array([e for e in gui.graph.edges if one_after_another(e.start_node.value, e.end_node.value, path)], Color.GREEN)
        gui.color_array([n for n in gui.graph.nodes if n.value in path], Color.GREEN)
        gui.wait(5)

        return path

    for e in current.edges:
        if e.end_node.value not in path:
            new_path = dfs(gui, e.end_node, end, path.copy())
            if new_path:
                return new_path

    return None


def bfs(gui, node_list, end, path=None, checked_nodes=None, master=True):
    if path is None: path=[]
    if checked_nodes is None: checked_nodes=[]

    gui.color_entire_graph()
    gui.color_array([node for node in gui.graph.nodes if node.value in [pair[1] for pair in checked_nodes]], Color.RED)
    gui.color_array([e for e in gui.graph.edges if (e.start_node.value, e.end_node.value) in checked_nodes], Color.RED)
    gui.wait(1)

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
        path, prev_val = bfs(gui, new_node_list, end, path.copy(), checked_nodes, False)
        if path and prev_val:
            path.append(prev_val)
            if master:
                gui.color_entire_graph()
                gui.color_array([node for node in gui.graph.nodes if node.value in path], Color.GREEN)
                gui.color_array([e for e in gui.graph.edges if e.start_node in path and e.end_node in path], Color.GREEN)
                gui.wait(7)
                return path[::-1]
            else:
                for node in node_list:
                    if node[1].value == prev_val:
                        return path, node[0].value
    return None, None


def boruvkas(gui):
    if not gui.graph.is_graph_connected():
        print("Cannot run Bovurkas on unconnected graph")
        return None

    involved_edges = []
    forest = [[node] for node in gui.graph.nodes]

    while len(forest) > 1:
        gui.color_entire_graph()
        colored_edges = []
        for e in gui.graph.edges:
            for comp in forest:
                if e.start_node in comp and e.end_node in comp:
                    colored_edges.append(e)
        gui.color_array(colored_edges, Color.RED)  # Later RANDOM
        gui.wait(1)

        for i in range(len(forest)):
            for node in forest[i]:
                node.make_mark(i)

        cheapest_edges = [None for _ in range(len(forest))]

        for edge in gui.graph.edges:
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

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if e in involved_edges], Color.GREEN)
    gui.wait(5)

    return involved_edges
