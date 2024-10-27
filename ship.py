import pygame
from SETTINGS import * 
from sprite_files.characters import All_Characters
from sprite_files.hud import Overlay
from menus.Inventory_menu import InventoryMenu

class Ship(All_Characters): 
    def __init__(self, game, groups, ship_type):
        super().__init__(groups, starting_pos=(0,0), ship_type=ship_type)
        self.game = game
        self.groups = groups
        self.inventory_ui = InventoryMenu(groups['overlay'], self, (5, 15))
        self.inventory_ui.sidebar.make_button({'name':'Drop', 'func':self.inventory_ui.drop_item})
        self.overlay = Overlay(groups['overlay'], self)
        self.gps_coord = (0,0)
        self.speed = 80 
        self.knotical_speed = 0
        self.gold = 0
        self.overlay.position_crew_icons(self.crew_list)
        self.is_clicking = False
        self.is_key_pressed = False
        self.dialoge = None

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

        elif keys[pygame.K_s]: # move down
            self.direction.y = 1

        else: # No vertical movement
            self.direction.y = 0
  
    def ui_input(self, keys, mouse_pos, interaction_keys:list):
        def _single_click_operations():
            for crew in self.crew_list:
                if crew.rect.collidepoint(mouse_pos):
                    self.is_clicking = True
                    self.deselect_tools()
                    if not self.selected_tool == crew.stats['tool']:
                        self.selected_tool = crew.stats['tool']
                        crew.toggle_status()
                        self.using_tool = True
                    else:
                        self.using_tool = False
                        self.selected_tool = None  
 
        def _single_press_operations():
            if keys[pygame.K_1]:
                key_press = 1
                self.deselect_tools()
                self.is_key_pressed = True
                if not self.selected_tool == self.crew_list[key_press-1].stats['tool']:
                    self.using_tool = True
                    self.crew_list[key_press-1].toggle_status()
                    self.selected_tool = self.crew_list[key_press-1].stats['tool']
                else:
                    self.using_tool = False
                    self.selected_tool = None

            elif keys[pygame.K_2]:
                key_press = 2
                self.deselect_tools()
                self.is_key_pressed = True
                if not self.selected_tool == self.crew_list[key_press-1].stats['tool']:
                    self.using_tool = True
                    self.crew_list[key_press-1].toggle_status()
                    self.selected_tool = self.crew_list[key_press-1].stats['tool']
                else:
                    self.using_tool = False
                    self.selected_tool = None

            elif keys[pygame.K_LSHIFT] and not self.interacting: #interact with objects
                self.interacting = True
                self.is_key_pressed = True

            elif keys[pygame.K_e]:
                self.inventory_ui.show_menu()
                self.is_key_pressed = True

            if not keys[pygame.K_LSHIFT]:
                self.interacting = False

        if not self.is_clicking and pygame.mouse.get_pressed()[0]:
            _single_click_operations()
        elif not pygame.mouse.get_pressed()[0]:
            self.is_clicking = False

        if not self.is_key_pressed:
            _single_press_operations()
        elif not any(keys[key] for key in interaction_keys):
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
            return_clause = self.inventory_ui.input() # currently only used to re position crew icons
            if return_clause == 'exit':
                self.overlay.position_crew_icons(self.crew_list)

    def _navigation(self):
        self.gps_coord = (int(self.rect.x / 7), int((self.rect.y / 7)*-1))
        if self.moving:
            self.knotical_speed = round((((self.speed-100)/100)*7.9)+11.8) 
        else:
            self.knotical_speed = 0

    def deselect_tools(self) -> None:
        """deselect each crew member"""
        for crew in self.crew_list:
            if crew.status == 'selected':
                crew.toggle_status()

    def resume_play(self):
        self.overlay.position_crew_icons(self.crew_list)
        return super().resume_play()

    def _stat_error_handling(self):
        #this will check for stats that attempt to go over the maximum, like gold exceeding 99,999,999
        if self.gold > 99999999:
            self.gold = 99999999