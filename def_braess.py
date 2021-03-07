# builds Braess' paradox example games
# see https://en.wikipedia.org/wiki/Braess's_paradox for example reference
from Game import Game


def def_braess(num_players):
    # Braess no paradox
    no_braess = Game(num_players)
    no_braess.add_node('A')
    no_braess.add_node('B')
    no_braess.add_edge('start', 'A', lambda x: x / 100)
    no_braess.add_edge('A', 'end', lambda x: 45)
    no_braess.add_edge('start', 'B', lambda x: 45)
    no_braess.add_edge('B', 'end', lambda x: x / 100)

    # Braess paradox
    braess = Game(num_players)
    braess.add_node('A')
    braess.add_node('B')
    braess.add_edge('start', 'A', lambda x: x / 100)
    braess.add_edge('A', 'end', lambda x: 45)
    braess.add_edge('start', 'B', lambda x: 45)
    braess.add_edge('B', 'end', lambda x: x / 100)
    braess.add_edge('A', 'B', lambda x: 0)

    return no_braess, braess