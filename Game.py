from collections import defaultdict
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx


class Game:

    # initialize
    def __init__(self):
        self.node = set()
        self.edge = defaultdict(list)  # will generate key for dictionary if empty when trying to append
        self.distance = {}
        self.start_node = None
        self.end_node = None

    # add node
    def add_node(self, value):
        self.node.add(value)

    # define start and destination nodes
    def path(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

    # add edge (assumes edges are bi-directional)
    def add_edge(self, from_node, to_node, distance):
        self.edge[from_node].append(to_node)
        self.edge[to_node].append(from_node)
        self.distance[(from_node, to_node)] = distance
        self.distance[(to_node, from_node)] = distance

    # find the vertex with minimum distance value from source, from the set of
    # vertices not yet included in shortest path tree. Determines which
    # branch to explore next
    @staticmethod
    def min_distance(dist, node_set):

        # initialize minimum distance for next node
        min_dist = float('inf')

        # search vertex not in the shortest path tree
        for u in node_set:
            if dist[u] < min_dist:
                min_dist = dist[u]
                min_node = u

        # return index for minimum vertex
        return min_node, min_dist

    # Dijkstra's algorithm
    def dijkstra(self):
        # dynamic node set
        node_set = set(self.node)

        # pre-allocate dist and prev
        dist = {}
        prev = {}
        for node in node_set:
            dist[node] = float('inf')

        # initialize starting node
        dist[self.start_node] = 0

        while node_set:
            # find node with minimum distance
            min_node, min_dist = self.min_distance(dist, node_set)

            # remove minimum node from set
            node_set.remove(min_node)

            # check if we're at end_node
            if min_node is self.end_node:
                break

            # loop over neighbors that are still in node_set
            for neighbor in self.edge[min_node]:
                if neighbor in node_set:
                    alt = min_dist + self.distance[(min_node, neighbor)]

                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = min_node

        # re-construct path
        path = [self.end_node]
        node = self.end_node
        while True:
            # iterate backwards through dict
            node = prev[node]

            # insert node to front
            path.insert(0, node)

            # exit if at starting node
            if node is self.start_node:
                break

        return path, dist[self.end_node]

    # plot network
    def plot(self):
        # build edge lists
        edges = []
        dists = []
        labels = defaultdict(list)
        for from_node in self.node:
            for to_node in self.edge[from_node]:
                if to_node not in [item[0] for item in edges]:
                    edges.append([from_node, to_node])
                    dists.append(self.distance[(from_node, to_node)])
                    labels[(from_node, to_node)] = self.distance[(from_node, to_node)]

        # setup colormap
        norm = mpl.colors.Normalize(vmin=min(dists), vmax=max(dists))
        mapper = cm.ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))

        # build graph and set colors
        G = nx.Graph()
        idx = 0
        for edge in edges:
            G.add_edge(edge[0], edge[1], color=mapper.to_rgba(dists[idx]))
            idx += 1
        colors = nx.get_edge_attributes(G, 'color').values()
        pos = nx.spring_layout(G)

        # plot
        nx.draw_networkx(G, pos, with_labels=True, node_color='skyblue', edge_color=colors, node_size=500, width=10.0)
        plt.colorbar(mapper, label='Cost')
        plt.title('Congestion Network: ' + self.start_node + ' to ' + self.end_node)
