from game import *
from input_player import move as input_move_maker

g = game(first_move_maker=input_move_maker)
g.run(verbose=1)