import time
import random
import numpy as np

POS_INFTY = 1000
NEG_INFTY = -1000

def time_remained(secs = 2.7):
    """ Closure: check remaining time """
    start = time.time()
    def check():
        return (time.time() - start) < secs
    return check

def list_changed(input, x, y, value):
    """ Return a new list of list with input[x][y] = value """
    row = input[x].tolist()
    row = row[:y] + [value] + row[y + 1:]
    output = input[:x].tolist() + [row] + input[x + 1:].tolist()
    return np.array(output)

class Node:
    def __init__(self, board, player = 1, parent = None, previous_move = None, height = 0, force_carry = None):
        """ Initialize node """
        self.board = board
        self.player = player
        self.opponent = 0 - player
        self.previous_move = previous_move
        self.parent = parent
        def get_value():
            sum = 0
            for i in board:
                for j in i:
                    sum += j
            return sum * player
        self.value = get_value()
        self.children = []
        self.height = height
        self.isExpand = False
        self.force_carry = force_carry if force_carry is not None else (False if parent is None else parent.value == self.value)

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

    def can_carry(self, pos):
        """ Check if carrying can be performed in the position """
        neighbours = Node.neighbour_list(pos)
        for x, y in neighbours:
            op_pos = (2*pos[0] - x, 2*pos[1] - y)
            if Node.valid_pos(op_pos):
                if self.board[op_pos[0]][op_pos[1]] == self.opponent and self.board[x][y] == self.opponent:
                    return True
        return False

    def apply_move(self, move):
        start, end = move
        output = self.board
        start_val = output[start[0]][start[1]]
        end_val = output[end[0]][end[1]]
        output = list_changed(output, start[0], start[1], end_val)
        output = list_changed(output, end[0], end[1], start_val)
        def surround(end):
            """ Apply surrounding to board at end point """
            nonlocal output
            neighbours = [(x, y) for x, y in Node.neighbour_list(end) if output[x][y] == self.opponent]

            def surround_recurse(pos, visited = None):
                """ Recursive surrounding """
                nonlocal output
                if visited is None:
                    _visited = set()
                else:
                    _visited = visited
                _visited.add(pos)
                neighbours = Node.neighbour_list(pos)
                for x, y in neighbours:
                    if output[x][y] == 0:
                        return False
                flag = True
                for x, y in neighbours:
                    if output[x][y] == self.opponent and (x, y) not in _visited:
                        flag = surround_recurse((x, y), _visited)
                        if flag == False:
                            return False
                if flag == True and visited is None:
                    for x, y in _visited:
                        output = list_changed(output, x, y, self.player)
                return True

            for pos in neighbours:
                surround_recurse(pos)
        def carry(end):
            """ Apply carrying to board at end point """
            new_surround = []
            nonlocal output
            neighbours = Node.neighbour_list(end)
            for x, y in neighbours:
                if output[x][y] == self.opponent:
                    op = (2*end[0] - x, 2*end[1] - y)
                    if Node.valid_pos(op):
                        if output[op[0]][op[1]] == self.opponent:
                            output = list_changed(output, op[0], op[1], self.player)
                            output = list_changed(output, x, y, self.player)
                            new_surround.append((x, y))
                            new_surround.append(op)
            for pos in new_surround:
                surround(pos)
        carry(end)
        surround(end)
        return output
    
    def expand(self):
        # if self.force_carry:
        if True:
            if self.can_carry(self.previous_move[0]):
                start = self.previous_move[0]
                neighbours = Node.neighbour_list(start)
                for x, y in neighbours:
                    if self.board[x][y] == self.player:
                        self.children.append(Node(self.apply_move(((x, y), start)), self.opponent, self, ((x, y), start), self.height + 1))
            if len(self.children) > 0:
                random.shuffle(self.children)
                self.isExpand = True
                return

        for x in range(5):
            for y in range(5):
                if self.board[x][y] == self.player:
                    neighbours = Node.neighbour_list((x, y))
                    for _x, _y in neighbours:
                        if self.board[_x][_y] == 0:
                            move = ((x, y), (_x, _y))
                            self.children.append(Node(self.apply_move(move), self.opponent, self, move, self.height + 1))
        random.shuffle(self.children)
        self.isExpand = True

def minimax_ab_cutoff(root: Node, maxplayer, alpha, beta, depth, resource):
    if maxplayer:
        if root.height == depth:
            return root.value
        if root.value == 16 or root.value == -16:
            return root.value
        best = NEG_INFTY
        if not resource():
            return best
        if not root.isExpand:
            root.expand()
        if not resource():
            return best
        for child in root.children:
            val = minimax_ab_cutoff(child, not maxplayer, alpha, beta, depth, resource)
            best = max(best, val)
            alpha = max(best, alpha)
            if beta <= alpha:
                break
        root.value = best
        return best
    else:
        if root.height == depth:
            return 0 - root.value
        if root.value == 16 or root.value == -16:
            return 0 - root.value
        best = POS_INFTY
        if not resource():
            return best
        if not root.isExpand:
            root.expand()
        if not resource():
            return best
        for child in root.children:
            val = minimax_ab_cutoff(child, not maxplayer, alpha, beta, depth, resource)
            best = min(best, val)
            beta = min(best, beta)
            if beta <= alpha:
                break
        root.value = 0 - best
        return best   

def iterdeep_minimax(root: Node, resource, fixed_depth = None):
    if fixed_depth is None:
        depth = 2
        while resource() and depth <= 4:
            val = minimax_ab_cutoff(root, True, NEG_INFTY, POS_INFTY, depth, resource)
            depth += 1
            if not resource():
                break
            best_child = root.children[0]
            for child in root.children:
                if 0 - best_child.value < 0 - child.value:
                    best_child = child
            if val == 16:
                break
    else:
        minimax_ab_cutoff(root, True, NEG_INFTY, POS_INFTY, fixed_depth, resource)
        best_child = root.children[0]
        for child in root.children:
            if 0 - best_child.value < 0 - child.value:
                best_child = child
    return best_child.board, best_child.previous_move

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
        return None, None
    def sum_list(temp):
        sum = 0
        for i in temp:
            for j in i:
                sum += j
        return sum
    return (start, end), sum_list(pre_board) == sum_list(now_board)

def move(board, player):
    global game_board
    previous_move, force_carry = get_previous_move(game_board, board)
    resource_remained = time_remained()
    root = Node(board = board, player = player, previous_move = previous_move, force_carry = force_carry)
    game_board, get_move = iterdeep_minimax(root = root, resource = resource_remained)
    return get_move

if __name__ == "__main__":
    # node = Node(
    #     list([
    #         [ 1,  0,  1,  0,  0],
    #         [ 1, -1,  1,  0,  0],
    #         [-1, -1,  1,  0, -1],
    #         [-1, -1,  0,  1, -1],
    #         [-1,  1,  1,  0,  0]
    #     ]), -1, previous_move = ((3,2),(2,2)), force_carry=True
    # )
    # resource = time_remained()
    # pre = time.time()
    # # val = minimax_ab_cutoff(node, True, NEG_INFTY, POS_INFTY, 3, resource)
    # val = iterdeep_minimax(node, resource)
    # print(time.time() - pre)
    # # for child in node.children:
    # #     if child.value + val == 0:
    # #         print(child.previous_move)
    # print(val)
    board = [[ 0,  1,  1,  1,  1],
            [ 1,  1,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1]]
    player = -1
    print(move(board = board, player = player))

        