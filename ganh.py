import numpy as np

class Ganh:
    def __init__(self):
        self.board = np.array([
            [ 1,  1,  1,  1,  1],
            [ 1,  0,  0,  0,  1],
            [ 1,  0,  0,  0, -1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1],
        ])


    def __str__(self):
        return str(self.board)

    def print(self):
        print(str(self))


if __name__ == '__main__':
    ganh = Ganh()
    print(ganh)