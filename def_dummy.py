from Game import Game


def def_dummy(num_players):
    g = Game(num_players, 'A', 'F')
    g.add_node('A')
    g.add_node('Z')
    g.add_node('B')
    g.add_node('C')
    g.add_node('D')
    g.add_node('F')
    g.add_node('X')
    g.add_edge('A', 'B', lambda x: 3)
    g.add_edge('A', 'Z', lambda x: 25)
    g.add_edge('B', 'C', lambda x: 10 * x)
    g.add_edge('B', 'D', lambda x: 2)
    g.add_edge('C', 'F', lambda x: 1)
    g.add_edge('D', 'C', lambda x: 2)
    g.add_edge('X', 'Z', lambda x: 50)
    g.add_edge('D', 'F', lambda x: 15)

    return g