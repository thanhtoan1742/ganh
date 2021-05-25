import numpy as np
import board_tools as bt
from board_tools import eprint


class board:
    def __init__(self, board=bt.get_initial_board(), current_player=1, moves=[]):
        self.board = np.array(board)
        self.current_player = current_player
        self.moves = moves
        self.scores = [bt.get_score(self.board)]


    def __str__(self):
        return bt.get_pretty_string(self.board)


    def pretty_print(self):
        print(bt.get_pretty_string(self.board))


    def get_current_player(self):
        return self.current_player


    def get_board(self):
        return self.board


    def get_winner(self):
        if sum(self.board.flatten() == 1) == 0:
            return -1
        if sum(self.board.flatten() == -1) == 0:
            return 1
        return 0


    def is_finished(self):
        return self.get_winner() != 0
 

    """
    If there is no open move return True.
    If there is any open move, return True if the move is
    an open move.
    """
    def _check_open_move_(self, sx, sy, tx, ty):
        # no previous move
        if len(self.moves) == 0:
            return True

        # previous move does not change score
        change_in_score = self.scores[-1] - self.scores[-2]
        if change_in_score != 0:
            return True

        (u, v), (_, _) = self.moves[-1]
        # previous move does not create opportunity to carry
        if len(bt.get_symmetric_neighbor_pair_with_value(self.board, u, v, 0 - self.current_player)) == 0:
            return True

        # no starting position for an open move
        possible_starting_positions = bt.get_neighbor_with_value(self.board, u, v, self.current_player)
        if len(possible_starting_positions) == 0:
            return True

        # check if current move is an open move or not
        return ((sx, sy) in possible_starting_positions) and (u == tx) and (v == ty)


    '''
    Check to validate move, then make change to the board, both moves then carry/surround
    '''
    def make_move(self, move):
        (sx, sy), (tx, ty) = move

        if self.board[sx][sy] != self.current_player:
            raise Exception('player in starting position does not match current player')
        if self.board[tx][ty] != 0:
            raise Exception('destination is not empty')
        if not (tx, ty) in bt.get_neighbor(sx, sy):
            raise Exception('destination is not reachable from starting position')

        if not self._check_open_move_(sx, sy, tx, ty):
            raise Exception('player has to play open move')

        bt.apply_move(self.board, (sx, sy, tx, ty))
        self.moves.append(move)
        self.scores.append(bt.get_score(self.board))

        self.current_player = 0 - self.current_player