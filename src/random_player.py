from random import choice
from player import player
import board_tools as bt

class random_player(player):
    def _get_move_(self):
        moves = self._get_possible_moves_()
        if len(moves) == 0:
            raise Exception('No available move')
        return choice(moves)

p = random_player()
def move(board, player):
    return p.move(board, player)

p_2 = random_player()
def move_2(board, player):
    return p_2.move(board, player)