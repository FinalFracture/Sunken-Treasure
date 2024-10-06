import pygame
from SETTINGS import * 
from support import import_folder
from timer import Timer
from sprite_files.characters import All_Characters
from sprite_files.hud import Overlay
from menu_files.Inventory_menu import InventoryMenu

class Ship(All_Characters): 
    def __init__(self, game, groups):
        self._import_assets()
        super().__init__(groups, starting_pos=(0,0))
        self.game = game
        self.groups = groups
        self.inventory_ui = InventoryMenu(groups['overlay'], self, (5, 15))
        self.overlay = Overlay(groups['overlay'], self)
        self.gps_coord = (0,0)
        self.speed = 80
        self.knotical_speed = 0
        self.gold = 0
        self.overlay.position_crew_icons(self.crew_list)
        self.is_clicking = False
        self.is_key_pressed = False
        self.dialoge = None

    def _import_assets(self):
        """pull all needed images to generate animations"""
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
                           'up_fishing_pole':[], 'down_fishing_pole':[], 'left_fishing_pole':[], 'right_fishing_pole':[]
                             }
        for animation in self.animations.keys():
            full_path = 'images/ship/' + animation
            self.animations[animation] = import_folder(full_path)

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
                    self.dialoge = interactable_object.interact()
                    self.dialoge.process_text(interactable_object)
                    self.interacting = False
                    break
                
    def update(self,dt):
        self._stat_error_handling()
        self._navigation()
        super().update(dt)
        self._move(dt)

    def movement_input(self, keys):
        """Function is called by the game event handler"""
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
  
    def ui_input(self, keys, mouse_pos):

        def _single_click_operations():
            for crew_icon in self.crew_list:
                if crew_icon.rect.collidepoint(mouse_pos) and not self.using_tool: #use assigned tool
                    self.selected_tool = crew_icon.stats['tool']
                    crew_icon.update_status('selected')
                    self.using_tool = True
                    self.is_clicking = True
                elif crew_icon.rect.collidepoint(mouse_pos) and self.using_tool: #stop using assigned tool
                    self.using_tool = False   
                    crew_icon.update_status('unselected')
                    self.is_clicking = True 

        def _single_press_operations():
            if keys[pygame.K_1] and not self.using_tool: 
                self.selected_tool = self.crew_list[0].stats['tool']
                self.crew_list[0].update_status('selected')
                self.using_tool = True
                self.is_key_pressed = True

            elif keys[pygame.K_1] and self.using_tool: 
                    self.crew_list[0].update_status('unselected')
                    self.using_tool = False
                    self.is_key_pressed = True

            elif keys[pygame.K_LSHIFT] and not self.interacting: #interact with objects
                self.interacting = True
                self.is_key_pressed = True

            elif keys[pygame.K_e] and not self.inventory_ui.is_active:
                self.inventory_ui.show_menu()
                self.overlay.position_crew_icons(self.crew_list)
                self.is_key_pressed = True

            if not keys[pygame.K_LSHIFT]:
                self.interacting = False

        if not self.is_clicking and pygame.mouse.get_pressed()[0]:
            _single_click_operations()
        elif not pygame.mouse.get_pressed()[0]:
            self.is_clicking = False

        if not self.is_key_pressed:
            _single_press_operations()
        elif not any(pygame.key.get_pressed()):
            self.is_key_pressed = False

    def dialoge_input(self, keys) -> None:
        if keys[pygame.K_d]:
            self.dialoge.text_scroll_direction =1
        elif keys[pygame.K_a]:
            self.dialoge.text_scroll_direction = -1
        else:
            self.dialoge.text_scroll_direction = 0
        
        if keys[pygame.K_ESCAPE]:
            self.dialoge._end_dialoge()

        if keys[pygame.K_RETURN] and self.dialoge.ready_to_continue:
            if self.dialoge.dialoge_type == 'menu': # the indicator * means open the shop when dialogue is finished
                self.dialoge._end_dialoge() 
                self.inventory_ui.show_menu()
                self.dialoge.owner.trade_ui.show_menu(self)
                self.dialoge.owner.inventory_ui.show_menu()
            elif self.dialoge.dialoge_type == 'basic':
                self.dialoge._end_dialoge()

    def menu_input(self, keys, mouse_pos):
        if self.inventory_ui.is_active:
            self.inventory_ui.input()

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