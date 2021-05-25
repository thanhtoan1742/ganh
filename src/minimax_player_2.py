from copy import deepcopy
from player import player
import board_tools as bt


class minimax_player(player):
    def _get_move_(self):
        moves = self._get_possible_moves_()

        best_move = None
        best_move_board = None
        for move in moves:
            temp = deepcopy(self.board)
            bt.apply_move(temp, move)

            if best_move == None or bt.get_score(best_move_board)*self.player < bt.get_score(temp)*self.player:
                best_move = move
                best_move_board = temp

        return best_move


p = minimax_player()
def move(board, player):
    return p.move(board, player)