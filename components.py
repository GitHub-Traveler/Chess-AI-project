import pygame
from settings import *
import chess
class ChessBoard:
    def __init__(self, screen: pygame.Surface, clock) -> None:
        self.screen = screen
        self.clock = clock
        self._initiate_game()

    def _initiate_game(self):
        # Initiate all variables to record important information in the game
        self.current_turn_white = True  # Current turn is white or black
        self.white_moves = []   # History of white moves
        self.black_moves = []   # History of black moves
        self.piece_image = {}   # Dictonary of chess pieces images.
        self.board = pygame.Surface((CHESS_PIECE_AREA * 8, CHESS_PIECE_AREA * 8))
        self.board.fill((255, 255, 255))
        self.piece_image['bP'] = pygame.image.load('Sprite/bP.png')
        self.piece_image['wP'] = pygame.image.load('Sprite/wP.png')
        self.piece_image['bQ'] = pygame.image.load('Sprite/bQ.png')
        self.piece_image['wQ'] = pygame.image.load('Sprite/wQ.png')
        self.piece_image['bK'] = pygame.image.load('Sprite/bK.png')
        self.piece_image['wK'] = pygame.image.load('Sprite/wK.png')
        self.piece_image['wKn'] = pygame.image.load('Sprite/wKn.png')
        self.piece_image['bKn'] = pygame.image.load('Sprite/bKn.png')
        self.piece_image['bR'] = pygame.image.load('Sprite/bR.png')
        self.piece_image['wR'] = pygame.image.load('Sprite/wR.png')
        self.piece_image['bB'] = pygame.image.load('Sprite/bB.png')
        self.piece_image['wB'] = pygame.image.load('Sprite/wB.png')
        for key, image in self.piece_image.items():
            self.piece_image[key] = pygame.transform.smoothscale(image, (CHESS_PIECE_AREA, CHESS_PIECE_AREA))
        self.black_pieces = ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bR', 'bKn', 'bB'
                            , 'bK', 'bQ', 'bB', 'bKn', 'bR']
        self.white_pieces = ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wR', 'wKn', 'wB'
                            , 'wK', 'wQ', 'wB', 'wKn', 'wR']
        self.black_pos = [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)
                          ,(8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
        self.white_pos = [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8)
                          ,(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8)]
        self.current_chosen_piece_position = None
        self.current_chosen_piece = None
        self.current_available_moves = None
        
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
            chosen_location = ((pos[1] - BASE_COORDINATE_BOARD[1]) // CHESS_PIECE_AREA + 1,
                                9 - ((pos[0] - BASE_COORDINATE_BOARD[0]) // CHESS_PIECE_AREA + 1))
            if (chosen_location[0] < 1 or chosen_location[0] > 8) or (chosen_location[1] < 1 or chosen_location[1] > 8):
                return
            if self.current_turn_white:
                chosen_location = (9 - chosen_location[0], 9 - chosen_location[1])
                if chosen_location in self.white_pos:
                    self.current_chosen_piece_position = chosen_location
                    self.current_chosen_piece = self.white_pieces[self.white_pos.index(chosen_location)]
                    self.current_available_moves = self.available_moves(chosen_location)
                elif chosen_location in self.current_available_moves:
                    self.white_pos[self.white_pos.index(self.current_chosen_piece_position)] = chosen_location
                    if chosen_location in self.black_pos:
                        remove_index = self.black_pos.index(chosen_location)
                        del self.black_pos[remove_index]
                        del self.black_pieces[remove_index]
                    self.current_turn_white = not self.current_turn_white
                else:
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = None
            else:
                chosen_location = (chosen_location[0], chosen_location[1])
                if chosen_location in self.black_pos:
                    self.current_chosen_piece_position = chosen_location
                    self.current_chosen_piece = self.black_pieces[self.black_pos.index(chosen_location)]
                    self.current_available_moves = self.available_moves(chosen_location)
                elif chosen_location in self.current_available_moves:
                    self.black_pos[self.black_pos.index(self.current_chosen_piece_position)] = chosen_location
                    if chosen_location in self.black_pos:
                        remove_index = self.black_pos.index(chosen_location)
                        del self.white_pos[remove_index]
                        del self.white_pieces[remove_index]
                    self.current_turn_white = not self.current_turn_white
                else:
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = None
    def draw(self):
        # Draw the empty chess board surface
        self.screen.blit(self.board, BASE_COORDINATE_BOARD)
        # Draw the chess board when it is white turn
        if self.current_turn_white:
            for x in range(1, 8, 2):
                for y in range(0, 8, 2):
                    pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                    CHESS_PIECE_AREA, CHESS_PIECE_AREA))
            for x in range(0, 8, 2):
                for y in range(1, 8, 2):
                    pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                    CHESS_PIECE_AREA, CHESS_PIECE_AREA))
            for i in range(0, len(self.black_pieces)):
                black_piece = self.black_pieces[i]
                black_piece_position = (9 - self.black_pos[i][0], self.black_pos[i][1])
                coordinate =  (CHESS_PIECE_AREA * (black_piece_position[1] - 1), CHESS_PIECE_AREA * (black_piece_position[0] - 1))
                self.board.blit(self.piece_image[black_piece], coordinate)
            
            for i in range(0, len(self.white_pieces)):
                white_piece = self.white_pieces[i]
                white_piece_position = (9 - self.white_pos[i][0], self.white_pos[i][1])
                coordinate =  (CHESS_PIECE_AREA * (white_piece_position[1] - 1), CHESS_PIECE_AREA * (white_piece_position[0] - 1))
                self.board.blit(self.piece_image[white_piece], coordinate)
        else:
            # Draw the chess board when it is black turn
            for x in range(0, 8, 2):
                for y in range(0, 8, 2):
                    pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                    CHESS_PIECE_AREA, CHESS_PIECE_AREA))
            for x in range(1, 8, 2):
                for y in range(1, 8, 2):
                    pygame.draw.rect(self.board, "grey", (x*CHESS_PIECE_AREA, y*CHESS_PIECE_AREA,
                                                    CHESS_PIECE_AREA, CHESS_PIECE_AREA))
            # Draw black pieces
            for i in range(0, len(self.black_pieces)):
                black_piece = self.black_pieces[i]
                black_piece_position = (self.black_pos[i][0], 9 - self.black_pos[i][1])
                coordinate =  (CHESS_PIECE_AREA * (black_piece_position[1] - 1), CHESS_PIECE_AREA * (black_piece_position[0] - 1))
                self.board.blit(self.piece_image[black_piece], coordinate)
            # Draw white pieces
            for i in range(0, len(self.white_pieces)):
                white_piece = self.white_pieces[i]
                white_piece_position = (self.white_pos[i][0], 9 - self.white_pos[i][1])
                coordinate = (CHESS_PIECE_AREA * (white_piece_position[1] - 1), CHESS_PIECE_AREA * (white_piece_position[0] - 1))
                self.board.blit(self.piece_image[white_piece], coordinate)
        return

    def available_moves(self, input: tuple):
        position = input
        if input in self.white_pos:
            current_piece = self.white_pieces[self.white_pos.index(input)]
            if current_piece == 'wK':
                return self.king_moves(position)
            if current_piece == 'wQ':
                return self.queen_moves(position)
            if current_piece == 'wKn':
                return self.knight_moves(position)
            if current_piece == 'wB':
                return self.bishop_moves(position)
            if current_piece == 'wR':
                return self.rook_moves(position)
            if current_piece == 'wP':
                return self.pawn_moves(position)
        if input in self.black_pos:
            current_piece = self.black_pieces[self.black_pos.index(input)]
            if current_piece == 'wK':
                return self.king_moves(position)
            if current_piece == 'wQ':
                return self.queen_moves(position)
            if current_piece == 'wKn':
                return self.knight_moves(position)
            if current_piece == 'wB':
                return self.bishop_moves(position)
            if current_piece == 'wR':
                return self.rook_moves(position)
            if current_piece == 'wP':
                return self.pawn_moves(position)

    def pawn_moves(self, input: tuple):
    def king_moves(self, input: tuple):
        pass
    def queen_moves(self, input: tuple):
    def bishop_moves(self, input: tuple):
    def rook_moves(self, input: tuple):
    def knight_moves(self, input: tuple):
        pass

class Agent:
    def __init__(self) -> None:
        pass