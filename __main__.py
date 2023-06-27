import sys
import os
import warnings


from game import ChessGame
if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    newgame = ChessGame()
    newgame.main_loop()