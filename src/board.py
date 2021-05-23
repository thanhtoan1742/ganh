import numpy as np


class board:
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
        self.moves = []


    def __str__(self):
        return str(self.board)


    def pretty_print(self):
        lines = [
            '---'.join([
                'X' if cell == 1 else 'O' if cell == -1 else '.'
                 for cell in row
            ])
            for row in self.board
        ]
        s = '\n'.join([
            '   0   1   2   3   4',
            '0  ' + lines[0], 
            '   | \ | / | \ | / |',
            '1  ' + lines[1],
            '   | / | \ | / | \ |',
            '2  ' + lines[2], 
            '   | \ | / | \ | / |',
            '3  ' + lines[3],
            '   | / | \ | / | \ |',
            '4  ' + lines[4]
        ])
        print(s, end='\n\n')


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


    def finished(self):
        return self.get_winner() != 0
            

    def _in_range_(self, x, y):
        return x >= 0 and y >= 0 and x < 5 and y < 5


    def _neighbor_(self, x, y):
        for i in range(8):
            if (x + y)%2 == 1 and i%2 == 1:
                continue

            u = x + board.dx[i]
            v = y + board.dy[i]
            if self._in_range_(u, v):
                yield u, v

    '''
        Return all of opposite pair of spot available
    '''
    def _neighbor_pair_(self, x, y):
        res = []
        for i in range(4):
            ax = x + board.dx[i]
            ay = y + board.dy[i]
            if not self._in_range_(ax, ay):
                continue


            bx = x + board.dx[(i + 4)%8]
            by = y + board.dy[(i + 4)%8]
            if not self._in_range_(bx, by):
                continue


            res.append((ax, ay, bx, by))
        return res


    '''
        Return all of opposite pair of enenmy to be carried
    '''
    def _carry_neighbor_pair_(self, x, y):
        res = []
        for ax, ay, bx, by in self._neighbor_pair_(x, y):
            if self.board[ax][ay] != self.board[bx][by]:
                continue
            if self.board[ax][ay] != 0 - self.current_player:
                continue
            res.append((ax, ay, bx, by))
        return res

    '''
        
    '''
    def _check_open_move_(self, sx, sy, tx, ty):
        if len(self.moves) == 0:
            return True

        (u, v), (_, _) = self.moves[-1]
        if len(self._carry_neighbor_pair_(u, v)) == 0:
            return True

        possible_starting_position = [
            (a, b)
            for a, b in self._neighbor_(u, v)
            if self.board[a][b] == self.get_current_player()
        ]
        if len(possible_starting_position) == 0:
            return True


        return ((sx, sy) in possible_starting_position) and (u == tx) and (v == ty)

    '''
        Get opposite pairs of enenmy to be carried, flip into friendly unit
    '''
    def _check_carry_(self, x, y):
        for ax, ay, bx, by in self._carry_neighbor_pair_(x, y):
            self.board[ax][ay] = self.board[x][y]
            self.board[bx][by] = self.board[x][y]


    def _DFS_(self, x, y):
        self.connected_component[x][y] = self.n_connected_component
        for u, v in self._neighbor_(x, y):
            if self.connected_component[u][v] != 0:
                continue
            if self.board[u][v] == 0:
                self.n_reachable_empty += 1
            if self.board[u][v] == self.board[x][y]:
                self._DFS_(u, v)

    '''
        Check all surrounded enemy node, flip all of surrounded inside enemy node
    '''
    def _check_surround_(self):
        self.connected_component = [[0 for y in range(5)] for x in range(5)]
        self.n_connected_component = 0
        reachable_empty = [-1]
        for x in range(5):
            for y in range(5):
                if self.connected_component[x][y] != 0 or self.board[x][y] == 0:
                    continue
                self.n_reachable_empty = 0
                self.n_connected_component += 1
                self._DFS_(x, y)
                reachable_empty.append(self.n_reachable_empty)

        for x in range(5):
            for y in range(5):
                if reachable_empty[self.connected_component[x][y]] == 0:
                    self.board[x][y] = 0 - self.board[x][y]

    '''
        Check to validate move, then make change to the board, both moves then carry/surround
    '''
    def make_move(self, move):
        (sx, sy), (tx, ty) = move
        # print(f'move from ({sx}, {sy}) to ({tx}, {ty})')

        if self.board[sx][sy] != self.current_player:
            raise Exception('player in starting position does not match current player')
        if self.board[tx][ty] != 0:
            raise Exception('destination is not empty')
        if not (tx, ty) in self._neighbor_(sx, sy):
            raise Exception('destination is not reachable from starting position')

        if not self._check_open_move_(sx, sy, tx, ty):
            raise Exception('player has to play open move')

        self.board[sx][sy] = 0
        self.board[tx][ty] = self.current_player
        self.moves.append(move)

        self._check_carry_(tx, ty)
        self._check_surround_()

        self.current_player = 0 - self.current_player