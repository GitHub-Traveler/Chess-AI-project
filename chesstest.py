import chess.engine

import chess
import chess.polyglot


from settings import *
import math

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
        
    def maximize(self, alpha, beta, current_depth):
        self.perf += 1
        current_score = - math.inf
        current_move = None
        perf = 0
        if current_depth == MAX_DEPTH_MINIMAX or self.board.is_checkmate():
            return self.evaluation(), None
        
        for i in self.board.legal_moves:
            self.board.push(i)
            score, move = self.minimize(alpha, beta, current_depth + 1)
            if current_score > beta:
                return current_score, current_move
            alpha = max(alpha, current_score)
            
        return current_score, current_move


    def minimize(self, alpha: int, beta: int, current_depth: int):
        current_score = math.inf
        current_move = None

        if current_depth == MAX_DEPTH_MINIMAX:
            return self.evaluation(), None
        
        for i in self.board.legal_moves:
            self.board.push(i)
            score, move = self.minimize(alpha, beta, current_depth + 1)
            if score < current_score:
                current_move = i
                current_score = score
            self.board.pop()
            if current_score < alpha:
                return current_score, current_move
            beta = min(beta, current_score)

        return current_score, current_move

    def evaluation(self):
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
        return int(result['score'].white().score(mate_score=MATE_SCORE))
    
import time
board = chess.Board()
agent = chessAgent(board, board.turn)

start = time.perf_counter()
print(agent.best_move())
stop = time.perf_counter()
print(stop - start)

print(agent.hit)
print(agent.perf)
