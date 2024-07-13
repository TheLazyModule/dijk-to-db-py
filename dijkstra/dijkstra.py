import heapq


def dijkstra(graph, initial, end):
    # shortest_paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return None, []  # No path exists

        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in the shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return shortest_paths[end][1], path


def bidirectional_dijkstra(graph, initial, end):
    forward_paths = {initial: (None, 0)}
    backward_paths = {end: (None, 0)}
    forward_queue = [(0, initial)]
    backward_queue = [(0, end)]
    visited_forward = set()
    visited_backward = set()
    best_path = None
    best_weight = float('inf')

    def visit_node(queue, paths, visited, other_paths):
        nonlocal best_weight, best_path  # Ensure these variables are accessible
        (current_weight, current_node) = heapq.heappop(queue)
        if current_node in visited:
            return

        visited.add(current_node)

        if current_node in other_paths:
            path_weight = current_weight + other_paths[current_node][1]
            if path_weight < best_weight:
                best_weight = path_weight
                best_path = current_node

        for next_node in graph.edges[current_node]:
            weight = graph.weights[(current_node, next_node)]
            new_weight = current_weight + weight
            if next_node not in paths or new_weight < paths[next_node][1]:
                paths[next_node] = (current_node, new_weight)
                heapq.heappush(queue, (new_weight, next_node))

    while forward_queue and backward_queue:
        if forward_queue:
            visit_node(forward_queue, forward_paths, visited_forward, backward_paths)
        if backward_queue:
            visit_node(backward_queue, backward_paths, visited_backward, forward_paths)
        if best_path:
            break

    if best_path:
        forward_path = []
        node = best_path
        while node:
            forward_path.append(node)
            node = forward_paths[node][0]
        forward_path.reverse()

        backward_path = []
        node = best_path
        while node:
            backward_path.append(node)
            node = backward_paths[node][0]

        backward_path = backward_path[1:]  # Remove the duplicate meeting node

        return best_weight, forward_path + backward_path
    else:
        return None, []  # No path exists
