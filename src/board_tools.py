from __future__ import print_function
import sys
import numpy as np

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


N_ROW = 5
N_COL = 5

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]


def is_in_range(x, y):
    return x >= 0 and y >= 0 and x < N_ROW and y < N_COL


def get_neighbor(x, y):
    res = []
    for i in range(8):
        if (x + y)%2 == 1 and i%2 == 1:
            continue

        u = x + dx[i]
        v = y + dy[i]
        if is_in_range(u, v):
            res.append((u, v))
    return res


"""
Return all pair of neighbors that:
- Inside the board
- Are symmetric with respect to (x, y)
"""
def get_symmetric_neighbor_pair(x, y):
    res = []
    for i in range(4):
        ax = x + dx[i]
        ay = y + dy[i]
        if not is_in_range(ax, ay):
            continue

        bx = x + dx[(i + 4)%8]
        by = y + dy[(i + 4)%8]
        if not is_in_range(bx, by):
            continue

        res.append((ax, ay, bx, by))
    return res


"""
Return all pair of carry neighbors of (x, y) that both cell 
has the value = value arguement.
"""
def get_symmetric_neighbor_pair_with_value(board, x, y, value):
    res = []
    for ax, ay, bx, by in get_symmetric_neighbor_pair(x, y):
        if board[ax][ay] != board[bx][by]:
            continue
        if board[ax][ay] != value:
            continue
        res.append((ax, ay, bx, by))
    return res


"""
Return all position that is neighbor of (x, y) and have the same
value = value arguement.
"""
def get_neighbor_with_value(board, x, y, value):
    res = []
    for u, v in get_neighbor(x, y):
        if board[u][v] == value:
            res.append((u, v))
    return res


"""
Return all position of a with value = value argument.
"""
def get_position_with_value(board, value):
    pos = []
    for x in range(N_ROW):
        for y in range(N_COL):
            if board[x][y] != value:
                continue
            
            pos.append((x, y))
    return pos

    
def get_score(board):
    return sum(board.flatten())



def _DFS_(board, x, y, mask, ncc):
    mask[x][y] = ncc
    for u, v in get_neighbor_with_value(board, x, y, board[x][y]):
        if mask[u][v] == 0:
            _DFS_(board, u, v, mask, ncc)


def get_connected_component_mask(board):
    mask = np.zeros((N_ROW, N_COL), dtype=int)
    ncc = 0
    for x in range(N_ROW):
        for y in range(N_COL):
            if mask[x][y] == 0:
                ncc += 1
                _DFS_(board, x, y, mask, ncc)

    return mask


'''
Flip all cells with value = value argument which are surrounded by 
cells with vale = 0 - value argument.
'''
def _update_surround_(board, value):
    mask = get_connected_component_mask(board)
    ncc = max(mask.flatten()) + 1

    is_reachable_empties = np.zeros(ncc, dtype=bool)
    for x in range(N_ROW):
        for y in range(N_COL):
            if len(get_neighbor_with_value(board, x, y, 0)) > 0:
                is_reachable_empties[mask[x][y]] = 1

    for x in range(N_ROW):
        for y in range(N_COL):
            if board[x][y] != value:
                continue

            if not is_reachable_empties[mask[x][y]]:
                board[x][y] = 0 - value


'''
Get opposite pairs of opponent's pieces to be carried, flip into friendly pieces.
'''
def _update_carry_(board, x, y):
    for ax, ay, bx, by in get_symmetric_neighbor_pair_with_value(board, x, y, 0 - board[x][y]):
        board[ax][ay] = board[x][y]
        board[bx][by] = board[x][y]


'''
Apply a valid move to the board.
'''
def apply_move(board, move):
    sx, sy, tx, ty = move

    board[tx][ty] = board[sx][sy]
    board[sx][sy] = 0
    
    _update_carry_(board, tx, ty)
    _update_surround_(board, 0 - board[tx][ty])


def get_initial_board():
    return np.array([
        [ 1,  1,  1,  1,  1],
        [ 1,  0,  0,  0,  1],
        [ 1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1],
    ])


def is_initial_board(board):
    return (board == get_initial_board()).all()


def get_pretty_string(board):
    lines = [
        '---'.join([
            'X' if cell == 1 else 'O' if cell == -1 else '.'
                for cell in row
        ])
        for row in board
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
    return s


