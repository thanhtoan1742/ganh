import numpy as np, copy
from random import choice

INF = 10000
START_MAX_DEPTH = 3
MID_MAX_DEPTH = 3
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

    return set([(u, v, x, y) for u, v in possible_starting_position])

# Extract the opponent move from 2 consecutive board.
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

    all_possible_moves = set()

    for x, y in pos:
        for u, v in get_cell_value_neighbor(board, 0, x, y):
            all_possible_moves.add((x, y, u, v))
    
    # print(all_possible_moves)
    return all_possible_moves

'''
    DEFINE MOVE STATE FUNCTION
'''

def _in_range_(x, y):
    return x >= 0 and y >= 0 and x < 5 and y < 5


def _neighbor_(x, y):
    for i in range(8):
        if (x + y)%2 == 1 and i%2 == 1:
            continue

        u = x + dx[i]
        v = y + dy[i]
        if _in_range_(u, v):
            yield u, v


def _neighbor_pair_(x, y):
    res = []
    for i in range(4):
        ax = x + dx[i]
        ay = y + dy[i]
        if not _in_range_(ax, ay):
            continue

        bx = x + dx[(i + 4)%8]
        by = y + dy[(i + 4)%8]
        if not _in_range_(bx, by):
            continue

        res.append((ax, ay, bx, by))
    return res


def _carry_neighbor_pair_(board, x, y, player):
    res = []
    for ax, ay, bx, by in _neighbor_pair_(x, y):
        if board[ax][ay] != board[bx][by]:
            continue
        if board[ax][ay] != 0 - player:
            continue
        res.append((ax, ay, bx, by))
    return res


def _check_open_move_(board, sx, sy, tx, ty, last_move, player):

    u, v, _, _ = last_move
    if len(_carry_neighbor_pair_(board, u, v, player)) == 0:
        return True

    possible_starting_position = [
        (a, b)
        for a, b in _neighbor_(u, v)
        if board[a][b] == player
    ]
    if len(possible_starting_position) == 0:
        return True

    return ((sx, sy) in possible_starting_position) and (u == tx) and (v == ty)


def _check_carry_(board, x, y, player):
    for ax, ay, bx, by in _carry_neighbor_pair_(board, x, y, player):
        board[ax][ay] = board[x][y]
        board[bx][by] = board[x][y]
        return board


def _DFS_(board, x, y):
        global connected_component, n_connected_component, reachable_empty, n_reachable_empty
        connected_component[x][y] = n_connected_component
        for u, v in _neighbor_(x, y):
            if connected_component[u][v] != 0:
                continue
            if board[u][v] == 0:
                n_reachable_empty += 1
            if board[u][v] == board[x][y]:
                _DFS_(board, u, v)


connected_component = None
n_connected_component = 0
reachable_empty = [-1]
n_reachable_empty = 0

def _check_surround_(board):
    global connected_component, n_connected_component, reachable_empty, n_reachable_empty

    connected_component = [[0 for y in range(5)] for x in range(5)]
    n_connected_component = 0
    reachable_empty = [-1]
    for x in range(5):
        for y in range(5):
            if connected_component[x][y] != 0 or board[x][y] == 0:
                continue
            n_reachable_empty = 0
            n_connected_component += 1
            _DFS_(board, x, y)
            reachable_empty.append(n_reachable_empty)

    for x in range(5):
        for y in range(5):
            if reachable_empty[connected_component[x][y]] == 0:
                board[x][y] = 0 - board[x][y]

    return board


def make_move(board, move, player, last_move):
    sx, sy, tx, ty = move
    # print(f'move from ({sx}, {sy}) to ({tx}, {ty})')

    new_board = copy.deepcopy(board)

    if new_board[sx][sy] != player:
        raise Exception('player in starting position does not match current player')
    if new_board[tx][ty] != 0:
        raise Exception('destination is not empty')
    if not (tx, ty) in _neighbor_(sx, sy):
        raise Exception('destination is not reachable from starting position')

    if last_move and not _check_open_move_(board, sx, sy, tx, ty, last_move, player):
        raise Exception('player has to play open move')

    new_board[sx][sy] = 0
    new_board[tx][ty] = player

    _check_carry_(new_board, tx, ty, player)
    _check_surround_(new_board)
    return new_board


'''
    DEFINE NEW MINIMAX
'''

def minimax(board, move_list, player, tree_depth):
    """
    Returns the optimal move for the current player on the board.
    """
    if abs(evaluate(board)) == 16: 
        return None
    optimal_move = None
    alpha = -INF  # current_worst_max_possible
    beta = INF   # current_worst_min_possible
    last_move = moves[-1] if len(moves) > 0 else None

    if player == 1:
        v = -INF
        for move in move_list:
            new_board = make_move(board, move, player, last_move)
            new_v = min_value(new_board, alpha, beta, 0 - player, tree_depth, move)
            if new_v > v:
                v = new_v
                alpha = v
                optimal_move = move
    else:
        v = INF
        for move in move_list:
            new_board = make_move(board, move, player, last_move)
            new_v = max_value(new_board, alpha, beta, 0 - player, tree_depth, move)
            if new_v < v:
                v = new_v
                beta = v
                optimal_move = move

    print(f"Minimax player optimal value: {v}")
    return optimal_move


def max_value(board, alpha, beta, player, depth, last_move):
    if abs(evaluate(board)) == 16 or depth == 0:
        return evaluate(board) * (1 + depth / 10)
    v = -INF
    move_list = get_all_possible_move(board, player, last_move)
    for move in move_list:
        new_board = make_move(board, move, player, last_move)
        new_v = min_value(new_board, alpha, beta, 0 - player, depth - 1, move)
        v = max(v, new_v) 
        alpha = max(new_v, alpha)
        if alpha > beta:
            # print(f"Break New: {alpha} {beta}")
            break
    return v


def min_value(board, alpha, beta, player, depth, last_move):
    if abs(evaluate(board)) == 16 or depth == 0:
        return evaluate(board) * (1 + depth / 10)
    v = INF
    move_list = get_all_possible_move(board, player, last_move)
    for move in move_list:
        new_board = make_move(board, move, player, last_move)
        new_v = max_value(new_board, alpha, beta, 0 - player, depth - 1, move)
        v = min(v, new_v)
        beta = min(new_v, beta)
        if beta < alpha:
            # print(f"Break New: {alpha} {beta}")
            break
    return v


def evaluate(board):
    sum = 0
    for i in range(5):
        for j in range(5):
            sum += board[i][j]
    return sum


def move(board_ndarray, player):
    global last_board
    board_ndarray = np.array(board_ndarray)
    update_board_opponent_turn(board_ndarray)

    if len(moves) > 0:
        last_move = moves[-1]
    else:
        last_move = None

    all_moves = get_all_possible_move(board_ndarray, player, last_move)

    if evaluate(board_ndarray) * player < 12: 
        # Opponent has more than 2 units left
        optimal_move = minimax(board_ndarray, all_moves, player, START_MAX_DEPTH)
    elif evaluate(board_ndarray) * player < 14: 
        # Opponent has 2 units left
        optimal_move = minimax(board_ndarray, all_moves, player, MID_MAX_DEPTH)
    else:   
        # Opponent has one unit left
        optimal_move = minimax(board_ndarray, all_moves, player, END_MAX_DEPTH)
    x, y, u, v = optimal_move
    update_board_my_turn(board_ndarray, (x, y, u, v))
    return (x, y), (u, v)