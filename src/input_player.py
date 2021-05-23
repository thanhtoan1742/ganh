from random_player_for_input_player import get_open_moves

def move(board, player):
    ss = get_open_moves(board, player)
    print('your open moves are: ')
    print(ss)
    x, y, u, v, = [int(e) for e in input().strip().split()]
    return (x, y), (u, v)
