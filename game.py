import pygame
import sys
from settings import *
import ctypes
from components import *
class ChessGame:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Chess')
        set_dpi_awareness()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_state = 'Menu'
        self.board = ChessBoard(self.screen, self.clock)
        self.background = pygame.image.load('Sprite/anhbanhscale.jpg')
        
        self.background = pygame.transform.smoothscale(self.background, self.screen.get_size())
    def main_loop(self):
        while True:
            
            ip = self._handle_input()
            self._game_logic(ip)
            self._draw()
            self.clock.tick(FPS)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
                pygame.quit()
                quit()
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return (pos, True)
            else:
                return (pos, False)

    def _game_logic(self, input: tuple):
        self.board.game_logic(input)

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, self.screen.get_rect())
        self.board.draw()
        pygame.display.flip()

def set_dpi_awareness():
    # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
    print(awareness.value)

    # Set DPI Awareness  (Windows 10 and 8)
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    # the argument is the awareness level, which can be 0, 1 or 2:
    # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

    # Set DPI Awareness  (Windows 7 and Vista)
    success = ctypes.windll.user32.SetProcessDPIAware()
    # behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)