import pygame
pygame.init() #initialize pygame

from src.utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from src.new_game import main_loop

class Game:
    ### main class to manage game functions###

    def __init__(self):
        
        with open('debug_log.txt', 'w') as log_file:
            log_file.write('Game started\nPygame initialized\n')
        
        self.main_loop = main_loop(self) #start the main game logic

    def run(self):
        #function to start and run the game.
        while True: 
            self.main_loop.run()

animal = Game()
animal.run()
