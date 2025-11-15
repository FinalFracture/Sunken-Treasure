import sys
import pygame


class EventHandler:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        with open('debug_log.txt', 'r+') as log_file:
            text = '\nEvent handler started'
            log_file.write(text)
        self.dt = 0.0
        self.is_key_pressed = False
        self.anything = None
        self.single_press_keys = [pygame.K_1, 
                        pygame.K_2, 
                        pygame.K_3, 
                        pygame.K_4, 
                        pygame.K_5, 
                        pygame.K_6,
                        pygame.K_7,
                        pygame.K_8,
                        pygame.K_9, 
                        pygame.K_e, 
                        pygame.K_SPACE,
                        pygame.K_a,
                        pygame.K_d,
                        pygame.K_ESCAPE,
                        pygame.K_RETURN,
                        pygame.K_w,
                        pygame.K_s]

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
        if any(keys[key] for key in self.single_press_keys):
            self.is_key_pressed = True
        else:
            self.is_key_pressed = False

EVENT_HANDLER = EventHandler()
