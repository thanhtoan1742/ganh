from board import *
from random_player import move as random_move_maker

# class game:
#   - run the main game loop.
#   - let the player interact with ganh.
class game:
    def __init__(self, board=board(), move_maker=random_move_maker):
        self.board = board
        self.move_maker = move_maker
        self.moves = []

    def run(self, verbose=0):
        while 1:
            if self.board.finished():
                break
            
            move = self.move_maker(self.board.get_board(), self.board.get_current_player())
            self.board.make_move(move)
            self.moves.append(move)
            if verbose > 0:
                self.board.pretty_print()

        winner = self.board().get_winner()
        print(f'player {winner} won!!!')


