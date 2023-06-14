import chess
import chess.engine
from settings import *
import math
import functools
class chessAgent:
    def __init__(self, board: chess.Board, agent_color):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.
        self.board = board
        self.agent_color = agent_color
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")

    @functools.lru_cache(None)
    def best_move(self):
        if self.agent_color == WHITE:
            return self.maximize(- math.inf, math.inf, 0)[1]
        else:
            return self.minimize(- math.inf, math.inf, 0)[1]
        
    @functools.lru_cache(10000)
    def maximize(self, alpha: int, beta:int, current_depth):
        current_score = - math.inf
        current_move = None

        if current_depth == MAX_DEPTH_MINIMAX or len(self.board.legal_moves):
            return self.evaluation(), None
        
        for i in self.board.legal_moves:
            self.board.push(i)
            score, move = self.minimize(alpha, beta, current_depth + 1)
            if score > current_score:
                current_move = i
                current_score = score
            self.board.pop()
            if current_score > beta:
                return current_score, current_move
            alpha = max(alpha, current_score)
            
        return current_score, current_move
    
    @functools.lru_cache(10000)
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
        return result['score']
    
    def evaluation_creative(self):
        # Write code about your own evaluation function here
        # YOUR CODE HERE
        pass

board = chess.Board()
agent = chessAgent(board, WHITE)
print(agent.evaluation())
agent.engine.close()