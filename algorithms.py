from heapq import heappop, heappush, heapify
from color import Color


def one_after_another(element1, element2, array):
    if element1 not in array or element2 not in array:
        return False

    return abs(array.index(element1) - array.index(element2)) == 1


def dfs(gui, current, visited=None, visited_edges=None, iterations=0):
    if visited is None: visited=set()
    if visited_edges is None: visited_edges=set()
    visited.add(current)

    gui.color_entire_graph()
    gui.color_array([e for e in gui.graph.edges if e in visited_edges], Color.RED)
    gui.color_array([n for n in gui.graph.nodes if n.value in visited], Color.RED)
    gui.wait(1)

    for e in gui.graph.get_edges_from_node(current):
        iterations += 1
        if e.second_node not in visited:
            visited_edges.add(e)
            dfs(gui, e.second_node, visited, visited_edges)


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


def TSP(gui, start, current, remaining, path=None, master=True):
    if path is None: path = set()
    remaining.remove(current)

    if not remaining:
        final_edge = gui.graph.get_edge(start, current)
        if final_edge:
            path.add(final_edge)
            weight = final_edge.weight
        else:
            weight = float("inf")
        gui.color_entire_graph()
        gui.color_array(gui.graph.nodes, Color.RED)
        gui.color_array([e for e in gui.graph.edges if e in path], Color.RED)
        gui.wait(0.8)

        return weight, path

    minimal_cost = float("inf")
    final_path = None

    for node in remaining:
        e = gui.graph.get_edge(current, node)
        if e is None:
            continue
        cost, current_path = TSP(gui, start, node, remaining.copy(), path.union({e}), False)
        if cost + e.weight < minimal_cost:
            minimal_cost = cost + e.weight
            final_path = current_path.union({e})

    if master and final_path:
        gui.color_entire_graph()
        gui.color_array(gui.graph.nodes, Color.GREEN)
        gui.color_array([e for e in gui.graph.edges if e in final_path], Color.GREEN)
        gui.wait(5)

    return minimal_cost, final_path


def color_with_min(gui):
    k = 1
    while not color_graph(gui, [c for c in Color.finite_generator(k)], gui.graph.nodes):
        gui.color_array(gui.graph.nodes, Color.NONE)
        k += 1
    return k


def color_graph(gui, colors, nodes_to_color, master=True):
    if not nodes_to_color:
        return True

    for node in nodes_to_color:
        for c in colors:
            for e in gui.graph.get_edges_from_node(node):
                if e.second_node.color == c:
                    break
            else:
                node.color = c
                if color_graph(gui, colors, nodes_to_color - {node}, False):
                    if master:
                        gui.wait(3)
                    return True
    return False
