import pygame
from settings import *
import chess
import chess.engine
import math

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

        # Check if input is valid or not
        if input:
            pos = input[0]
            click = input[1]
        else:
            pos = None
            click = False
        
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
                if piece is not None:
                    piece = piece.symbol()
                    if piece.islower():
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
    def __init__(self, board: chess.Board, agent_color):
        # Initialize the board and the side in which the chess agent will be
        # If agent_color == WHITE, then the agent will be of WHITE side, and if agent_color == BLACK, then
        # the agent will be of BLACK side.
        self.board = board
        self.agent_color = agent_color
        self.maximum_depth = MAX_DEPTH_MINIMAX

    def best_move(self):
        if self.agent_color == WHITE:
            return self.maximize(- math.inf, math.inf, 0)[0]
        else:
            return self.minimize(- math.inf, math.inf, 0)[0]
    
    def maximize(self, alpha: int, beta:int, current_depth):
        current_score = - math.inf
        current_move = None

        if current_depth == MAX_DEPTH_MINIMAX:
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
        engine = chess.engine.SimpleEngine.popen_uci("stockfish\src\stockfish.exe")
        result = engine.analyse(self.board, chess.engine.Limit(depth=0))
        print(list(result))
        return result['score']
    
    def evaluation_creative(self):
        # Write code about your own evaluation function here
        # YOUR CODE HERE
        pass



