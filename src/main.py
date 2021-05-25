from game import *
from input_player import move as input_move_maker
from random_player import move as random_move_maker
from minimax_player import move as minimax_move_maker
from minimax_player_2 import move as minimax_move_maker_2
from monte_carlo_move import move as monte_carlo_move

# g = game(first_move_maker=input_move_maker)
# g = game(first_move_maker=minimax_move_maker_2, second_move_maker=random_move_maker)
g = game()
g.run(verbose=0, limit_time=True)