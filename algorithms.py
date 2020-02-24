from heapq import heappop, heappush, heapify
from color import Color


def one_after_another(element1, element2, array):
    if element1 not in array or element2 not in array:
        return False

    return abs(array.index(element1) - array.index(element2)) == 1


def dfs(gui, current, visited=None):
    if visited is None: visited=[]
    visited.append(current.value)

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if one_after_another(e.first_node.value, e.second_node.value, visited)], Color.RED)
    gui.color_array([n for n in gui.graph.nodes if n.value in visited], Color.RED)
    gui.wait(1)

    for e in gui.graph.get_edges_from_node(current):
        if e.second_node.value not in visited:
            dfs(gui, e.second_node, visited)


def bfs(gui, start_node):
    checked_pairs = [(None, start_node)]
    next_to_check = [start_node]

    while next_to_check:
        gui.color_entire_graph()
        gui.color_array([node for node in gui.graph.nodes if node.value in (second for first, second in checked_pairs)],
                        Color.RED)
        gui.color_array([e for e in gui.graph.edges if (e.first_node.value, e.second_node.value) in checked_pairs
                         or (e.second_node.value, e.first_node.value) in checked_pairs], Color.RED)
        gui.wait(1)

        new_nodes_to_check = []
        for node in next_to_check:
            neighbours = [e.second_node for e in gui.graph.get_edges_from_node(node) if e.second_node not in (p[1] for p in checked_pairs)]
            new_nodes_to_check.extend(neighbours)
            checked_pairs.extend([(node, n) for n in neighbours])

        next_to_check = new_nodes_to_check


def boruvkas(gui):
    if not gui.graph.weakly_connected:
        print("Spanning tree doesn't exist")
        return None

    forest = [set([node]) for node in gui.graph.nodes]
    MST = set()

    while len(forest) > 1:
        for i, component in enumerate(forest):
            for node in component:
                node.make_mark(i)

        cheapest_edges = [None for _ in range(len(forest))]

        for edge in gui.graph.edges:
            if edge.first_node.mark != edge.second_node.mark:
                if not cheapest_edges[edge.first_node.mark] or edge < cheapest_edges[edge.first_node.mark]:
                    cheapest_edges[edge.first_node.mark] = edge
                if not cheapest_edges[edge.second_node.mark] or edge < cheapest_edges[edge.second_node.mark]:
                    cheapest_edges[edge.second_node.mark] = edge

        new_forest = []
        for e in set(filter(None, cheapest_edges)):
            MST.add(e)
            C = forest[e.first_node.mark]
            C.update(forest[e.second_node.mark])
            new_forest.append(C)

        # Color elements
        gui.color_entire_graph()
        component_colors = list(Color.finite_generator(len(forest)))
        for node in gui.graph.nodes:
            node.color_element(component_colors[node.mark])
        for e in gui.graph.edges:
            if e.first_node.mark == e.second_node.mark and e in MST:
                e.color_element(component_colors[e.first_node.mark])
        gui.wait(7)

        forest = new_forest

    chosen_color = next(iter(gui.graph.nodes)).color
    gui.color_array(gui.graph.nodes, chosen_color)
    gui.color_array([e for e in gui.graph.edges if e in MST], chosen_color)
    gui.wait(5)
    return MST


def prims(gui):
    if not gui.graph.weakly_connected:
        print("Spanning tree doesn't exist")
        return None

    visited, MST = set(), set()
    first_node = next(iter(gui.graph.nodes))
    visited.add(first_node)
    all_edges = list(gui.graph.get_edges_from_node(first_node))
    heapify(all_edges)

    while len(visited) < gui.graph.order:
        gui.color_entire_graph()
        gui.color_array([e for e in gui.graph.edges if e in MST], Color.RED)
        gui.color_array([n for n in gui.graph.nodes if n in visited], Color.RED)
        gui.wait(1)

        while True:
            e = heappop(all_edges)
            if e.first_node not in visited or e.second_node not in visited: break
        MST.add(e)
        visited.add(e.second_node)
        for new_edge in gui.graph.get_edges_from_node(e.second_node):
            heappush(all_edges, new_edge)

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if e in MST], Color.RED)
    gui.color_array([n for n in gui.graph.nodes if n in visited], Color.RED)
    gui.wait(5)

    return MST


def color_graph(gui):
    color_gen = Color.infinite_generator()
    first_color = next(color_gen)
    used_colors = [first_color]

    for i, node in enumerate(gui.graph.nodes):
        if i == 0:
            node.color = first_color
        else:
            node.color = Color.NONE

    for node in gui.graph.nodes:
        if node.color == Color.NONE:
            taken_colors = [e.second_node.color for e in gui.graph.get_edges_from_node(node) if e.second_node.color != Color.NONE]
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
