import numpy as np, copy
from board import *
from random import choice

INF = 10000
START_MAX_DEPTH = 3
END_MAX_DEPTH = 3

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

last_board = np.eye(1)
moves = []
counter = 0

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

# Return open move list if there is one, otherwise return None.
def get_open_moves(board, player, last_move):
    x, y, _, _ = last_move
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

    # print(f"Last board:\n {last_board}\n")
    # print(f"Board:\n {board}\n")

    # print(f"pos: {pos}")
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


def get_all_possible_move(board, player, last_move):
    # print(last_move)
    # print(board)
    # print(player)
    if last_move:
        open_moves = get_open_moves(board, player, last_move)
        # If open moves exist, return only open moves
        if len(open_moves) > 0:
            return open_moves

    # Else return all possible move of all current player position
    pos = get_player_position(board, player)
    # print(pos)
    if len(pos) == 0:
        return

    all_possible_moves = []

    for x, y in pos:
        for u, v in get_cell_value_neighbor(board, 0, x, y):
            all_possible_moves.append((x, y, u, v))
    
    # print(all_possible_moves)
    return all_possible_moves


def utility(board):
    win = board.get_winner()
    if win == 1:
        return INF
    elif win == -1:
        return -INF
    else:
        return 0


def minimax(board, move_list, player):
    global counter
    counter += 1
    # print(f"Counter: {counter}")
    """
    Returns the optimal move for the current player on the board.
    """
    if board.finished(): 
        return None
    optimal_move = None
    current_worst_max_possible = -INF  # alpha
    current_worst_min_possible = INF   # beta 

    
    if player == 1:
        v = -INF
        for move in move_list:
            new_board = copy.deepcopy(board)
            x1, y1, x2, y2 = move
            new_board.make_move(((x1,y1),( x2,y2)))
            new_v = min_value(new_board, current_worst_max_possible, current_worst_min_possible, 0 - player, 0)
            if new_v > v:
                v = new_v
                current_worst_max_possible = v
                optimal_move = move
    else:
        v = INF
        for move in move_list:
            new_board = copy.deepcopy(board)
            x1, y1, x2, y2 = move
            new_board.make_move(((x1,y1),( x2,y2)))
            new_v = max_value(new_board, current_worst_max_possible, current_worst_min_possible, 0 - player, 0)
            if new_v < v:
                v = new_v
                current_worst_min_possible = v
                optimal_move = move
    return optimal_move


def max_value(board, current_worst_max_possible, current_worst_min_possible, player, depth):
    global counter
    if board.finished():
        return utility(board)
    if counter < 25:
        if depth == START_MAX_DEPTH:
            return evaluate(board)
    else:
        if depth == END_MAX_DEPTH:
            return evaluate(board)
    v = -INF
    start, end = board.moves[-1]
    x1, y1 = start
    x2, y2 = end
    move_list = get_all_possible_move(board.board, player, (x1,y1,x2,y2))
    for move in move_list:
        new_board = copy.deepcopy(board)
        x1, y1, x2, y2 = move
        new_board.make_move(((x1,y1),( x2,y2)))
        new_v = min_value(new_board, current_worst_max_possible, current_worst_min_possible, 0 - player, depth + 1)
        if new_v > current_worst_min_possible:
            return new_v
        v = max(v, new_v) 
        current_worst_max_possible = v
    return v


def min_value(board, current_worst_max_possible, current_worst_min_possible, player, depth):
    global counter
    if board.finished():
        return utility(board)
    if counter % 3 == 0:
        if depth == START_MAX_DEPTH:
            return evaluate(board)
    else:
        if depth == END_MAX_DEPTH:
            return evaluate(board)
    v = INF
    start, end = board.moves[-1]
    x1, y1 = start
    x2, y2 = end
    move_list = get_all_possible_move(board.board, player, (x1,y1,x2,y2))
    for move in move_list:
        new_board = copy.deepcopy(board)
        x1, y1, x2, y2 = move
        new_board.make_move(((x1,y1),( x2,y2)))
        new_v = max_value(new_board, current_worst_max_possible, current_worst_min_possible, 0 - player, depth + 1)
        if new_v < current_worst_max_possible:
            return new_v
        v = min(v, new_v)
        current_worst_min_possible = v
    return v


def evaluate(board):
    sum = 0
    for i in range(5):
        for j in range(5):
            sum += board.board[i][j]
    return sum



def move(board_ndarray, player):
    global last_board, counter
    board_ndarray = np.array(board_ndarray)
    update_board_opponent_turn(board_ndarray)

    if len(moves) > 0:
        last_move = moves[-1]
    else:
        last_move = None

    all_moves = get_all_possible_move(board_ndarray, player, last_move)
    board_class = board()
    board_class.board = board_ndarray
    board_class.current_player = player

    optimal_move = minimax(board_class, all_moves, player)
    x, y, u, v = optimal_move
    update_board_my_turn(board_ndarray, (x, y, u, v))
    return (x, y), (u, v)