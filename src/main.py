from game import *
from input_player import move as input_move_maker
from random_player import move as random_move_maker
from minimax_player import move as minimax_move_maker

# g = game(first_move_maker=input_move_maker)
g = game()
g.run(verbose=1)