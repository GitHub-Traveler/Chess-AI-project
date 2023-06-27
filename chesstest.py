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
        self.engine = engine = chess.engine.SimpleEngine.popen_uci("stockfish_user_build.exe")
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
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=1))
        return int(result['score'].white().score(mate_score=10000000))
    
    def null_move_ordering(self, alpha, beta):
        pass

import time
board = chess.Board()

agent = chessAgent(board, board.turn)
# agent = chessAgent(board, WHITE)

start = time.perf_counter()
print(agent.best_move())
stop = time.perf_counter()
print(stop - start)

print(agent.hit)
print(agent.perf)
