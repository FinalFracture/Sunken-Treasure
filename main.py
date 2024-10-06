import pygame
from SETTINGS import *
from game import Level

class Game:
    ### main class to manage game functions###

    def __init__(self):
        pygame.init() #initialize pygame
        with open('debug_log.txt', 'w') as log_file:
            text = """
                    Game started
                    Pygame initialized
                    """
            log_file.write(text)
        self.window = pygame.display.set_mode((screen_width, screen_height)) #calling from settings, set the height and width of the display window
        pygame.display.set_caption('Treasures of the Surf')
        pygame.display.set_icon(pygame.image.load('images\\animals\carp\carp.png'))
        self.clock = pygame.time.Clock() #for creating a framerate independant animation setup. 
        self.level = Level(self) #start the main game logic

    def run(self):
        #function to start and run the game.
        while True:
            dt = self.clock.tick() / 1000 #multipler for animation speeds. 
            self.level.run(dt)
            pygame.display.update()

animal = Game()
animal.run()
