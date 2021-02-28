from collections import defaultdict


class Graph:

    # initialize
    def __init__(self):
        self.node = set()
        self.edge = defaultdict(list)  # will generate key for dictionary if empty when trying to append
        self.distance = {}

    # add node
    def add_node(self, value):
        self.node.add(value)

    # add edge
    def add_edge(self, from_node, to_node, distance):
        self.edge[from_node].append(to_node)
        self.edge[to_node].append(from_node)
        self.distance[(from_node, to_node)] = distance
        self.distance[(to_node, from_node)] = distance

    # find the vertex with minimum distance value, from the set of
    # vertices not yet included in shortest path tree
    @staticmethod
    def min_distance(dist, node_set):

        # initialize minimum distance for next node
        min_dist = float('inf')

        # Search not nearest vertex not in the
        # shortest path tree
        for u in node_set:
            if dist[u] < min_dist:
                min_dist = dist[u]
                min_node = u

        # return index for minimum vertex
        return min_node, min_dist

    # Dijkstra's algorithm
    def dijkstra(self, start_node, end_node):
        visited = {start_node: 0} # {node: distance from start_node}
        path = {}

        # dynamic node set
        node_set = set(self.node)

        # pre-allocate dist and prev
        dist = {}
        prev = {}
        for node in node_set:
            dist[node] = float('inf')

        # initialize starting node
        dist[start_node] = 0

        while node_set:
            # find node with minimum distance
            min_node, min_dist = self.min_distance(dist, node_set)

            # remove minimum node from set
            node_set.remove(min_node)

            # check if we're at end_node
            if min_node is end_node:
                break

            # loop over neighbors that are still in node_set
            for neighbor in self.edge[min_node]:
                if neighbor in node_set:
                    alt = min_dist + self.distance[(min_node, neighbor)]

                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = min_node

        # re-construct path
        path = [end_node]
        node = end_node
        while True:
            # iterate backwards through list
            node = prev[node]

            # insert node in to front
            path.insert(0, node)

            # exit if at starting node
            if node is start_node:
                break

        return path, dist[end_node]

    # plot nodes
    def plot_graph(self):
        None
