import numpy as np
from random import choice
import board_tools as bt
from board_tools import eprint

"""
This class is currently designed so that the player does not change side.
TODO: look into new game.
"""
class player:
    NULL_BOARD = np.zeros((5, 5))
    def __init__(self):
        self.last_board = self.NULL_BOARD
        self.board = self.last_board
        self.moves = []
        self.player = 0


    """
    We are playing a new game if we are playing on first or second turn.
    TODO: Complete the method.
    NOTE: Reset player at new game.
    """
    def _is_new_game_(self):
        return (self.last_board == self.NULL_BOARD).all()
      

    """
    Return open move list if there is one, otherwise return None.
    """
    def _get_open_moves_(self):
        if len(self.moves) == 0:
            return []

        x, y, _, _ = self.moves[-1]
        possible_starting_positions = bt.get_neighbor_with_value(self.board, x, y, self.player)
        if len(possible_starting_positions) == 0:
            return []
        carry_neighbor_pairs = bt.get_symmetric_neighbor_pair_with_value(self.board, x, y, 0 - self.player)
        if len(carry_neighbor_pairs) == 0:
            return []

        return [(u, v, x, y) for u, v in possible_starting_positions]


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

        (x, y), (u, v) = pos
        if self.board[x][y] != 0:
            x, y, u, v = u, v, x, y

        return x, y, u, v


        
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
            if bt.is_initial_board(self.board):
                return
            self.last_board = bt.get_initial_board()

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
    Each concrete player class implements this method.
    Return (x, y, u, v) as the move.
    """

    def _get_possible_moves_(self):
        # If open moves exist, randomly chose 1 play it.
        open_moves = self._get_open_moves_()
        if len(open_moves) > 0:
            return open_moves

        # Randomly chose a starting position then randomly chose a destination.
        moves = [
            (x, y, u, v)
            for x, y, in bt.get_position_with_value(self.board, self.player)
            for u, v in bt.get_neighbor_with_value(self.board, x, y, 0)
        ]
        return moves


    def _get_move_(self):
        raise NotImplementedError

    def move(self, board, player):
        self.board = np.array(board)
        self.player = player
        self._update_opponent_turn_()

        x, y, u, v = self._get_move_()
        self._update_my_turn_((x, y, u, v))
        return (x, y), (u, v)
