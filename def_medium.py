# medium sized example
from Game import Game


def def_medium(num_players):
    g = Game(num_players)
    g.add_node('A')
    g.add_node('B')
    g.add_node('C')
    g.add_node('D')
    g.add_node('E')
    g.add_node('F')
    g.add_node('G')
    g.add_edge('start', 'A', lambda x: x / 50)
    g.add_edge('start', 'B', lambda x: x)
    g.add_edge('A', 'B', lambda x: 90)
    g.add_edge('A', 'C', lambda x: 3 * x)
    g.add_edge('D', 'B', lambda x: 30)
    g.add_edge('C', 'D', lambda x: 2 * x)
    g.add_edge('G', 'C', lambda x: 4)
    g.add_edge('B', 'E', lambda x: x / 100)
    g.add_edge('D', 'E', lambda x: x ** 2 / 20)
    g.add_edge('F', 'C', lambda x: x ** 2 / 10)
    g.add_edge('F', 'G', lambda x: 14)
    g.add_edge('F', 'end', lambda x: 40)
    g.add_edge('G', 'E', lambda x: x / 20)
    g.add_edge('G', 'end', lambda x: 30)

    return g
