"""
This module contains the class chessAgent, which is our main AI agent for solving the chess board.
"""

import chess.engine
import chess
import chess.polyglot
from settings import *
import csv

import chess.polyglot
from settings import *
import csv
from chess import Move, Piece
from ultility_function import move_ordering



class chessAgent:
    def __init__(self, board: chess.Board):
        # Initiate the agent, which takes the chess.Board object as argument.
        chess.Board.__hash__ = chess.polyglot.zobrist_hash
        self.board = board
        self.maximum_depth = MAX_DEPTH_MINIMAX
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_user_build.exe")
        self.transposition_table = {}
        self.pv_move = None
        self.final_move = None
        self.hit = 0
        self.perf = 0

    def best_move_algorithm(self):
        # Main function, which returns the best move and the NegaMax value.
        self.hit = 0
        self.perf = 0
        self.final_move = None
        self.pv_move = None
        if self.board.turn == WHITE:
            score = self.iterative_deepening(WHITE, {})
            return self.final_move, score
        else:
            score = self.iterative_deepening(BLACK, {})
            return self.final_move, score
    
    def iterative_deepening(self, color:bool, transposition_table):
        """
        Iterative Deepening Framework
        Calls the function MTDF() with each depth
        The function jump two depths at a time as chess is an alternating game, NegaMax/MiniMax values of odds and evens depth
        will be similar and can be used for guessing the deeper MiniMax values
        """
        firstguess = 0
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
        """
        MTD(f) function, which is an improvement of Alpha-Beta Searcch
        Initiate the lowerbound and upperbound, and use the guess with repeated calls of Zero-Window Search
        for closing the upper bound and lower bound.
        """
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
        """
        The main alpha-beta function, but with transposition table implemented to reduce time searched.
        """
        best_action = None
        self.perf += 1
        original_alpha = alpha
        hash = self.board.__hash__()
        # Search in the transposition table using Zobrist hash
        if hash in transposition_table:
            self.hit += 1
            entry = transposition_table[hash]
            best_action = entry["best_action"]
            if entry["depth"] >= current_depth:
                if entry["type"] == "exact":
                    return entry["value"]
                if entry["type"] == "lowerbound":
                    alpha = max(entry["value"], alpha)
                elif entry["type"] == "upperbound":
                    beta = min(entry["value"], beta)
                
                if alpha >= beta:
                    return entry["value"]
            
        # Return evaluation results if it is the terminal state or maximum depth
        if current_depth == 0 or self.board.is_checkmate():
            value = self.evaluation(color, transposition_table, hash, current_depth)
            return value

        # Order the moves using heuristic move ordering
        current_value = - MATE_SCORE - 1
        moves_list = move_ordering(self.board)
        
        # Find the PV-Move ordering using the transposition table and saved best move
        if best_action is not None and best_action in moves_list:
            moves_list.remove(best_action)
            moves_list = [best_action] + moves_list
        if self.pv_move in moves_list:
            moves_list.remove(self.pv_move)
            moves_list = [self.pv_move] + moves_list

        # Alpha-Beta Search loops
        for move in moves_list:
            self.board.push(move)
            value = - self.alpha_beta_with_memory(current_depth - 1, max_depth, - beta, - alpha, transposition_table, not color)
            self.board.pop()
            if value > current_value:
                current_value = value
                best_action = move
                if current_depth == max_depth:
                    self.final_move = move
            alpha = max(current_value, alpha)
            if alpha >= beta:
                break
        
        # Save the results in the transposition table.
        if current_value <= original_alpha:
            transposition_table[hash] = {"type": "upperbound", "value": current_value, "depth": current_depth, "best_action": best_action}
        elif current_value >= beta:
            transposition_table[hash] = {"type": "lowerbound", "value": current_value, "depth": current_depth, "best_action": best_action}
        else:
            transposition_table[hash] = {"type": "exact", "value": current_value, "depth": current_depth, "best_action": best_action}

        return current_value
    
    
    def evaluation(self, color, transposition_table, hash, depth):
        """
        Evaluation function for the Alpha-Beta Search
        Stockfish Evaluation is used for convenience, as the evaluation function of chess is extremely complicated
        """
        self.perf += 1
        # Search for results in the transposition table
        if hash in transposition_table:
            self.hit += 1
            return transposition_table[hash]["value"]
        # If there is no, call the engine API and return the value of chessboard with respect to the current player
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
        if color == WHITE:
            value = int(result['score'].white().score(mate_score=MATE_SCORE))
            transposition_table[hash] = {"type": "exact", "value": value, "depth": depth, "best_action": None}
            return value
        else:
            value = int(result['score'].black().score(mate_score=MATE_SCORE))
            transposition_table[hash] = {"type": "exact", "value": value, "depth": depth, "best_action": None}
            return value
        
import time
import csv
file_path = "board_fen_list.txt"
board = chess.Board()
agent = chessAgent(board)
time_processed_list = []
nodes_visited_list = []
file = open("result_improved.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(["Board No.", "Time Processed", "Nodes Visited", "Best Move", "Best Score"])
boardno = 1
with open(file_path, 'r') as board_list:
    for board_fen in board_list:
        board_fen = board_fen.strip()
        agent.board.set_fen(board_fen)
        start = time.perf_counter()
        move, score = agent.best_move_algorithm()
        stop = time.perf_counter()
        time_processed = stop - start
        time_processed_list.append(time_processed)
        nodes_visited_list.append(agent.perf)
        writer.writerow([boardno, time_processed, agent.perf, move.uci(), score])
        boardno += 1
        

print(sum(time_processed_list) / len(time_processed_list))
print(sum(nodes_visited_list) / len(nodes_visited_list))
agent.engine.close()
file.close()
