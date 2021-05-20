from random_player import in_range, neighbor, empty_neighbor

def move(board, player):
    x, y, u, v, = [int(e) for e in input().strip().split()]
    return (x, y), (u, v)
