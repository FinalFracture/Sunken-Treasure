import pygame
from pygame.sprite import Sprite
from SETTINGS import *
from sprite_files.hud import Textbox
from sprite_files.hud import UpgradeIconBg

class UpgradeMenu(Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.group = group
        self.menu_indicators = []
        self.is_active = False
        self.z = overlay_layers['menu']
        self._menu_setup()
        self.group.remove(element for element in self.menu_ui)

    def _menu_setup(self) -> None:
        """set the position for each element of the menu and assign its logic"""
        #menu setup
        self.image = pygame.image.load('images/hud/upgrade_menu_bg.png')
        self.rect = self.image.get_rect(center = (400, 250))
        self.exit_button = pygame.Rect(0,0, 11, 11)
        self.exit_button.center = ((self.rect.left + 339, self.rect.top + 12))

        #items to display setup
        self.item_title_textbox = Textbox(self.group, self, offset = (40, 20))

        #list of every surface that needs to be displayed
        self.menu_ui = [self, self.item_title_textbox]
        self.display_group = [] 

        #inventory slots setup
        self.inventory_slots = {} #dict of each inventory slot
        self.slot_spacing = 38 #distance from center of 1 slot to center of the next, plus 10 for spacing
        self.num_of_cols = 4


        #configure the inventory grid
        inv_slots = [] #a list of each slot, will be enumerated and turned into a dictionary
        left_offset = self.rect.left + 60
        bottom_offset = self.rect.top + self.rect.bottom/2
        for col in range(self.num_of_cols):
            slot = UpgradeIconBg(self.group)
            slot.rect.center = (left_offset + ((col -1)* self.slot_spacing), bottom_offset + 0)
            inv_slots.append(slot)
            self.menu_ui.append(slot)
            self.menu_ui.append(slot.value_display)
        self.inventory_slots = {index:item for index, item in enumerate(inv_slots)}
        self.item_list = []

    def update(self, dt) -> None:
        self._input()

    def show_menu(self) -> None:
        """ display to the screen and add to players inventory"""
        self.is_active = True
        for item in self.menu_ui:
            self.display_group.append(item)
        self.group.add(element for element in self.display_group)
        
    def _input(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #set flags to use for preventing code from running repeatedly with key presses
        if not keys[pygame.K_b or pygame.K_RETURN]:
            self.key_pressed = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False

        #click based interaction
        if keys[pygame.K_ESCAPE]:
            self.exit()

        if keys[pygame.K_u]:
            self.show_menu()

    def exit(self) -> None:
        #resolve any final actions and remove this object from display
        for item in self.display_group:
            self.group.remove(item)  #stop showing anything on the screen
        self.display_group = []
        self.is_active = False
    
