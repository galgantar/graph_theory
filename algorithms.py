from heapq import heappop, heappush, heapify
from graph import Color


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


def bfs(gui, node_list, end, path=None, checked_pairs=None, first_call=True):
    if path is None: path=[]
    if checked_pairs is None: checked_pairs=[]

    gui.color_entire_graph()
    gui.color_array([node for node in gui.graph.nodes if node.value in (second for first, second in checked_pairs)], Color.RED)
    gui.color_array([e for e in gui.graph.edges if (e.start_node.value, e.end_node.value) in checked_pairs], Color.RED)
    gui.wait(1)

    new_node_list = []
    for first, second in node_list:
        if second.value == end.value:
            path.append(second.value)
            return path, first.value

        elif second.value not in [second for first, second in checked_pairs]:
            new_node_list.extend([(e.start_node, e.end_node) for e in second.edges])
            if not first_call:
                checked_pairs.append((first.value, second.value))
            else:
                checked_pairs.append((None, second.value))

    if new_node_list:
        path, prev_val = bfs(gui, new_node_list, end, path.copy(), checked_pairs, False)
        if path and prev_val:
            path.append(prev_val)
            if first_call:
                gui.color_entire_graph()
                gui.color_array([node for node in gui.graph.nodes if node.value in path], Color.GREEN)
                gui.color_array([e for e in gui.graph.edges if e.start_node in path and e.end_node in path], Color.GREEN)
                gui.wait(7)
                return reversed(path)
            else:
                for first, second in node_list:
                    if second.value == prev_val:
                        return path, first.value
    return None, None


def boruvkas(gui):
    if not gui.graph.weakly_connected:
        print("Spanning tree doesn't exist")
        return None

    involved_edges = set()
    forest = [[node] for node in gui.graph.nodes]

    while len(forest) > 1:
        for i, component in enumerate(forest):
            for node in component:
                node.make_mark(i)

        cheapest_edges = [None for _ in range(len(forest))]

        for edge in gui.graph.edges:
            if edge.start_node.mark != edge.end_node.mark:
                if not cheapest_edges[edge.start_node.mark] or edge < cheapest_edges[edge.start_node.mark]:
                    cheapest_edges[edge.start_node.mark] = edge
                if not cheapest_edges[edge.end_node.mark] or edge < cheapest_edges[edge.end_node.mark]:
                    cheapest_edges[edge.end_node.mark] = edge

        involved_edges.update(cheapest_edges)

        new_forest = []
        for edge in cheapest_edges:
            new_component = []
            for component in forest:
                if edge.start_node in component or edge.end_node in component:
                    new_component.extend(component)

            for component in new_forest:
                if edge.start_node in component or edge.end_node in component:
                    component.extend(new_component)
                    break
            else:
                new_forest.append(new_component)

        # Color elements
        gui.color_entire_graph()
        component_colors = list(Color.finite_generator(len(forest)))
        for node in gui.graph.nodes:
            node.color_element(component_colors[node.mark])
        for e in gui.graph.edges:
            if e.start_node.mark == e.end_node.mark and e in involved_edges:
                e.color_element(component_colors[e.start_node.mark])
        gui.wait(7)

        forest = new_forest

    chosen_color = next(iter(gui.graph.nodes)).color
    gui.color_array(gui.graph.nodes, chosen_color)
    gui.color_array([e for e in gui.graph.edges if e in involved_edges], chosen_color)
    gui.wait(5)
    return involved_edges


def prims(gui):
    if not gui.graph.weakly_connected:
        print("Spanning tree doesn't exist")
        return None

    visited, min_tree = set(), set()
    first_node = next(iter(gui.graph.nodes))
    visited.add(first_node)
    next_edge = [e for e in first_node.edges]
    heapify(next_edge)

    while len(visited) < gui.graph.order:
        gui.color_entire_graph()
        gui.color_array([e for e in gui.graph.edges if e in min_tree], Color.RED)
        gui.color_array([n for n in gui.graph.nodes if n in visited], Color.RED)
        gui.wait(1)

        while True:
            e = heappop(next_edge)
            if e not in min_tree and (e.start_node not in visited or e.end_node not in visited): break
        min_tree.add(e)
        visited.add(e.end_node)
        for edge in e.end_node.edges:
            heappush(next_edge, edge)

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if e in min_tree], Color.RED)
    gui.color_array([n for n in gui.graph.nodes if n in visited], Color.RED)
    gui.wait(5)

    return min_tree


def color_graph(gui):
    color_gen = Color.infinite_generator()
    first_color = next(color_gen)
    gui.graph.nodes[0].color = first_color
    used_colors = [first_color]

    for i in range(1, len(gui.graph.nodes)):
        gui.graph.nodes[i].color = Color.NONE

    for node in gui.graph.nodes:
        if node.color == Color.NONE:
            taken_colors = [e.end_node.color for e in node.edges if e.end_node.color != Color.NONE]
            for color in used_colors:
                if color not in taken_colors:
                    node.color = color
                    break
            else:
                node.color = next(color_gen)
                used_colors.append(node.color)

    gui.wait(5)
    return len(used_colors)


def TSP(gui, start, current, remaining, path=None, master=True):
    if path is None: path = set()
    if not gui.graph.totally_connected:
        print("Can't calculate TSP - edges missing")
        return None

    if not remaining:
        last_edge = gui.graph.get_edge(start, current)
        if last_edge: path.add(last_edge)
        gui.color_entire_graph()
        gui.color_array(gui.graph.nodes, Color.RED)
        gui.color_array([e for e in gui.graph.edges if e in path], Color.RED)
        gui.wait(0.3)
        return gui.graph.cost_of_edge(start, current), set([gui.graph.get_edge(start, current)])

    minimal_cost = float("inf")
    final_path = None

    for node in remaining - set([current]):
        e = gui.graph.get_edge(current, node)
        cost, current_path = TSP(gui, start, node, remaining - set([node]), path.union(set([e])), False)
        if cost + e.weight < minimal_cost:
            minimal_cost = cost + e.weight
            final_path = current_path.union(set([e]))

    if master:
        gui.color_entire_graph()
        gui.color_array(gui.graph.nodes, Color.RED)
        gui.color_array([e for e in gui.graph.edges if e in final_path], Color.RED)
        gui.wait(5)

    return minimal_cost, final_path
