from __future__ import print_function
import numpy as np
from random import choice
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

"""
this class is currently designed so that the player does not change side.
TODO: look into new game.
"""
class player:
    dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

    def __init__(self):
        self.last_board = np.zeros((5, 5))
        self.board = self.last_board
        self.moves = []
        self.player = 0

    def _is_in_range_(self, x, y):
        return x >= 0 and y >= 0 and x < 5 and y < 5

    """
    Return all pair of neighbors that:
    - Inside the board
    - Are symmetric with respect to (x, y)
    """
    def _get_symmetric_neighbor_pair_(self, x, y):
        res = []
        for i in range(4):
            ax = x + self.dx[i]
            ay = y + self.dy[i]
            if not self._is_in_range_(ax, ay):
                continue

            bx = x + self.dx[(i + 4)%8]
            by = y + self.dy[(i + 4)%8]
            if not self._is_in_range_(bx, by):
                continue

            res.append((ax, ay, bx, by))
        return res

    """
    Return all pair of carry neighbors of (x, y) that both cell 
    has the value of cell_value.
    """
    def _get_symmetric_neighbor_pair_with_value_(self, cell_value, x, y):
        res = []
        for ax, ay, bx, by in self._get_symmetric_neighbor_pair_(x, y):
            if self.board[ax][ay] != self.board[bx][by]:
                continue
            if self.board[ax][ay] != cell_value:
                continue
            res.append((ax, ay, bx, by))
        return res

    def _get_neighbor_(self, x, y):
        res = []
        for i in range(8):
            if (x + y)%2 == 1 and i%2 == 1:
                continue

            u = x + self.dx[i]
            v = y + self.dy[i]
            if self._is_in_range_(u, v):
                res.append((u, v))
        return res

    """
    Return all position that is neighbor of (x, y) and have the same
    value of cell_value
    """
    def _get_neighbor_with_value_(self, cell_value, x, y):
        res = []
        for u, v in self._get_neighbor_(x, y):
            if self.board[u][v] == cell_value:
                res.append((u, v))
        return res



    """
    Return all position of a player.
    """
    def _get_player_position_(self):
        pos = []
        for x in range(5):
            for y in range(5):
                if self.board[x][y] != self.player:
                    continue
                
                # get all neighbor empty cell.
                if len(self._get_neighbor_with_value_(0, x, y)) == 0:
                    continue

                pos.append((x, y))
        return pos



    """
    We are playing a new game if we are playing on first or second turn.
    Check the n.o. our pieces or oppenent's piece increases.
    TODO: Complete the method.
    NOTE: Reset player at new game.
    """
    def _is_new_game_(self):
        return (self.last_board == np.zeros((5, 5))).all()
      

    """
    Return open move list if there is one, otherwise return None.
    """
    def get_open_moves(self):
        if len(self.moves) == 0:
            return []

        x, y, _, _ = self.moves[-1]
        possible_starting_position = self._get_neighbor_with_value_(self.player, x, y)
        if len(possible_starting_position) == 0:
            return []
        carry_neighbor_pair = self._get_symmetric_neighbor_pair_with_value_(0 - self.player, x, y)
        if len(carry_neighbor_pair) == 0:
            return []

        return [(u, v, x, y) for u, v in possible_starting_position]


    """
    Extract the opponent move from 2 consecutive board.
    """
    def _extract_opponent_move_(self):
        pos = [
            (x, y) 
            for y in range(5) 
            for x in range(5) 
            if abs(self.board[x][y]) != abs(self.last_board[x][y])
        ]
        eprint(self.last_board)
        eprint(self.board)
        eprint(pos)

        (x, y), (u, v) = pos
        if self.board[x][y] != 0:
            x, y, u, v = u, v, x, y

        return x, y, u, v


    def _get_initial_board_(self):
        return np.array([
            [ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1],
        ])


    def _is_initial_board_(self):
        initial_board = self._get_initial_board_()
        return (initial_board == self.board).all()

        
    """
    If we are playing a new game then reset moves list and add the opponent
    move to the moves list if it exist. Otherwise, we just add the opponent
    move the the moves list.
    The opponent move is calculated from last_board and board.
    """
    def _update_opponent_turn_(self):
        if self._is_new_game_():
            self.moves = []
            # If we play the first turn the do nothing.
            # Else we set last_board to initial board
            if self._is_initial_board_():
                return
            self.last_board = self._get_initial_board_()

        opponent_move = self._extract_opponent_move_()
        self.moves.append(opponent_move)


    """
    Set last_board to the state after we make our move.
    """
    def _update_my_turn_(self, move):
        x, y, u, v = move
        self.moves.append(move)
        self.last_board = self.board
        self.last_board[u][v] = self.last_board[x][y]
        self.last_board[x][y] = 0

    """
    Each player implement this method.
    Return (x, y, u, v) as the move.
    """
    def _get_move_(self):
        raise NotImplementedError

    def move(self, board, player):
        self.board = np.array(board)
        self.player = player
        self._update_opponent_turn_()

        x, y, u, v = self._get_move_()
        self._update_my_turn_((x, y, u, v))
        return (x, y), (u, v)
