# import game definition files
from def_dummy import def_dummy
from def_braess import def_braess
from def_medium import def_medium

# build network
num_players = 3000

# dummy example
g = def_dummy(num_players)
g.plot_nash()

# Braess' paradox example
no_braess, braess = def_braess(5000)
nb_cost, nb_path = no_braess.nash()  # cost and path per player
no_braess.plot_nash()  # plot
n_cost, n_path = braess.nash()
braess.plot_nash()

# medium sized example
m = def_medium(100)
m.plot_nash()
