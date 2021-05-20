from random_player import open_moves

def move(board, player):
    ss = list(open_moves(board, player))
    print('your open moves are: ')
    print(ss)
    x, y, u, v, = [int(e) for e in input().strip().split()]
    return (x, y), (u, v)
