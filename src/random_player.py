from random import choice

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

def in_range(x, y):
    return x >= 0 and y >= 0 and x < 5 and y < 5

def neighbor_pair(x, y):
    res = []
    for i in range(4):
        ax = x + dx[i]
        ay = y + dy[i]
        if not in_range(ax, ay):
            continue

        bx = x + dx[(i + 4)%8]
        by = y + dy[(i + 4)%8]
        if not in_range(bx, by):
            continue

        res.append((ax, ay, bx, by))
    return res

def carry_neighbor_pair(board, player, x, y):
    res = []
    for ax, ay, bx, by in neighbor_pair(x, y):
        if board[ax][ay] != board[bx][by]:
            continue
        if board[ax][ay] != 0 - player:
            continue
        res.append((ax, ay, bx, by))
    return res

def open_moves(board, player):
    res = []
    for x in range(5):
        for y in range(5):
            if board[x][y] != player:
                continue

            for u, v in neighbor(x, y):
                if board[u][v] != 0:
                    continue

                if len(carry_neighbor_pair(board, player, u, v)) > 0:
                    res.append((x, y, u, v))
    return res


def neighbor(x, y):
    res = []
    for i in range(8):
        if (x + y)%2 == 1 and i%2 == 1:
            continue

        u = x + dx[i]
        v = y + dy[i]
        if in_range(u, v):
            res.append((u, v))
    return res


def empty_neighbor(board, x, y):
    res = []
    for u, v in neighbor(x, y):
        if board[u][v] == 0:
            res.append((u, v))
    return res


def move(board, player):
    ss = open_moves(board, player)
    print(f'random player ({player}) open moves:')
    print(ss)
    if len(ss) > 0:
        x, y, u, v = choice(ss)
        return (x, y), (u, v)

    ss = []
    for x in range(5):
        for y in range(5):
            if board[x][y] != player:
                continue
            
            if len(empty_neighbor(board, x, y)) == 0:
                continue

            ss.append((x, y))
    if len(ss) == 0:
        return

    x, y = choice(ss)
    u, v = choice(empty_neighbor(board, x, y))
    return (x, y), (u, v)