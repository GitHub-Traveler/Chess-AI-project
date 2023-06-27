import pygame
from settings import *
import chess
import chess.engine
import chess.polyglot
import math
from ultility_function import move_ordering

class ChessBoard:
    def __init__(self, screen: pygame.Surface, clock) -> None:
        self.screen = screen
        self.clock = clock
        self._initiate_game()

    def _initiate_game(self):
        self.current_turn = WHITE
        self.board = pygame.Surface((CHESS_PIECE_AREA * 8, CHESS_PIECE_AREA * 8))
        self.board.fill((255, 255, 255))
        self.piece_image = {}
        self.piece_image['p'] = pygame.image.load('Sprite/bP.png')
        self.piece_image['P'] = pygame.image.load('Sprite/wP.png')
        self.piece_image['q'] = pygame.image.load('Sprite/bQ.png')
        self.piece_image['Q'] = pygame.image.load('Sprite/wQ.png')
        self.piece_image['k'] = pygame.image.load('Sprite/bK.png')
        self.piece_image['K'] = pygame.image.load('Sprite/wK.png')
        self.piece_image['N'] = pygame.image.load('Sprite/wKn.png')
        self.piece_image['n'] = pygame.image.load('Sprite/bKn.png')
        self.piece_image['r'] = pygame.image.load('Sprite/bR.png')
        self.piece_image['R'] = pygame.image.load('Sprite/wR.png')
        self.piece_image['b'] = pygame.image.load('Sprite/bB.png')
        self.piece_image['B'] = pygame.image.load('Sprite/wB.png')
        self.piece_image['possible_moves_mark'] = pygame.image.load('Sprite/possible_moves.png')
        for key, image in self.piece_image.items():
            self.piece_image[key] = pygame.transform.smoothscale(image, (CHESS_PIECE_AREA, CHESS_PIECE_AREA))
        self.chessboard = chess.Board()
        self.chessboard.reset()
        self.agent = chessAgent(self.chessboard, BLACK)
        self.current_available_moves = []
        self.current_chosen_chess_piece = None


    def get_all_moves_onepiece(self, start_location: int) -> list[chess.Move]:
        # Get all moves of a chess piece from a given position.
        list_of_moves = []
        for move in self.chessboard.legal_moves:
            if move.from_square == start_location:
                list_of_moves.append(move)
        return list_of_moves
    
    def game_logic(self, input: tuple):
        if self.chessboard.is_checkmate():
            self.agent.engine.close()
            pygame.quit()
            quit()
        # Check if input is valid or not
        if input:
            pos = input[0]
            click = input[1]
        else:
            pos = None
            click = False

        if self.chessboard.turn == BLACK:
            print(self.chessboard.legal_moves)
            # self.agent.minimize.cache_clear()
            # self.agent.maximize.cache_clear()
            self.chessboard.push(self.agent.best_move_algorithm()[0])
            return
        
        if not click:
            pass
        else:
            # Determine the tile which is clicked on
            chosen_location = (7 - (pos[1] - BASE_COORDINATE_BOARD[1]) // CHESS_PIECE_AREA,
                                ((pos[0] - BASE_COORDINATE_BOARD[0]) // CHESS_PIECE_AREA))
            if (chosen_location[0] < 0 or chosen_location[0] > 7) or (chosen_location[1] < 0 or chosen_location[1] > 7):
                return
            int_location_value = chosen_location[0] * 8 + chosen_location[1]
            piece = self.chessboard.piece_at(chosen_location[0] * 8 + chosen_location[1])
            if self.chessboard.turn == WHITE:
                if piece is not None:
                    piece = piece.symbol()
                    if piece.isupper():
                        self.current_chosen_chess_piece = piece
                        self.current_available_moves = self.get_all_moves_onepiece(int_location_value)
                        return
                    else:
                        for move in self.current_available_moves:
                            if int_location_value == move.to_square:
                                self.chessboard.push(move)
                                self.current_chosen_chess_piece = None
                                self.current_available_moves = []
                                break
                        else:
                            self.current_chosen_chess_piece = None
                            self.current_available_moves = []
                else:
                    for move in self.current_available_moves:
                        if int_location_value == move.to_square:
                            self.chessboard.push(move)
                            self.current_chosen_chess_piece = None
                            self.current_available_moves = []
                            break
                    else:
                        self.current_chosen_chess_piece = None
                        self.current_available_moves = []
            else:
                self.chessboard.push(self.agent.best_move_algorithm()[0])

    def draw(self):
        # Draw the empty chess board surface
        self.screen.blit(self.board, BASE_COORDINATE_BOARD)
        # Draw the chess board when it is white turn
        self.board.fill((255, 255, 255))
        for x in range(1, 8, 2):
            for y in range(0, 8, 2):
                pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                CHESS_PIECE_AREA, CHESS_PIECE_AREA))
        for x in range(0, 8, 2):
            for y in range(1, 8, 2):
                pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                CHESS_PIECE_AREA, CHESS_PIECE_AREA))
        for position, chess_piece in self.chessboard.piece_map().items():
            xy_position = (9 - (position // 8 + 1), position % 8 + 1)
            piece = chess_piece.symbol()
            coordinate = (CHESS_PIECE_AREA * (xy_position[1] - 1), CHESS_PIECE_AREA * (xy_position[0] - 1))
            self.board.blit(self.piece_image[piece], coordinate)

        for move in self.current_available_moves:
            square = move.to_square
            mark_position = (9 - (square // 8 + 1), (square % 8 + 1))
            coordinate = (CHESS_PIECE_AREA * (mark_position[1] - 1), CHESS_PIECE_AREA * (mark_position[0] - 1))
            self.board.blit(self.piece_image['possible_moves_mark'], coordinate)
        return

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
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_user_build.exe")
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
            return self.final_move, score
        else:
            self.final_move = None
            # score = self.alpha_beta_with_memory(0, - MATE_SCORE, MATE_SCORE, {}, BLACK)
            # score = self.MTDF(0, {}, BLACK)
            score = self.iterative_deepening(BLACK, {})
            return self.final_move, score
    
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
        best_action = None
        self.perf += 1
        original_alpha = alpha
        hash = self.board.__hash__()
        if hash in transposition_table:
            best_action = transposition_table[hash]["best_action"]
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
            
        if current_depth == 0 or self.board.is_checkmate():
            value = self.evaluation(color, transposition_table, hash, current_depth)
            return value

        current_value = - MATE_SCORE - 1
        moves_list = move_ordering(self.board)
        # if not self.board.is_check():
        #     self.board.push(chess.Move.null())
        #     score = - self.alpha_beta_with_memory(current_depth - 1 - R, max_depth, - beta, - alpha, transposition_table, not color)
        #     self.board.pop()
        #     if score >= beta:
        #         return score
            
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
    
    
        
    def creative_evaluation(self):
        if self.board.is_insufficient_material():
            return DRAW_VALUE

        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))

        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))

        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))

        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))

        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

        value = (
            PV['pawn'] * (wp - bp) +
            PV['knight'] * (wn - bn) +
            PV['bishop'] * (wb - bb) +
            PV['rook'] * (wr - br) +
            PV['queen'] * (wq - bq)
        )

        if self.board.turn == chess.WHITE:
            return value
        return -value



