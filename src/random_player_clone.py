from random import choice
import numpy as np

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

last_board = np.eye(1)
moves = []

def is_in_range(x, y):
    return x >= 0 and y >= 0 and x < 5 and y < 5

def get_neighbor_pair(x, y):
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

# Return all pair of carry neighbors of (x, y) that both cell 
# has the value of cell_value.
def get_carry_cell_value_neighbor_pair(board, cell_value, x, y):
    res = []
    for ax, ay, bx, by in get_neighbor_pair(x, y):
        if board[ax][ay] != board[bx][by]:
            continue
        if board[ax][ay] != cell_value:
            continue
        res.append((ax, ay, bx, by))
    return res

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


# Return all position that is neighbor of (x, y) and have the same
# value of cell_value
def get_cell_value_neighbor(board, cell_value, x, y):
    res = []
    for u, v in get_neighbor(x, y):
        if board[u][v] == cell_value:
            res.append((u, v))
    return res



# Return all position of a player.
def get_player_position(board, player):
    pos = []
    for x in range(5):
        for y in range(5):
            if board[x][y] != player:
                continue
            
            # get all neighbor empty cell.
            if len(get_cell_value_neighbor(board, 0, x, y)) == 0:
                continue

            pos.append((x, y))
    return pos



# We are playing a new game if we are playing on first or second turn.
# Check the n.o. our pieces or oppenent's piece increases.
# FIXME: This is wrong when player loses pieces (the n.o pieces decrease) then
# gains pieces again (the n.o pieces increase).
def is_new_game(last_board, board):
    if (last_board == np.eye(1)).all():
        return True
    return False

    clp = sum(last_board.flatten() == 1)
    cln = sum(last_board.flatten() == -1)
    cp = sum(board.flatten() == 1)
    cn = sum(board.flatten() == -1)

    return cp > clp or cn > cln


# Return open move list if there is one, otherwise return None.
def get_open_moves(board, player):
    global moves
    if len(moves) == 0:
        return []

    x, y, _, _ = moves[-1]
    possible_starting_position = get_cell_value_neighbor(board, player, x, y)
    if len(possible_starting_position) == 0:
        return []
    carry_neighbor_pair = get_carry_cell_value_neighbor_pair(board, 0 - player, x, y)
    if len(carry_neighbor_pair) == 0:
        return []

    return [(u, v, x, y) for u, v in possible_starting_position]


# Extract the opponent move from 2 consecutive board.
# FIXME: wrong when there is carry or surround aka pieces changing side.
def extract_opponent_move(last_board, board):
    pos = [
        (x, y) 
        for y in range(5) 
        for x in range(5) 
        if abs(board[x][y]) != abs(last_board[x][y])
    ]

    (x, y), (u, v) = pos
    if board[x][y] != 0:
        x, y, u, v = u, v, x, y

    return x, y, u, v


def get_initial_board():
    return np.array([
        [ 1,  1,  1,  1,  1],
        [ 1,  0,  0,  0,  1],
        [ 1,  0,  0,  0, -1],
        [-1,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1],
    ])


def is_initial_board(board):
    initial_board = get_initial_board()
    return (initial_board == board).all()

    
# If we are playing a new game then reset moves list and add the opponent
# move to the moves list if it exist. Otherwise, we just add the opponent
# move the the moves list.
# The opponent move is calculated from last_board and board.
def update_board_opponent_turn(board):
    global last_board, moves
    if is_new_game(last_board, board):
        moves = []
        # If we play the first turn the do nothing.
        # Else we set last_board to initial board
        if is_initial_board(board):
            return
        last_board = get_initial_board()

    opponent_move = extract_opponent_move(last_board, board)
    moves.append(opponent_move)


# Set last_board to the state after we make our move.
def update_board_my_turn(board, move):
    global last_board, moves
    x, y, u, v = move
    moves.append(move)
    last_board = board
    last_board[u][v] = last_board[x][y]
    last_board[x][y] = 0


def move(board, player):
    global last_board
    board = np.array(board)
    update_board_opponent_turn(board)

    # If open moves exist, randomly chose 1 play it.
    open_moves = get_open_moves(board, player)
    if len(open_moves) > 0:
        op = choice(open_moves)
        update_board_my_turn(board, op)
        return (op[0], op[1]), (op[2], op[3])
       
    # Randomly chose a starting position then randomly chose a destination.
    pos = get_player_position(board, player)
    if len(pos) == 0:
        return
    x, y = choice(pos)
    u, v = choice(get_cell_value_neighbor(board, 0, x, y))

    update_board_my_turn(board, (x, y, u, v))
    return (x, y), (u, v)