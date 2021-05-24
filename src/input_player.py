from player import player

class input_player(player):
    def _get_move_(self):
        open_moves = self.get_open_moves()
        print('open moves are:')
        print(open_moves)

        x, y, u, v = [int(e) for e in input().strip().split()]
        return x, y, u, v

        



p = input_player()
def move(board, player):
    return p.move(board, player)