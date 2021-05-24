from monte_functions import *

game_board = [[ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1]]

def get_previous_move(pre_board, now_board):
    start = None
    end = None
    for x in range(5):
        for y in range(5):
            comp1 = pre_board[x][y]
            comp2 = now_board[x][y]
            if not (comp1 == comp2 or comp1 + comp2 == 0):
                if comp2 == 0:
                    start = (x, y)
                else:
                    end = (x, y)
    if start is None:
        return None
    return (start, end)

def move(board, player):
    global game_board
    previous_move = get_previous_move(game_board, board)
    resource_remained = time_remained()
    game = board_game(player = player, board = board, previous_move = previous_move)
    game("set_self", game)
    while resource_remained():
        game("iterate")
    if game("get_result") == 0:
        get_move = game("get_best_child")("get_move")
    else:
        get_move = None
    game_board = game("get_best_child")("get_board")
    return get_move

if __name__ == "__main__":
    print(move(
        [[ 1,  1,  1,  1,  1],
        [ 1,  0,  0,  0,  1],
        [ 1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1]], 1
    ))
