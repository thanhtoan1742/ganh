from random import choice

def in_range(x, y):
    return x >= 0 and y >= 0 and x < 5 and y < 5

def neighbor(x, y):
    res = []
    dx = [-1, -1, 0, 1, 1, 1, 0, -1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]

    for i in range(0, 8, 2):
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

if __name__ == '__main__':
    from board import board
    b = board().board.copy()
    print(move(b, 1))