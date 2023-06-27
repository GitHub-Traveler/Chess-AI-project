import chess.engine
import chess
import chess.polyglot


from settings import *
import math
import cachetools
from cachetools.keys import hashkey


class chessAgent:
    def __init__(self, board: chess.Board, agent_color):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.
        chess.Board.__hash__ = chess.polyglot.zobrist_hash
        self.board = board
        self.agent_color = agent_color
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
        self.transposition_table = {}
        self.hit = 0
        self.perf = 0
    def best_move(self):
        if self.agent_color == WHITE:
            self.transposition_table = {}
            return self.maximize(- math.inf, math.inf, 0)
        else:
            self.transposition_table = {}
            return self.minimize(- math.inf, math.inf, 0)
        
    # @cachetools.cached(cache=cachetools.LRUCache(maxsize=10000))
    def maximize(self, alpha, beta, current_depth):
        self.perf += 1
        current_score = - math.inf
        current_move = None
        perf = 0
        if current_depth == MAX_DEPTH_MINIMAX or self.board.is_checkmate():
            return self.evaluation(), None, 1
        
        for i in self.board.legal_moves:
            self.board.push(i)
            score, move, additional = self.minimize(alpha, beta, current_depth + 1)
            perf += additional
            if score > current_score:
                current_move = i
                current_score = score
            self.board.pop()
            if current_score >= beta:
                return current_score, current_move, perf
            alpha = max(alpha, current_score)
            
        return current_score, current_move, perf
    
    # @cachetools.cached(cache=cachetools.LRUCache(maxsize=10000))
    def minimize(self, alpha, beta, current_depth: int):
        self.perf += 1
        current_score = math.inf
        current_move = None
        perf = 0
        if current_depth == MAX_DEPTH_MINIMAX or self.board.is_checkmate():
            return self.evaluation(), None, 1
        

        for i in self.board.legal_moves:
            self.board.push(i)
            score, move, additional = self.maximize(alpha, beta, current_depth + 1)
            perf += additional
            if score < current_score:
                current_move = i
                current_score = score
            self.board.pop()
            if current_score <= alpha:
                return current_score, current_move, perf
            beta = min(beta, current_score)

        return current_score, current_move, perf
    
    def evaluation(self):
        self.perf += 1
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
        return int(result['score'].white().score(mate_score=10000000))
        if not self.transposition_table.get(self.board, False):
            result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
            result = float(result['score'].white().score(mate_score=10000000))
            self.transposition_table[self.board] = result
            return result
        else:
            self.hit += 1
            return self.transposition_table[self.board]
    
    def null_move_ordering(self, alpha, beta):
        pass

import time
board = chess.Board("1K2k3/2B5/1pbb2r1/p7/P6n/1Q5p/R2r4/2nB4 w - - 0 1")

agent = chessAgent(board, board.turn)
# agent = chessAgent(board, WHITE)

start = time.perf_counter()
print(agent.best_move())
stop = time.perf_counter()
print(stop - start)

print(agent.hit)
print(agent.perf)
