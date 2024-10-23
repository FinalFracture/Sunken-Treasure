import sys
import pygame

class EventHandler:
    def __init__(self, player) -> None:
        self.player = player
        with open('debug_log.txt', 'r+') as log_file:
            text = '\nEvent handler started'
            log_file.write(text)
        
    def run(self, dt, game_state) -> None:
        """Event handler is the sole checker for mouse and keyboard inputs. Should only have one instance per game instance."""
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        interaction_keys = [pygame.K_1, 
                        pygame.K_2, 
                        pygame.K_3, 
                        pygame.K_4, 
                        pygame.K_5, 
                        pygame.K_6, 
                        pygame.K_e, 
                        pygame.K_LSHIFT]
        for event in pygame.event.get():
            #check for events to exit the game.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()        
        if game_state == 'paused':
            pass
        elif game_state == 'dialoge':
            self.player.dialoge_input(keys)
        elif game_state == 'menu':
            self.player.menu_input(keys, mouse_pos)
        else:
            self.player.movement_input(keys)
            self.player.ui_input(keys, mouse_pos, interaction_keys)

