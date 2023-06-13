import pygame
from settings import *

def is_mated(black_pieces: list, white_pieces: list, black_pos: list, white_pos: list):
    # This function returns 1 if black is mated, -1 if white is mated, 0 if both are not mated
    # and 2 if both sides are mated
    # YOUR CODE HERE
    pass

def is_winning(black_pieces: list, white_pieces: list, black_pos: list, white_pos: list):
    # This function returns 1 if white wins (black checkmated), -1 if black wins (white checkmated)
    # 0 if both sides are not checkmated (and 2 if both sides are checkmated)
    # YOUR CODE HERE
    pass

def is_stalemate(black_pieces: list, white_pieces: list, black_pos: list, white_pos: list):
    # This function returns 1 if black is in a stalemate, -1 if white is in stalemate 
    # 0 if both sides are not in stalemate (and 2 if both sides are stalemate)
    # YOUR CODE HERE
    pass

class ChessBoard:
    def __init__(self, screen: pygame.Surface, clock) -> None:
        self.screen = screen
        self.clock = clock
        self._initiate_game()
        self.agent = Agent(self)

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
        self.piece_image['possible_moves_mark'] = pygame.image.load('Sprite/possible_moves.png')
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
        self.filled = self.black_pos + self.white_pos
        self.current_chosen_piece_position = None
        self.current_chosen_piece = None
        self.current_available_moves = []
        
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
                        self.filled.remove(chosen_location)
                        self.filled[self.filled.index(self.current_chosen_piece_position)] = chosen_location
                    else:
                        self.filled[self.filled.index(self.current_chosen_piece_position)] = chosen_location
                    self.current_turn_white = not self.current_turn_white
                    # Next turn and reset the state
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = []
                else:
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = []
                
            else:
                chosen_location = (chosen_location[0], chosen_location[1])
                if chosen_location in self.black_pos:
                    self.current_chosen_piece_position = chosen_location
                    self.current_chosen_piece = self.black_pieces[self.black_pos.index(chosen_location)]
                    self.current_available_moves = self.available_moves(chosen_location)
                elif chosen_location in self.current_available_moves:
                    self.black_pos[self.black_pos.index(self.current_chosen_piece_position)] = chosen_location
                    if chosen_location in self.white_pos:
                        remove_index = self.white_pos.index(chosen_location)
                        del self.white_pos[remove_index]
                        del self.white_pieces[remove_index]
                        self.filled.remove(chosen_location)
                        self.filled[self.filled.index(self.current_chosen_piece_position)] = chosen_location
                    else:
                        self.filled[self.filled.index(self.current_chosen_piece_position)] = chosen_location
                    self.current_turn_white = not self.current_turn_white
                    # Next turn and reset the state
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = []
                else:
                    self.current_chosen_piece_position = None
                    self.current_chosen_piece = None
                    self.current_available_moves = []
    def draw(self):
        # Draw the empty chess board surface
        self.screen.blit(self.board, BASE_COORDINATE_BOARD)
        # Draw the chess board when it is white turn
        self.board.fill((255, 255, 255))
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

            for i in self.current_available_moves:
                mark_position = (9 - i[0], i[1])
                coordinate = (CHESS_PIECE_AREA * (mark_position[1] - 1), CHESS_PIECE_AREA * (mark_position[0] - 1))
                self.board.blit(self.piece_image['possible_moves_mark'], coordinate)
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
            
            for i in self.current_available_moves:
                mark_position = (i[0],9 - i[1])
                coordinate = (CHESS_PIECE_AREA * (mark_position[1] - 1), CHESS_PIECE_AREA * (mark_position[0] - 1))
                self.board.blit(self.piece_image['possible_moves_mark'], coordinate)
        return

    def available_moves(self, input: tuple):
        position = input
        if input in self.white_pos:
            current_piece = self.white_pieces[self.white_pos.index(input)]
            if current_piece == 'wK':
                return self.white_king_moves(position)
            if current_piece == 'wQ':
                return self.white_queen_moves(position)
            if current_piece == 'wKn':
                return self.white_knight_moves(position)
            if current_piece == 'wB':
                return self.white_bishop_moves(position)
            if current_piece == 'wR':
                return self.white_rook_moves(position)
            if current_piece == 'wP':
                return self.white_pawn_moves(position)
        if input in self.black_pos:
            current_piece = self.black_pieces[self.black_pos.index(input)]
            if current_piece == 'bK':
                return self.black_king_moves(position)
            if current_piece == 'bQ':
                return self.black_queen_moves(position)
            if current_piece == 'bKn':
                return self.black_knight_moves(position)
            if current_piece == 'bB':
                return self.black_bishop_moves(position)
            if current_piece == 'bR':
                return self.black_rook_moves(position)
            if current_piece == 'bP':
                return self.black_pawn_moves(position)

    def white_pawn_moves(self, input: tuple):
        moves = []
        if input[0] < 7 and (input[0]+1,input[1]) not in self.filled:
            moves.append((input[0]+1,input[1]))
            #If the pawn is in the first position
            if input[0] == 2 and (input[0]+2,input[1]) not in self.filled:
                moves.append((input[0]+2,input[1]))

        #check for enemies
        if (input[0]+1,input[1]+1) in self.black_pos:  
            moves.append((input[0]+1,input[1]+1))
        if (input[0]+1,input[1]-1) in self.black_pos:  
            moves.append((input[0]+1,input[1]-1))

        return moves
    def black_pawn_moves(self, input: tuple):
        moves = []
        if input[0] >= 0 and (input[0]-1,input[1]) not in self.filled:
            moves.append((input[0]-1,input[1]))
            #If the pawn is in the first position
            if input[0] == 7 and (input[0]-2,input[1]) not in self.filled:
                moves.append((input[0]-2,input[1]))

        #check for enemies
        if (input[0]-1,input[1]+1) in self.white_pos:  
            moves.append((input[0]-1,input[1]+1))
        if (input[0]-1,input[1]-1) in self.white_pos:  
            moves.append((input[0]-1,input[1]-1))

        return moves
    
    def white_bishop_moves(self, input: tuple):
        moves = []

        # Tính toán các nước đi đường chéo trái lên
        i, j = input[0]-1, input[1]-1
        while i >= 1 and j >= 1 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i-1, j-1
        if i >= 1 and j >= 1 and (i,j) in self.black_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo phải lên
        i, j = input[0]-1, input[1]+1
        while i >= 1 and j < 9 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i-1, j+1
        if i >= 1 and j < 9 and (i,j) in self.black_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo trái xuống
        i, j = input[0]+1, input[1] - 1
        while i < 9 and j >= 1 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i+1, j-1
        if i < 9 and j >= 1 and (i,j) in self.black_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo phải xuống
        i, j = input[0]+1, input[1] + 1
        while i < 9 and j < 9 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i+1, j+1
        if i < 9 and j < 9 and (i,j) in self.black_pos:
            moves.append((i, j))

        return moves
    

    def black_bishop_moves(self, input: tuple):
        moves = []

        # Tính toán các nước đi đường chéo trái lên
        i, j = input[0]-1, input[1]-1
        while i >= 1 and j >= 1 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i-1, j-1
        if i >= 1 and j >= 1 and (i,j) in self.white_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo phải lên
        i, j = input[0]-1, input[1]+1
        while i >= 1 and j < 9 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i-1, j+1
        if i >= 1 and j < 9 and (i,j) in self.white_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo trái xuống
        i, j = input[0]+1, input[1] - 1
        while i < 9 and j >= 1 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i+1, j-1
        if i < 9 and j >= 1 and (i,j) in self.white_pos:
            moves.append((i, j))

        # Tính toán các nước đi đường chéo phải xuống
        i, j = input[0]+1, input[1] + 1
        while i < 9 and j < 9 and (i,j) not in self.filled:
            moves.append((i, j))
            i, j = i+1, j+1
        if i < 9 and j < 9 and (i,j) in self.white_pos:
            moves.append((i, j))

        return moves

    def white_rook_moves(self, input: tuple):
        moves = []
        i,j = input[0], input[1]

        # Check vertical moves
        while i < 8 and (i+1,j) not in self.filled:
            moves.append((i+1, j))
            i = i + 1
            print(str(i) + " vertical 1")
        if i < 8 and (i+1,j) in self.black_pos:
            moves.append((i+1,j ))
        i,j = input[0], input[1]

        while i >= 1 and (i-1,j) not in self.filled:
            moves.append((i-1, j))
            i = i - 1
            print(str(i) + " vertical 2")
        if i >= 1 and (i-1,j) in self.black_pos:
            moves.append((i-1,j ))
        i,j = input[0], input[1]

        #Check horizontal moves
        while j < 8 and (i,j+1) not in self.filled:
            moves.append((i, j+1))
            j = j + 1
            print(str(j) + " horizontal 1")
        if j < 8 and (i,j+1) in self.black_pos:
            moves.append((i,j + 1 ))

        i,j = input[0], input[1]

        while j>= 1 and (i,j-1) not in self.filled:
            moves.append((i, j-1))
            j = j - 1
            print(str(j) + " horizontal 2")
        if j >= 1 and (i,j-1) in self.black_pos:
            moves.append((i,j-1))
            

        return moves

    
    def black_rook_moves(self, input: tuple):
        moves = []
        i,j = input[0], input[1]

        # Check vertical moves
        while i < 8 and (i+1,j) not in self.filled:
            moves.append((i+1, j))
            i = i + 1
        if i < 8 and (i+1,j) in self.white_pos:
            moves.append((i+1,j ))
        i,j = input[0], input[1]

        while i >= 1 and (i-1,j) not in self.filled:
            moves.append((i-1, j))
            i = i - 1
        if i >= 1 and (i-1,j) in self.white_pos:
            moves.append((i-1,j ))
        i,j = input[0], input[1]

        #Check horizontal moves
        while j < 8 and (i,j+1) not in self.filled:
            moves.append((i, j+1))
            j = j + 1
        if j < 8 and (i,j+1) in self.white_pos:
            moves.append((i,j + 1 ))

        i,j = input[0], input[1]

        while j>= 1 and (i,j-1) not in self.filled:
            moves.append((i, j-1))
            j = j - 1
        if j >= 1 and (i,j-1) in self.white_pos:
            moves.append((i,j-1 ))

        return moves


    def white_knight_moves(self, input: tuple):
        moves = []

        # Possible moves of knight
        offsets = [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)]
        for offset in offsets:
            i, j = input[0] + offset[0], input[1] + offset[1]

            if i >= 0 and i < 9 and j >= 0 and j < 9 and ((i,j) not in self.filled or (i,j) in self.black_pos):
                moves.append((i, j))

        return moves
    def black_knight_moves(self, input: tuple):
        moves = []

        # Possible moves of knight
        offsets = [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1)]
        for offset in offsets:
            i, j = input[0] + offset[0], input[1] + offset[1]

            if i >= 0 and i < 9 and j >= 0 and j < 9 and ((i,j) not in self.filled or (i,j) in self.white_pos):
                moves.append((i, j))

        return moves
    
    def white_queen_moves(self, input: tuple):
        moves = []
        moves.extend(self.white_bishop_moves(input))
        moves.extend(self.white_rook_moves(input))
        
        return moves
    def black_queen_moves(self, input: tuple):
        moves = []
        moves.extend(self.black_bishop_moves(input))
        moves.extend(self.black_rook_moves(input))
        
        return moves
    def white_king_moves(self, input: tuple):

        moves = []
        # Check all 8 squares around the king
        offsets = [(-1, -1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for offset in offsets:
            i, j = input[0] + offset[0], input[1] + offset[1]
            if i >= 0 and i < 9 and j >= 0 and j < 9 and ((i,j) not in self.filled or (i,j) in self.black_pos):
                moves.append((i, j))
        return moves
    def black_king_moves(self, input: tuple):

        moves = []
        # Check all 8 squares around the king
        offsets = [(-1, -1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for offset in offsets:
            i, j = input[0] + offset[0], input[1] + offset[1]
            if i >= 0 and i < 9  and j >= 0 and j < 9 and ((i,j) not in self.filled or (i,j) in self.white_pos):
                moves.append(( i, j))
        return moves

class Agent:
    def __init__(self, board: ChessBoard) -> None:
        self.board = board

    def find_best_move(self) -> tuple[tuple, tuple]:
        # This function returns the best move for the agent turn as two tuples
        # The first tuple is the initial location of the chess piece
        # The second tuple is the final location of that chess piece
        # YOUR CODE HERE
        pass
