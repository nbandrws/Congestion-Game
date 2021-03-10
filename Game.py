from collections import defaultdict
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import networkx as nx


class Game:

    # initialize
    def __init__(self, num_players=1, start_node='start', end_node='end'):
        self.node = set()
        self.edge = defaultdict(list)  # will generate key for dictionary if empty when trying to append
        self.cost = {}  # cost function
        self.num_edge = {}  # number of players on edge
        self.num_players = num_players  # number of players in game

        # construct start and end points
        self.start_node = start_node
        self.add_node(start_node)
        self.end_node = end_node
        self.add_node(end_node)
        self.s_num = None

    # add node
    def add_node(self, value):
        self.node.add(value)

    # set start and end nodes
    def path(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

    # add edge (assumes edges are bi-directional)
    def add_edge(self, from_node, to_node, cost):
        self.edge[from_node].append(to_node)
        self.edge[to_node].append(from_node)
        self.cost[(from_node, to_node)] = cost
        self.cost[(to_node, from_node)] = cost
        self.num_edge[(from_node, to_node)] = None
        self.num_edge[(to_node, from_node)] = None

    # find the vertex with minimum cost from source, from the set of
    # vertices not yet included in shortest path tree. Determines which
    # branch to explore next
    @staticmethod
    def __min_cost(cost, node_set):
        # initialize minimum cost for next node
        min_cost = float('inf')
        min_node = None

        # search vertex not in the shortest path tree
        for u in node_set:
            if cost[u] < min_cost:
                min_cost = cost[u]
                min_node = u

        # return index for minimum vertex
        return min_node, min_cost

    # Dijkstra's algorithm
    def __dijkstra(self):
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
            min_node, min_cost = self.__min_cost(cost_log, node_set)

            # remove minimum node from set
            node_set.remove(min_node)

            # check if we're at end_node
            if min_node is self.end_node:
                break

            # loop over neighbors that are still in node_set
            for neighbor in self.edge[min_node]:
                if neighbor in node_set:
                    # +1 to cost to account for current player
                    alt = min_cost + self.cost[(min_node, neighbor)](self.num_edge[(min_node, neighbor)] + 1)

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

        total_cost = cost_log[self.end_node]
        return path, total_cost

    def nash(self, num_players=None):
        if num_players is None:
            num_players = self.num_players

        # reset number of players on edge to 0
        for key in self.num_edge:
            self.num_edge[key] = 0

        # compute Nash through sequential dijkstra best response calculations
        path_pp = []  # path per player
        for _ in range(num_players):
            path = self.__dijkstra()[0]
            path_pp.append(path)

        # sum up cost to each player after all players have played
        cost_pp = []  # cost per player
        for path in path_pp:
            total_cost = 0
            for idx, node in enumerate(path):
                if node is not path[-1]:
                    num_on_edge = self.num_edge[(path[idx], path[idx + 1])]
                    total_cost += self.cost[(path[idx], path[idx + 1])](num_on_edge)
                else:
                    cost_pp.append(total_cost)

        return cost_pp, path_pp

    # plot network
    def plot_nash(self):
        # check if nash has been calculated already
        if next(iter(self.num_edge.items()))[1] is None:
            self.nash()

        # build edge lists
        edges = []
        players = []
        for from_node in self.node:
            for to_node in self.edge[from_node]:
                if to_node not in [item[0] for item in edges]:
                    edges.append([from_node, to_node])
                    players.append(self.num_edge[(from_node, to_node)])

        # build graph and set colors
        fig, ax = plt.subplots()
        plt.title('Congestion Game: ' + self.start_node + ' to ' + self.end_node)

        # setup colormap
        norm = mpl.colors.Normalize(vmin=0, vmax= 2 * self.num_players)
        mapper = cm.ScalarMappable(norm=norm, cmap=plt.get_cmap('jet'))

        # build graph
        G = nx.Graph()
        idx = 0
        for edge in edges:
            G.add_edge(edge[0], edge[1], color=mapper.to_rgba(players[idx]))
            idx += 1
        colors = nx.get_edge_attributes(G, 'color').values()
        pos = nx.spring_layout(G)

        # plot
        nx.draw_networkx(G, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color=colors, node_size=500, width=10.0)
        plt.colorbar(mapper, label='# of Players')

        # setup widget
        axcolor = 'lightgoldenrodyellow'
        axnum = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
        self.s_num = Slider(axnum, 'Total Players', 1, 2 * self.num_players, valinit=self.num_players, valstep=1)

        def update(val):
            num_players = self.s_num.val
            self.nash(num_players)

            # build edge lists
            edges = []
            players = []
            for from_node in self.node:
                for to_node in self.edge[from_node]:
                    if to_node not in [item[0] for item in edges]:
                        edges.append([from_node, to_node])
                        players.append(self.num_edge[(from_node, to_node)])

            # build graph
            idx = 0
            for edge in edges:
                G.add_edge(edge[0], edge[1], color=mapper.to_rgba(players[idx]))
                idx += 1
            colors = nx.get_edge_attributes(G, 'color').values()

            # re-draw
            ax.clear()
            nx.draw_networkx(G, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color=colors, node_size=500,
                             width=10.0)
            ax.set_title('Congestion Game: ' + self.start_node + ' to ' + self.end_node)
            fig.canvas.draw()

        self.s_num.on_changed(update)
