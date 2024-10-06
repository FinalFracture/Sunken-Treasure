import pygame
from menu_files.Inventory_menu import InventoryMenu
from menu_files.upgrade_menu import UpgradeMenu
from sprite_files.sprites import Textbox

class MenuManager:
    def __init__(self, group, player):
        self.group = group
        self.player = player
        self._menu_setup()

    def _menu_setup(self):
        #run once on instance creation
        self.is_active = False
        #Initialize class objects
        self.upgrade_menu = UpgradeMenu(self.group)
        self.inventory_menu = InventoryMenu(self.group)
        self.menus = [self.upgrade_menu, self.inventory_menu]
        # designate on screen area's with interactable functions
        
        #list of every surface that needs to be displayed
        self.menu_ui = [self.inventory_menu, self.upgrade_menu]
        self.display_group = [] 

    def show_menus(self) -> None:
        """ display to the screen and add to players inventory"""
        self.is_active = True
        self.upgrade_menu.is_active = True
        self.inventory_menu.is_active = True
        for item in self.menu_ui:
            self.display_group.append(item)
        self.group.add(element for element in self.display_group)

    def show_inventory(self, giver_of_items, receiver_of_items):
        self.inventory_menu.show_menu(giver_of_items=giver_of_items, receiver_of_items=receiver_of_items)

    def _input(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #set flags to use for preventing code from running repeatedly with key presses
        if not keys[pygame.K_e or pygame.K_b or pygame.K_RETURN]:
            self.key_pressed = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False

        #click based interaction

        #position based interaction

        #key based interaction
        
        

    def _update_status(self):
        #check if any constituent menus are active, and adjust self.is_active accordingly
        if any(menu.is_active for menu in self.menus):
            self.is_active = True
        else:
            self.is_active = False

    def update(self, dt):
        self._update_status()
        self._input()