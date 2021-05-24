from math import log, sqrt
import time
import random
import copy

def time_remained(secs = 2.9):
    """ Closure: check remaining time """
    start = time.time()
    def check():
        return (time.time() - start) < secs
    return check

def board_game(player = 1, parent = None, board = None, previous_move = None, parent_simulate_sum = None, bonus = None):
    """ Closure: game board """
    data = [[ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1]] if board is None else board
    self = None
    children = []
    win = 0
    visited = [0 if bonus is None else bonus] if parent_simulate_sum is None else parent_simulate_sum
    value = 0
    opponent = 0 - player
    random.seed()
    result = 0

    def neighbour_list(pos):
        """ Return list of neighbour positions of a position """
        temp = []
        relative = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if (pos[0] + pos[1]) % 2 == 0:
            relative.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        for i in relative:
            new_pos = (pos[0] + i[0], pos[1] + i[1])
            if new_pos[0] >= 0 and new_pos[0] <= 4 and new_pos[1] >= 0 and new_pos[1] <= 4:
                temp.append(new_pos)
        return temp

    def valid_pos(pos):
        """ Check if a position is valid """
        return pos[0] >= 0 and pos[0] <= 4 and pos[1] >= 0 and pos[1] <= 4

    def occupied(pos):
        """ Check if the position is occupied """
        nonlocal data
        return data[pos[0]][pos[1]] != 0

    def can_carry(pos):
        """ Check if carrying can be performed in the position """
        if occupied(pos):
            return False
        neighbours = neighbour_list(pos)
        nonlocal data
        for x, y in neighbours:
            op_pos = (2*pos[0] - x, 2*pos[1] - y)
            if valid_pos(op_pos):
                if data[op_pos[0]][op_pos[1]] == data[x][y] and data[x][y] == opponent:
                    return True
        return False

    def swap(start, end, add = True):
        """ Return a new board with start and end positions swapped """
        nonlocal data
        if not add:
            new_data = data
        else:
            new_data = copy.deepcopy(data)
        start_value = new_data[start[0]][start[1]]
        end_value = new_data[end[0]][end[1]]
        new_data[start[0]][start[1]] = end_value
        new_data[end[0]][end[1]] = start_value
        return new_data

    def is_end():
        """ Check if game ends. Return 1 if win, -1 if lose and 0 if not end """
        sum = 0
        for x in range(5):
            for y in range(5):
                sum += data[x][y]
        if sum == 16 or sum == -16:
            return 1 if sum > 0 else -1
        else:
            return 0

    def all_moves():
        """ List of all possible moves """
        temp = []
        nonlocal data

        if is_end() != 0:
            return temp

        if previous_move is not None:
            pos = previous_move[0]
            if can_carry(pos):
                neighbours = neighbour_list(pos)
                for x, y in neighbours:
                    if data[x][y] == player:
                        temp.append(((x, y), pos))
                if len(temp) > 0:
                    return temp

        for x in range(5):
            for y in range(5):
                if data[x][y] == player:
                    neighbours = neighbour_list((x, y))
                    for pos in neighbours:
                        if not occupied(pos):
                            temp.append(((x, y), pos))
        return temp

    can_move = all_moves()

    def move_applied(move, add = True):
        """ Return the new board after applying move """
        start, end = move
        new_data = swap(start, end, add)
        add_value = 0

        def surround(end):
            """ Apply surrounding to board at end point """
            nonlocal new_data
            neighbours = [(x, y) for x, y in neighbour_list(end) if new_data[x][y] == opponent]

            def surround_recurse(pos, visited = None):
                """ Recursive surrounding """
                nonlocal add_value
                if visited is None:
                    _visited = set()
                else:
                    _visited = visited
                _visited.add(pos)
                neighbours = neighbour_list(pos)
                for x, y in neighbours:
                    if new_data[x][y] == 0:
                        return False
                flag = True
                for x, y in neighbours:
                    if new_data[x][y] == opponent and (x, y) not in _visited:
                        flag = surround_recurse((x, y), _visited)
                        if flag == False:
                            return False
                if flag == True and visited is None:
                    for x, y in _visited:
                        new_data[x][y] = player
                        add_value += 0.05
                return True

            for pos in neighbours:
                surround_recurse(pos)

        def carry(end):
            """ Apply carrying to board at end point """
            new_surround = []
            nonlocal new_data
            nonlocal add_value
            neighbours = neighbour_list(end)
            for x, y in neighbours:
                if new_data[x][y] == opponent:
                    op = (2*end[0] - x, 2*end[1] - y)
                    if valid_pos(op):
                        if new_data[op[0]][op[1]] == opponent:
                            new_data[op[0]][op[1]] = player
                            new_data[x][y] = player
                            new_surround.append((x, y))
                            new_surround.append(op)
                            add_value += 0.1
            for pos in new_surround:
                surround(pos)

        carry(end)
        surround(end)

        nonlocal data
        old_data = data
        data = new_data
        nonlocal player
        nonlocal opponent
        player = 0 - player
        opponent = 0 - opponent
        for _x in range(5):
            for _y in range(5):
                start = (_x, _y)
                if can_carry(start):
                    neighbours = neighbour_list(start)
                    for x, y in neighbours:
                        if data[x][y] == opponent:
                            add_value -= 0.14
                            break
        data = old_data
        player = 0 - player
        opponent = 0 - opponent
        return new_data, add_value

    def best_child():
        """ Get best child """
        best = None
        if len(children) > 0:
            best = children[random.randint(0, len(children) - 1)]
        for child in children:
            if best == None:
                best = child
            elif best("get_value") < child("get_value"):
                best = child
        return best

    def random_expand(add = True):
        """ Expand with random move and return new child """
        index = random.randint(0 , len(can_move) - 1)
        move = can_move[index]
        if add:
            can_move[index: index + 1] = []
        new_board, bonus = move_applied(move, add)
        child = board_game(player = opponent, parent = self, board = new_board, previous_move = move, parent_simulate_sum = visited, bonus = bonus)
        child("set_self", child)
        if add:
            children.append(child)
        return child

    def update_value(result):
        """ Update value upon win/lose \n
        UCT value = win / visited + sqrt(2 * ln parent_simulate_sum / visited)"""
        nonlocal value
        nonlocal visited
        nonlocal win
        visited[0] += 1
        win += result * player
        value = win / visited[0] + (0 if bonus is None else bonus) #+ sqrt(2 * log(parent_simulate_sum[0] if parent_simulate_sum is not None else visited[0]) / visited[0])

    def traverse():
        """ Combination of selection and expansion. Traverse the tree """
        child = self
        while child("is_fully_expand") and child("get_result") == 0:
            child = child("get_best_child")
        return child("expand") if child("get_result") == 0 else child

    def simulation():
        """ Simulation. Simulate a game until win """
        child = self
        step = 0
        nonlocal data
        old_data = copy.deepcopy(data)
        while child("get_result") == 0 and step < 1000:
            child = child("expand", False)
            step += 1
        data = old_data
        return child("get_result")

    def backpropagation(value):
        """ Backpropagation. Update value from node to root """
        parent = self
        while parent is not None:
            parent("update_value", value)
            parent = parent("get_parent")

    def action(*action):
        """ Perform action:
        - "get_value": return value
        - "get_move": get move from parent to this
        - "set_self", self: self initializing
        - "update_value", value: update UCT value
        - "get_parent": return parent
        - "is_fully_expand": return True if node is fully expanded, otherwise return False
        - "get_best_child": return child with highest uct value
        - "expand": randomly expand
        - "get_result": get result at node
        - "simulate": simulate
        - "iterate": update all tree in one cycle
        - "backpropagate": backpropagate """
        if action[0] == "get_value":
            return value
        if action[0] == "get_move":
            return previous_move
        if action[0] == "set_self":
            nonlocal self
            self = action[1]
            nonlocal result
            result = is_end()
            return
        if action[0] == "update_value":
            update_value(action[1])
            return
        if action[0] == "get_parent":
            return parent
        if action[0] == "is_fully_expand":
            return len(can_move) == 0
        if action[0] == "get_best_child":
            return best_child()
        if action[0] == "expand":
            return random_expand() if len(action) == 1 else random_expand(False)
        if action[0] == "get_result":
            return result
        if action[0] == "simulate":
            return simulation()
        if action[0] == "backpropagate":
            backpropagation(action[1])
            return
        if action[0] == "iterate":
            node = traverse()
            _value = node("simulate")
            node("backpropagate", _value)
            return
        if action[0] == "get_board":
            return data
        if action[0] == "test":
            if action[1] not in can_move:
                print(can_move)
                print(action[1])
                return None
            return move_applied(action[1])[0]
        if action[0] == "visit":
            return visited[0]
        raise "No action!"

    return action

if __name__ == "__main__":
    test = board_game(previous_move=((3, 2), (2, 2)))