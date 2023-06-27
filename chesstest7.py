import chess.engine
import chess
import chess.polyglot
from settings import *
import math
import random
import stockfish

def move_ordering(board: chess.Board):
    # Generate all legal moves
    moves = list(board.legal_moves)

    # Create a dictionary to store the priority of each move
    move_priority = {}

    # Assign a priority to each move
    for move in moves:
        priority = 0

        # If the move is a capture, increase its priority
        if board.is_capture(move):
            priority += 100

        # If the move gives a check, increase its priority
        if board.gives_check(move):
            priority += 50

        move_priority[move] = priority

    # Sort the moves based on their priority (descending order)
    sorted_moves = sorted(moves, key=lambda move: move_priority[move], reverse=True)

    return sorted_moves

class chessAgent:
    def __init__(self, board: chess.Board, agent_color: bool):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.
        # The transposition table saves the state of the chess board as (lowerbound, upperbound, depth)
        # lowerbound and upperbound are alpha and beta respectively

        chess.Board.__hash__ = chess.polyglot.zobrist_hash
        self.board = board
        self.agent_color = agent_color
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = stockfish.Stockfish("stockfish_user_build.exe")
        self.engine.set_depth(1)
        self.transposition_table = {}
        self.pv_move = None
        self.final_move = None
        self.hit = 0
        self.perf = 0

    def best_move_algorithm(self):
        if self.board.turn == WHITE:
            self.final_move = None
            self.pv_move = None
            # score = self.alpha_beta_with_memory(0, - MATE_SCORE, MATE_SCORE, {}, WHITE)
            # score = self.MTDF(0, {}, BLACK)
            score = self.iterative_deepening(WHITE, {})
            return score, self.final_move
        else:
            self.final_move = None
            # score = self.alpha_beta_with_memory(0, - MATE_SCORE, MATE_SCORE, {}, BLACK)
            # score = self.MTDF(0, {}, BLACK)
            score = self.iterative_deepening(BLACK, {})
            return score, self.final_move
    
    def iterative_deepening(self, color:bool, transposition_table):
        firstguess = 0
        # for d in range(0, self.maximum_depth + 1):
        #         firstguess = self.MTDF(firstguess, transposition_table, color, self.maximum_depth - d)
        if self.maximum_depth % 2 == 1:
            for d in range(1, self.maximum_depth + 1, 2):
                firstguess = self.MTDF(firstguess, transposition_table, color, d)
                self.pv_move = self.final_move
        else:
            for d in range(0, self.maximum_depth + 1, 2):
                firstguess = self.MTDF(firstguess, transposition_table, color, d)
                self.pv_move = self.final_move
        return firstguess

    def MTDF(self, f:int, transposition_table: dict, color: bool, max_depth: int):
        current_value = f
        lowerbound = - MATE_SCORE
        upperbound = MATE_SCORE
        while lowerbound < upperbound:
            self.final_move = None
            if current_value == lowerbound:
                beta = current_value + 1
            else:
                beta = current_value
            current_value = self.alpha_beta_with_memory(max_depth, max_depth, beta - 1, beta, transposition_table, color)
            if current_value < beta:
                upperbound = current_value
            else:
                lowerbound = current_value

        return current_value

    def alpha_beta_with_memory(self, current_depth, max_depth, alpha, beta, transposition_table, color):
        original_alpha = alpha
        hash = self.board.__hash__()
        if hash in transposition_table:
            self.hit += 1
            entry = transposition_table[hash]
            if entry["depth"] >= current_depth:
                # print(current_depth, entry["depth"], "Somethings went wrong")
                if entry["type"] == "exact":
                    return entry["value"]
                if entry["type"] == "lowerbound":
                    alpha = max(entry["value"], alpha)
                elif entry["type"] == "upperbound":
                    beta = min(entry["value"], beta)
                
                if alpha >= beta:
                    return entry["value"]
        
        self.perf += 1
        if current_depth <= 0 or self.board.is_checkmate():
            value = self.evaluation(color, transposition_table, hash, current_depth)
            return value

        current_value = - MATE_SCORE - 1
        moves_list = move_ordering(self.board)

        if not self.board.is_check():
            self.board.push(chess.Move.null())
            score = - self.alpha_beta_with_memory(current_depth - 1 - R, max_depth, - beta, - alpha, transposition_table, not color)
            self.board.pop()
            if score >= beta:
                return score
            
        if self.pv_move in moves_list:
            moves_list.remove(self.pv_move)
            moves_list = [self.pv_move] + moves_list

        for move in moves_list:
            self.board.push(move)
            value = - self.alpha_beta_with_memory(current_depth - 1, max_depth, - beta, - alpha, transposition_table, not color)
            self.board.pop()
            if value > current_value:
                current_value = value
                if current_depth == max_depth:
                    self.final_move = move
            alpha = max(current_value, alpha)
            if alpha >= beta:
                break
        
        if current_value <= original_alpha:
            transposition_table[hash] = {"type": "upperbound", "value": current_value, "depth": current_depth}
        elif current_value >= beta:
            transposition_table[hash] = {"type": "lowerbound", "value": current_value, "depth": current_depth}
        else:
            transposition_table[hash] = {"type": "exact", "value": current_value, "depth": current_depth}

        return current_value
    
    
    def evaluation(self, color, transposition_table, hash, depth):
        if hash in transposition_table:
            self.hit += 1
            return transposition_table[hash]["value"]
        self.perf += 1
        self.engine.set_fen_position(self.board.fen())
        result = self.engine.get_evaluation()
        value = result["value"]
        transposition_table[hash] = {"type": "exact", "value": value, "depth": depth}
        return value
    

import time
board = chess.Board()

agent = chessAgent(board, board.turn)
print(board.legal_moves)
start = time.perf_counter()
print(agent.best_move_algorithm())
stop = time.perf_counter()
print(stop - start)


print("Best move:", agent.final_move)
print(agent.hit)
print(agent.perf)



