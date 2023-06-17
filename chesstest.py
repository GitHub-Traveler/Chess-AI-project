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
        self.board = chess.Board()
        self.agent_color = agent_color
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
        self.transposition_table = {}

    def best_move(self):
        if self.agent_color == WHITE:
            self.transposition_table = {}
            return self.maximize(- math.inf, math.inf, 0)
        else:
            self.transposition_table = {}
            return self.minimize(- math.inf, math.inf, 0)
        
    # @cachetools.cached(cache=cachetools.LRUCache(maxsize=10000))
    def maximize(self, alpha, beta, current_depth):
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
            if current_score > beta:
                return current_score, current_move, perf
            alpha = max(alpha, current_score)
            
        return current_score, current_move, perf
    
    # @cachetools.cached(cache=cachetools.LRUCache(maxsize=10000))
    def minimize(self, alpha, beta, current_depth: int):
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
            if current_score < alpha:
                return current_score, current_move, perf
            beta = min(beta, current_score)

        return current_score, current_move, perf
    
    def evaluation(self):
        zobrist_key = chess.polyglot.zobrist_hash(self.board)
        if self.transposition_table.get(zobrist_key, False):
            return self.transposition_table[zobrist_key]
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
        self.transposition_table[zobrist_key] = result
        return float(result['score'].relative.score(mate_score=10000000))
    
    # def creative_evaluation(self):
    #     if self.board.is_insufficient_material():
    #         return DRAW_VALUE

    #     wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
    #     bp = len(self.board.pieces(chess.PAWN, chess.BLACK))

    #     wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
    #     bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))

    #     wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
    #     bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))

    #     wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
    #     br = len(self.board.pieces(chess.ROOK, chess.BLACK))

    #     wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
    #     bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

    #     value = (
    #         PV['pawn'] * (wp - bp) +
    #         PV['knight'] * (wn - bn) +
    #         PV['bishop'] * (wb - bb) +
    #         PV['rook'] * (wr - br) +
    #         PV['queen'] * (wq - bq)
    #     )

    #     if self.board.turn == chess.WHITE:
    #         return value
    #     return -value
    
    def null_move_ordering(self, alpha, beta):
        pass

board = chess.Board()
agent = chessAgent(board, WHITE)

print(agent.best_move())
agent.engine.close()