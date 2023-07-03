import chess.engine
import chess
import chess.polyglot
from settings import *
from ultility_function import move_ordering

class chessAgent:
    def __init__(self, board: chess.Board):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.
        # The transposition table saves the state of the chess board as (lowerbound, upperbound, depth)
        # lowerbound and upperbound are alpha and beta respectively

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
        best_action = None
        self.perf += 1
        original_alpha = alpha
        hash = self.board.__hash__()
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
            
        if current_depth == 0 or self.board.is_checkmate():
            value = self.evaluation(color, transposition_table, hash, current_depth)
            return value

        current_value = - MATE_SCORE - 1
        moves_list = move_ordering(self.board)
            
        if best_action is not None and best_action in moves_list:
            moves_list.remove(best_action)
            moves_list = [best_action] + moves_list
        if self.pv_move in moves_list:
            moves_list.remove(self.pv_move)
            moves_list = [self.pv_move] + moves_list

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

        if current_value <= original_alpha:
            transposition_table[hash] = {"type": "upperbound", "value": current_value, "depth": current_depth, "best_action": best_action}
        elif current_value >= beta:
            transposition_table[hash] = {"type": "lowerbound", "value": current_value, "depth": current_depth, "best_action": best_action}
        else:
            transposition_table[hash] = {"type": "exact", "value": current_value, "depth": current_depth, "best_action": best_action}

        return current_value
    
    
    def evaluation(self, color, transposition_table, hash, depth):
        self.perf += 1
        if hash in transposition_table:
            self.hit += 1
            return transposition_table[hash]["value"]
        result = self.engine.analyse(self.board, chess.engine.Limit(depth=0))
        if color == WHITE:
            value = int(result['score'].white().score(mate_score=MATE_SCORE))
            transposition_table[hash] = {"type": "exact", "value": value, "depth": depth, "best_action": None}
            return value
        else:
            value = int(result['score'].black().score(mate_score=MATE_SCORE))
            transposition_table[hash] = {"type": "exact", "value": value, "depth": depth, "best_action": None}
            return value
        
    def move_ordering(self):
        # Generate all legal moves
        moves = list(self.board.legal_moves)

        # Create a dictionary to store the priority of each move
        move_priority = {}

        # Assign a priority to each move
        for move in moves:
            priority = 0

            # If the move is a capture, increase its priority
            if self.board.is_capture(move):
                priority += 100

            # If the move gives a check, increase its priority
            if self.board.gives_check(move):
                priority += 50

            move_priority[move] = priority

        # Sort the moves based on their priority (descending order)
        sorted_moves = sorted(moves, key=lambda move: move_priority[move], reverse=True)

        return sorted_moves