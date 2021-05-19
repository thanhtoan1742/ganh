from board import *
from random_player import *

# class game:
#   - run the main game loop.
#   - let the player interact with ganh.
class game:
    def __init__(self, board = board(), player_0 = random_player(), player_1 = random_player()):
        self.board = board
        self.player_0 = player_0
        self.player_1 = player_1


    def run(self):
        while (1):
            if (self.ganh.finished()):
                break

            self.ganh.player_move(player=0, )
