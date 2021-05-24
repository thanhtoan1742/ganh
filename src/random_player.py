from random import choice
from player import player

class random_player(player):
    def _get_move_(self):
        # If open moves exist, randomly chose 1 play it.
        open_moves = self.get_open_moves()
        if len(open_moves) > 0:
            op = choice(open_moves)
            return (op[0], op[1], op[2], op[3])

        # Randomly chose a starting position then randomly chose a destination.
        pos = self._get_player_position_()
        if len(pos) == 0:
            return
        x, y = choice(pos)
        u, v = choice(self._get_neighbor_with_value_(0, x, y))
        return (x, y, u, v)


p = random_player()
def move(board, player):
    return p.move(board, player)

p_2 = random_player()
def move_2(board, player):
    return p_2.move(board, player)