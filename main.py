# import game definition files
from def_dummy import def_dummy
from def_braess import def_braess

# build network
num_players = 4000

# dummy
# g = def_dummy(num_players)
# path1, total_cost1 = g.dijkstra()
# path2, total_cost2 = g.dijkstra()
# costs, paths = g.nash()
# g.plot()

# Braess'
no_braess, braess = def_braess(num_players)
nb_cost, nb_path = no_braess.nash()
no_braess.plot_nash()
# n_cost, n_path = braess.nash()
braess.plot_nash()
