from Game import Game

# build network
G = Game()
G.num_players = 1
G.path('A', 'F')
G.add_node('A')
G.add_node('Z')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_node('F')
G.add_node('X')
G.add_edge('A', 'B', lambda x: 3)
G.add_edge('A', 'Z', lambda x: 25)
G.add_edge('B', 'C', lambda x: 10 * x)
G.add_edge('B', 'D', lambda x: 2)
G.add_edge('C', 'F', lambda x: 1)
G.add_edge('D', 'C', lambda x: 2)
G.add_edge('X', 'Z', lambda x: 50)
G.add_edge('D', 'F', lambda x: 15)

# run Dijkstra
path, cost = G.dijkstra()
# G.plot()