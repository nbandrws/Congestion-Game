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
        self.cost = {}  # cost function
        self.num_edge = {}  # number of players on edge
        self.start_node = None
        self.end_node = None
        self.num_players = None  # number of players in game

    # add node
    def add_node(self, value):
        self.node.add(value)

    # define start and destination nodes
    def path(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

    # add edge (assumes edges are bi-directional)
    def add_edge(self, from_node, to_node, cost):
        self.edge[from_node].append(to_node)
        self.edge[to_node].append(from_node)
        self.cost[(from_node, to_node)] = cost
        self.cost[(to_node, from_node)] = cost
        self.num_edge[(from_node, to_node)] = 0  # initialize number of players on edge to 0
        self.num_edge[(to_node, from_node)] = 0

    # find the vertex with minimum cost from source, from the set of
    # vertices not yet included in shortest path tree. Determines which
    # branch to explore next
    @staticmethod
    def min_cost(cost, node_set):

        # initialize minimum cost for next node
        min_cost = float('inf')

        # search vertex not in the shortest path tree
        for u in node_set:
            if cost[u] < min_cost:
                min_cost = cost[u]
                min_node = u

        # return index for minimum vertex
        return min_node, min_cost

    # Dijkstra's algorithm
    def dijkstra(self):
        # dynamic node set
        node_set = set(self.node)

        # pre-allocate cost and visit_log
        cost_log = {}
        visit_log = {}
        for node in node_set:
            cost_log[node] = float('inf')

        # initialize starting node
        cost_log[self.start_node] = 0

        while node_set:
            # find node with minimum cost
            min_node, min_cost = self.min_cost(cost_log, node_set)

            # remove minimum node from set
            node_set.remove(min_node)

            # check if we're at end_node
            if min_node is self.end_node:
                break

            # loop over neighbors that are still in node_set
            for neighbor in self.edge[min_node]:
                if neighbor in node_set:
                    alt = min_cost + self.cost[(min_node, neighbor)](self.num_edge[(min_node, neighbor)])

                    if alt < cost_log[neighbor]:
                        cost_log[neighbor] = alt
                        visit_log[neighbor] = min_node

        # re-construct path
        path = [self.end_node]
        node = self.end_node
        while True:
            # iterate backwards through visit_log
            node = visit_log[node]

            # insert node to front
            path.insert(0, node)

            # update number of players on path
            self.num_edge[(path[0], path[1])] += 1
            self.num_edge[(path[1], path[0])] += 1

            # exit if at starting node
            if node is self.start_node:
                break

        return path, cost_log[self.end_node]

    # find Nash
    def nash(self):
        None

    # plot network
    def plot(self):
        # build edge lists
        edges = []
        costs = []
        labels = defaultdict(list)
        for from_node in self.node:
            for to_node in self.edge[from_node]:
                if to_node not in [item[0] for item in edges]:
                    edges.append([from_node, to_node])
                    costs.append(self.cost[(from_node, to_node)])
                    labels[(from_node, to_node)] = self.cost[(from_node, to_node)]

        # setup colormap
        norm = mpl.colors.Normalize(vmin=min(costs), vmax=max(costs))
        mapper = cm.ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))

        # build graph and set colors
        G = nx.Graph()
        idx = 0
        for edge in edges:
            G.add_edge(edge[0], edge[1], color=mapper.to_rgba(costs[idx]))
            idx += 1
        colors = nx.get_edge_attributes(G, 'color').values()
        pos = nx.spring_layout(G)

        # plot
        nx.draw_networkx(G, pos, with_labels=True, node_color='skyblue', edge_color=colors, node_size=500, width=10.0)
        plt.colorbar(mapper, label='Cost')
        plt.title('Congestion Network: ' + self.start_node + ' to ' + self.end_node)
