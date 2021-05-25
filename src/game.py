import time
from board import *
from random_player import move as random_move_maker_1
from random_player import move_2 as random_move_maker_2

class game:
    TIME_LIMIT = 3

    def __init__(self, board=board(), first_move_maker=random_move_maker_1, second_move_maker=random_move_maker_2):
        self.board = board
        self.first_move_maker = first_move_maker
        self.second_move_maker = second_move_maker

    def run(self, verbose=0, limit_time=False):
        current_move_maker = self.first_move_maker
        next_move_maker = self.second_move_maker
        while 1:
            if verbose > 0:
                self.board.pretty_print()
            if self.board.is_finished():
                break



            begin_time = time.perf_counter()
            move = current_move_maker(self.board.get_board(), self.board.get_current_player())
            duration = time.perf_counter() - begin_time
            if verbose > 0:
                print('time: %.4f' % duration)
            if duration > self.TIME_LIMIT and limit_time:
                raise Exception('time limit exceeded, your time is %4f' % duration)


            c_player = 'X' if self.board.get_current_player() == 1 else 'O'
            if verbose > 0:
                print(f"Player {c_player} moves from ({move[0][0]}, {move[0][1]}) to ({move[1][0]}, {move[1][1]})")
            self.board.make_move(move)

            current_move_maker, next_move_maker = next_move_maker, current_move_maker

        winner = self.board.get_winner()
        c_winner = 'X (first player)' if winner == 1 else 'O (second player)'
        print(f'{c_winner} won!!!')