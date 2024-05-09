import pygame, sys
from SETTINGS import *
from game import Level

class Game:
    ### main class to manage game functions###

    def __init__(self):
        pygame.init() #initialize pygame
        self.log = open('save_file.txt', 'w') # create/overwrite the document for troubleshooting/logging. 
        self.window = pygame.display.set_mode((screen_width, screen_height)) #calling from settings, set the height and width of the display window
        pygame.display.set_caption('Treasures of the Surf')
        pygame.display.set_icon(pygame.image.load('images\\animals\catfish\catfish.png'))
        self.clock = pygame.time.Clock() #for creating a framerate independant animation setup. 
        self.level = Level(self) #start the main game logic

    def run(self):
        #function to start and run the game.
        while True:
            for event in pygame.event.get():
                #check for events to exit the game.
                if event.type == pygame.QUIT:
                    self.log.close() #properly exit and deallocate the memory for log. 
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick() / 1000 #multipler for animation speeds. 
            self.level.run(dt)
            pygame.display.update()

animal = Game()
animal.run()
