from Game import Game

# build network
G = Game()
G.path('A', 'F')
G.add_node('A')
G.add_node('Z')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_node('F')
G.add_node('X')
G.add_edge('A', 'B', 3)
G.add_edge('A', 'Z', 25)
G.add_edge('B', 'C', 10)
G.add_edge('B', 'D', 2)
G.add_edge('C', 'F', 1)
G.add_edge('D', 'C', 2)
G.add_edge('X', 'Z', 50)
G.add_edge('D', 'F', 15)

# run Dijkstra
path, dist = G.dijkstra()
# G.plot()