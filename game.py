import pygame
from settings import *
import ctypes
class ChessGame:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Chess')
        set_dpi_awareness()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        print(pygame.display.get_desktop_sizes())
        self.clock = pygame.time.Clock()

    def main_loop(self):
        while True:
            
            self._handle_input()
            self._game_logic()
            self._draw()
            
            self.clock.tick(FPS)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
    def _game_logic(self):
        pass

    def _draw(self):
        self.screen.fill((0, 0, 255))
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