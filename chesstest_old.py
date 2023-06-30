import chess.engine

import chess
import chess.polyglot


from settings import *
import math
class chessAgent:
    def __init__(self, board: chess.Board):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.

        chess.Board.__hash__ = chess.polyglot.zobrist_hash
        self.board = board
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = engine = chess.engine.SimpleEngine.popen_uci("stockfish_user_build.exe")
        self.transposition_table = {}
        self.hit = 0
        self.perf = 0

    def best_move_algorithm(self):
        if self.board.turn == WHITE:
            return self.maximize(- MATE_SCORE, MATE_SCORE, 0)
        else:
            return self.minimize(- MATE_SCORE, MATE_SCORE, 0)

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
        return int(result['score'].white().score(mate_score=MATE_SCORE))

import time
file_path = "board_fen_list.txt"
board = chess.Board()
agent = chessAgent(board)
time_processed_list = []
nodes_visited_list = []
with open(file_path, 'r') as board_list:
    for board_fen in board_list:
        board_fen = board_fen.strip()
        agent.board.set_fen(board_fen)
        start = time.perf_counter()
        agent.best_move_algorithm()
        stop = time.perf_counter()
        time_processed = stop - start
        time_processed_list.append(time_processed)
        nodes_visited_list.append(agent.perf)

print(sum(time_processed_list) / len(time_processed_list))
print(sum(nodes_visited_list) / len(nodes_visited_list))
agent.engine.close()