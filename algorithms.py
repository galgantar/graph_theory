import time

def dfs(drawable_graph, current, end, path=[]):
    path.append(current)
    for n in drawable_graph.nodes:
        if n in path:
            n.color_red()
        else:
            n.color_black()

        time.sleep(2)
    if current == end:
        for n in drawable_graph.nodes:
            if n in path:
                n.color_green()
            else:
                n.color_black()
        time.sleep(7)
        return path

    for node in drawable_graph[current].edges:
        if node not in path:
            new_path = dfs(drawable_graph, node, end, path)
            if new_path:
                return new_path
    return None


def bfs(graph, current, end, level=0, path=[], master=True):
    path.append(current)

    if end == current:
        return path
    else:
        for node in graph[current].edges:
            if node not in path:

                new_path = bfs(graph, node, end, level-1, path, False)
                if new_path:
                    return new_path

    while level < graph.nr_of_nodes and master:
        level += 1
        bfs(graph, current, end, level, path, True)

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
