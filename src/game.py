from random import random
from board import *
from random_player import move as random_move_maker

# class game:
#   - run the main game loop.
#   - let the player interact with ganh.
class game:
    def __init__(self, board=board(), first_move_maker=random_move_maker, second_move_maker=random_move_maker):
        self.board = board
        self.first_move_maker = first_move_maker
        self.second_move_maker = second_move_maker
        self.moves = []

    def run(self, verbose=0):
        current_move_maker = self.first_move_maker
        next_move_maker = self.second_move_maker
        while 1:
            if self.board.finished():
                break

            if verbose > 0:
                self.board.pretty_print()
            move = current_move_maker(self.board.get_board(), self.board.get_current_player())
            self.board.make_move(move)
            self.moves.append(move)

            current_move_maker, next_move_maker = next_move_maker, current_move_maker

        winner = self.board().get_winner()
        print(f'player {winner} won!!!')