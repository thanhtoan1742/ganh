import numpy as np
import board_tools as bt
from board_tools import eprint


class board:
    def __init__(self, board=bt.get_initial_board(), current_player=1):
        self.board = board
        self.current_player = current_player
        self.moves = []


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
 

    def _check_open_move_(self, sx, sy, tx, ty):
        if len(self.moves) == 0:
            return True
        (u, v), (_, _) = self.moves[-1]

        if len(bt.get_symmetric_neighbor_pair_with_value(self.board, u, v, 0 - self.current_player)) == 0:
            return True

        possible_starting_positions = bt.get_neighbor_with_value(self.board, u, v, self.current_player)
        if len(possible_starting_positions) == 0:
            return True

        return ((sx, sy) in possible_starting_positions) and (u == tx) and (v == ty)


    '''
    Get opposite pairs of opponent's pieces to be carried, flip into friendly pieces.
    '''
    def _update_carry_(self, x, y):
        for ax, ay, bx, by in bt.get_symmetric_neighbor_pair_with_value(self.board, x, y, 0 - self.current_player):
            self.board[ax][ay] = self.board[x][y]
            self.board[bx][by] = self.board[x][y]



    '''
    Check all surrounded oppoent's node, flip all of surrounded inside enemy node
    '''
    def _update_surround_(self):
        mask = bt.get_connected_component_mask(self.board)
        ncc = max(mask.flatten()) + 1

        is_reachable_empties = np.zeros(ncc, dtype=bool)
        for x in range(bt.N_ROW):
            for y in range(bt.N_COL):
                if len(bt.get_neighbor_with_value(self.board, x, y, 0)) > 0:
                    is_reachable_empties[mask[x][y]] = 1

        for x in range(bt.N_ROW):
            for y in range(bt.N_COL):
                if self.board[x][y] != 0 - self.current_player:
                    continue

                if not is_reachable_empties[mask[x][y]]:
                    self.board[x][y] = self.current_player


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

        self.board[sx][sy] = 0
        self.board[tx][ty] = self.current_player
        self.moves.append(move)

        self._update_carry_(tx, ty)
        self._update_surround_()

        self.current_player = 0 - self.current_player