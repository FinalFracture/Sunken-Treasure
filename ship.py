import pygame
from SETTINGS import * 
from support import import_folder
from timer import Timer
from sprite_files.characters import Character
from sprite_files.hud import Overlay
from menu_files.Inventory_menu import InventoryMenu

class Ship(Character): 
    def __init__(self, game, groups):
        self._import_assets()
        super().__init__(groups)
        self.game = game
        self.groups = groups
        self.inventory_ui = InventoryMenu(groups[1], self, (5, 15))
        self.overlay = Overlay(groups[1], self)
        self.gps_coord = (0,0)
        self.speed = 80
        self.knotical_speed = 0
        self.gold = 99999999
        self.overlay.position_crew_icons(self.crew_list)

    def _import_assets(self):
        """pull all needed images to generate animations"""
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
                           'up_fishing_pole':[], 'down_fishing_pole':[], 'left_fishing_pole':[], 'right_fishing_pole':[]
                             }
        for animation in self.animations.keys():
            full_path = 'images/ship/' + animation
            self.animations[animation] = import_folder(full_path)

    def _input(self, dt):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        #set flags to use for preventing code from running repeatedly with key presses
        if not keys[pygame.K_1 or pygame.K_e]:
            self.key_pressed = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False
        self._process_movement_input(keys, mouse_pos)
        self._process_ui_interaction_input(keys, mouse_pos)

    def _process_movement_input(self, keys, mouse_pos):
        if keys[pygame.K_a]: # move left
            self.direction.x = -1
            self.status, self.status_hold = 'left', 'left'

        elif keys[pygame.K_d]: # move right
            self.direction.x = 1
            self.status, self.status_hold = 'right', 'right'
        
        else: #no horizontal movement
            self.direction.x = 0

        if keys[pygame.K_w]: #move up
            self.direction.y = -1
            self.status, self.status_hold = 'up', 'up'

        elif keys[pygame.K_s]: # move down
            self.direction.y = 1

        else: # No vertical movement
            self.direction.y = 0
 
    def _process_ui_interaction_input(self, keys, mouse_pos):
        self._check_crew_icon_interaction(keys, mouse_pos)

        if keys[pygame.K_LSHIFT] and not self.interacting: #interact with objects
            self.interacting = True
        elif not keys[pygame.K_LSHIFT]:
            self.interacting = False 

        if not self.key_pressed and keys[pygame.K_e] and not self.inventory_ui.is_active:
            self.inventory_ui.show_menu()
            self.overlay.position_crew_icons(self.crew_list)

    def _check_crew_icon_interaction(self, keys, mouse_pos):
        #look at all inputs that may be interacting with the crew icons
        for crew_icon in self.crew_list:
            if crew_icon.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.clicking and not self.using_tool: #use assigned tool
                self.selected_tool = crew_icon.stats['tool']
                crew_icon.update_status('selected')
                self.using_tool = True
                self.clicking = True
            
            if crew_icon.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.clicking and self.using_tool: #stop using assigned tool
                    self.using_tool = False   
                    crew_icon.update_status('unselected') 
                    self.clicking = True

        if keys[pygame.K_1] and not self.key_pressed and not self.using_tool: 
            self.selected_tool = self.overlay.crew_list[0].stats['tool']
            crew_icon.update_status('selected')
            self.using_tool = True
            self.key_pressed = True
        if keys[pygame.K_1] and not self.key_pressed and self.using_tool: 
                crew_icon.update_status('unselected')
                self.using_tool = False
                self.key_pressed = True

    def _get_status(self, dt):
        super()._get_status(dt)
        #detect interactable objects nearby
        if any(self.rect.colliderect(sprite) for sprite in self.game.interactables):
            self._interactions()

        #check for movement
        keys = pygame.key.get_pressed()
        if any((keys[pygame.K_a], keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_d])):
            self.moving = True
        else:
            self.moving = False

    def _interactions(self):
        #check for interactions with the worlds objects
        if self.interacting:
            for interactable_object in self.game.interactables:
                if self.rect.colliderect(interactable_object.rect):
                    interactable_object.interact(self)
                    self.interacting = False
                    continue
                
    def update(self,dt):
        self._stat_error_handling()
        self._input(dt)
        self._navigation()
        super().update(dt)
        self._move(dt)

    def _navigation(self):
        self.gps_coord = (int(self.rect.x / 7), int((self.rect.y / 7)*-1))
        if self.moving:
            self.knotical_speed = round((((self.speed-100)/100)*7.9)+11.8) 
        else:
            self.knotical_speed = 0

    def _stat_error_handling(self):
        #this will check for stats that attempt to go over the maximum, like gold exceeding 99,999,999
        if self.gold > 99999999:
            self.gold = 99999999