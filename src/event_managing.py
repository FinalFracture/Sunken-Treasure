import sys
import pygame


class EventHandler:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        with open('debug_log.txt', 'r+') as log_file:
            text = '\nEvent handler started'
            log_file.write(text)
        self.dt = 0.0
        self.anything = None
        self.overworld_keys = [pygame.K_1, 
                        pygame.K_2, 
                        pygame.K_3, 
                        pygame.K_4, 
                        pygame.K_5, 
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9, 
                        pygame.K_e, 
                        pygame.K_LSHIFT]
        
        self.menu_keys = [
                        pygame.K_a,
                        pygame.K_d,
                        pygame.K_ESCAPE]

    def run(self, input_function:callable) -> None:
        """Event handler is the sole checker for mouse and keyboard inputs. Should only have one instance per game instance."""
        self.dt = self.clock.tick() / 1000
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            #check for events to exit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
        
        input_function(keys, mouse_pos, self.dt)

        # every frame debug
        if self.anything is not None: # and keys[pygame.K_0]:
            self.anything.debug()

    def get_test_item(self, item):
        self.anything = item

EVENT_HANDLER = EventHandler()
