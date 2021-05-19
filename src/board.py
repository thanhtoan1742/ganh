import numpy as np

class board:

    #   7 0 1
    #   6   2
    #   5 4 3
    dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

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
                ' '.join(['X' if cell == 1 else 'O' if cell == -1 else '.'
                    for cell in row])
                for row in self.board
            ]) + 
            '\n'
        )

    def get_current_player(self):
        return self.current_player

    def get_board(self):
        return self.board

    def finished(self):
        n_first_player_pieces = sum(self.board.flatten() == 1)
        n_second_player_pieces = sum(self.board.flatten() == -1)
        return n_first_player_pieces == 0 or n_second_player_pieces == 0

    def _in_range_(self, coord):
        x, y = coord
        return x >= 0 and y >= 0 and x < 5 and y < 5

    #   3 0 1
    #   2   2
    #   1 0 3
    def _carrial_neighbor_pair_(self, coord):
        x, y = coord
        for i in range(4):
            ax = x + board.dx[i]
            ay = y + board.dy[i]
            if not self._in_range_((ax, ay)):
                continue

            bx = x + board.dx[(i + 4)%8]
            by = y + board.dy[(i + 4)%8]
            if not self._in_range_((bx, by)):
                continue

            yield (ax, ay), (bx, by)


    def _neigbor_(self, coord):
        x, y = coord
        for i in range(0, 8, 2):
            if (x + y)%2 == 1 and i%2 == 1:
                continue

            u = x + board.dx[i]
            v = y + board.dy[i]
            if self._in_range_((u, v)):
                yield u, v


    def _check_carry_(self, coord):
        x, y = coord
        for (ax, ay), (bx, by) in self._carrial_neighbor_pair_(coord):
            if self.board[ax][ay] != self.board[bx][by]:
                continue
            if self.board[ax][ay] == self.board[x][y]:
                continue

            self.board[ax][ay] = self.board[x][y]
            self.board[bx][by] = self.board[x][y]

    # TODO: check for open and force the open move.
    def make_move(self, move):
        (sx, sy), (tx, ty) = move
        if self.board[sx][sy] != self.current_player:
            raise KeyError('player in starting position does not match current player')
        if self.board[tx][ty] != 0:
            raise KeyError('destination is not empty')
        if not (tx, ty) in self._neigbor_((sx, sy)):
            raise KeyError('destination is not reachable from starting position')


        self.board[sx][sy] = 0
        self.board[tx][ty] = self.current_player

        self._check_carry(tx, ty)
        self._check_surround(tx, ty)

        self.current_player = 0 - self.current_player
