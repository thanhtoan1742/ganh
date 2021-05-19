import numpy as np

class board:
    def __init__(self):
        self.board = np.array([
            [ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1],
        ])
        self.current_player = 1

    def __str__(self):
        return str(self.board)

    def pretty_print(self):
        print(
            '\n' + 
            '\n'.join([
                ' '.join(['X' if e == 1 else 'O' if e == -1 else '.'
                    for e in row])
                for row in self.board
            ]) + 
            '\n'
        )

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board

    def make_move(self, move):
        ###
        self.current_player = 0 - self.current_player

    def finished(self):
        return False