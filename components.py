import pygame
from settings import *
class ChessBoard:
    def __init__(self, screen: pygame.Surface, clock) -> None:
        self.screen = screen
        self.clock = clock
        self._initiate_game()
    
    def game_logic(self, input: list):
        pos = input[0]
        click = input[1]
        if not click:
            pass
        else:
            pass
    
    def draw(self):
        anhbanh = pygame.image.load('Sprite/anhbanh.jpg')
        anhbanh = pygame.transform.smoothscale(anhbanh, (200, 200))
        rectange = anhbanh.get_rect()
        self.screen.blit(anhbanh, rectange)
        return

    def _initiate_game(self):
        self.piece_image = {}
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
        

