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
has the value of cell_value.
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
value of cell_value
"""
def get_neighbor_with_value(board, x, y, value):
    res = []
    for u, v in get_neighbor(x, y):
        if board[u][v] == value:
            res.append((u, v))
    return res


"""
Return all position of a player.
"""
def get_position_with_value(board, value):
    pos = []
    for x in range(N_ROW):
        for y in range(N_COL):
            if board[x][y] != value:
                continue
            
            pos.append((x, y))
    return pos

