import pygame
import math
from sprite_files.hud import Icon_bg, ItemStatBox, HoverMessage
from SETTINGS import *


class InventoryMenu(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, owner:pygame.sprite.Sprite, top_left_pos:tuple) -> None:
        super().__init__(group)
        self.group= group
        self.is_active = False
        self.z = overlay_layers['menu']
        self.owner = owner
        self._menu_setup(top_left_pos)
        self.group.remove(element for element in self.menu_ui)  #remove from group to prevent from rendering.

    def _menu_setup(self, top_left_pos) -> None:
        """set the position for each element of the menu and assign its logic"""
        def _setup_inv_slots() -> dict:
            #configure the inventory grid
            inv_slots = [] #a list of each slot, will be enumerated and turned into a dictionary
            for row in range(self.num_of_rows):
                for col in range(self.num_of_cols):
                    slot = Icon_bg(self.group)
                    slot.rect.center = (60 + self.rect.x + ((col -1)* self.slot_spacing), 150 + self.rect.y + (self.slot_spacing * (row - 1)))
                    inv_slots.append(slot)
                    self.menu_ui.append(slot)
                    self.menu_ui.append(slot.value_display)
            return {index:item for index, item in enumerate(inv_slots)}
            
        def _setup_crew_slots():
            #Crew slots setup
            self.active_crew_page = 0 #used to decide which page of inventory to show
            self.crew_slots = {} #dict of each inventory slot
            self.crew_pages = {1:self.crew_slots}
            self.crew_rows = 1
            self.crew_icon_row_y = self.inventory_slots[41].rect.centery + self.slot_spacing
            self.crew_spots = self.num_of_cols * self.crew_rows

            #configure the inventory grid
            crew_slots = [] #a list of each slot, will be enumerated and turned into a dictionary
            for page in range(len(self.crew_pages.keys())):
                for row in range(self.crew_rows):
                    for col in range(self.num_of_cols):
                        slot = Icon_bg(self.group)
                        slot.rect.center = (60 + self.rect.x + ((col -1)* self.slot_spacing), self.crew_icon_row_y)
                        crew_slots.append(slot)
                        self.menu_ui.append(slot)
                        self.menu_ui.append(slot.value_display)
                crew_slots_page = {index:item for index, item in enumerate(crew_slots)}
                self.crew_pages[page] = crew_slots_page
            self.crew_list = []
            self.crew_slots =crew_slots_page

        #menu setup
        self.active_inventory_page = 0 #used to decide which page of inventory to show
        self.slot_spacing = 38 #distance from center of 1 slot to center of the next, plus 10 for spacing
        self.num_of_rows = 7
        self.num_of_cols = 6
        self.max_slots = self.num_of_cols * self.num_of_rows
        self.full_slots = 0
        self.image = pygame.image.load('images/hud/menu_bg.png')
        self.rect = self.image.get_rect(topleft = top_left_pos)
        self.exit_button = pygame.Rect(0,0, 11, 11)
        self.exit_button.center = ((self.rect.left + 339, self.rect.top + 12))
        self.item_stats_display = ItemStatBox(self.group, self.rect, (25,10))

        #items to display setup
        self.menu_ui = [self, self.item_stats_display] + self.item_stats_display.ui_elements

        self.inventory_slots = _setup_inv_slots()
        _setup_crew_slots()

        # Needed for mouse position inputs
        self.all_slots = []
        for key, value in self.inventory_slots.items():
            self.all_slots.append(value)
        for key, value in self.crew_slots.items():
            self.all_slots.append(value)

    def show_menu(self) -> None:
        """ display to the screen and add to players inventory"""
        self.is_active = True
        for item in self.menu_ui:
            self.group.add(item)
        self.menu_refresh()

    def menu_refresh(self):
        #run all commands when the menu needs to be refreshed
        self._clear_inventory_squares()
        self._clear_crew_squares()
        self._fill_inventory_squares()
        self._fill_crew_squares()

    def _clear_inventory_squares(self) -> None:  
        #remove all inventory items from display groups.
        #for item in self.item_list: #if we run into errors about a sprite not being in a group, this is the culprit.
        #   self.group.add(item)
        self.item_list = []

        for slot in self.inventory_slots.values(): 
            slot.deselect()
            if slot.subject:
                self.group.remove(slot.subject)
                slot.subject = None #clear what is stored in each slot.

    def _clear_crew_squares(self) -> None:  
        #remove all inventory items from display groups.
        self.crew_list = []

        for slot in self.crew_slots.values(): 
            slot.deselect()
            if slot.subject:
                self.group.remove(slot.subject)
                slot.subject = None #clear what is stored in each slot.

    def _fill_inventory_squares(self) -> None: 
        """assign each item an inventory slot"""
        def _divide_inventory_items() -> list:
            inventory_page_slots = 42 # the number of slots on a page of inventory
            needed_inventory_pages = math.ceil(len(self.owner.inventory)/inventory_page_slots)
            starting_inventory_index = 0
            divided_inventory = []
            if len(self.owner.inventory) < inventory_page_slots:
                divided_inventory = self.owner.inventory
            else:
                for page in range(needed_inventory_pages):
                    if len(self.owner.inventory) > inventory_page_slots*page+1:
                        divided_inventory.append(self.owner.inventory[starting_inventory_index:(inventory_page_slots*page+1)-1])
                        starting_inventory_index += inventory_page_slots
                    else:
                        divided_inventory.append(self.owner.inventory[starting_inventory_index:])
            
            return divided_inventory[self.active_inventory_page]

        self.item_list = _divide_inventory_items()
        self.group.add(self.item_list)
        for index, item in enumerate(self.item_list):
            self.inventory_slots[index].subject = item #inventory slot assignemnt

    def _fill_crew_squares(self) -> None: 
        """assign each crew a slot"""
        self.crew_list = self.owner.crew_list
        self.group.add(self.crew_list)
        self.crew_slots = self.crew_pages[self.active_crew_page]
        for index, crew in enumerate(self.crew_list):
            self.crew_slots[index].subject = crew #crew slot assignemnt
            crew.z = overlay_layers['menu_items']
        
    def input(self) -> None:
        #set flags to use for preventing code from running repeatedly with key presses
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_b or pygame.K_RETURN or pygame.K_e or pygame.K_u]:
            self.key_pressed = False
        if not pygame.mouse.get_pressed()[0]:
            self.clicking = False

        #click based interaction
        if (pygame.mouse.get_pressed()[0] and self.exit_button.collidepoint(mouse_pos) or keys[pygame.K_ESCAPE]):
            self.exit()

        #position based interaction
        for slot in self.all_slots:
            if slot.rect.collidepoint(mouse_pos):
                if slot.subject:
                    self.item_stats_display.item_name_display.text =f"Name : {slot.subject.name}"
                    self.item_stats_display.item_value_display.text = f'Value : {str(slot.subject.stats["value"])}'
                    self.item_stats_display.item_description_line1.text = slot.subject.stats['description1']
                    self.item_stats_display.item_description_line2.text = slot.subject.stats['description2']
                elif not slot.subject:
                    self.item_stats_display.item_name_display.text = ''
                    self.item_stats_display.item_value_display.text = ''
                    self.item_stats_display.item_description_line1.text =''
                    self.item_stats_display.item_description_line2.text =""
            elif not any(slot.rect.collidepoint(mouse_pos) for slot in self.all_slots):
                self.item_stats_display.item_name_display.text = '' 
                self.item_stats_display.item_value_display.text =''
                self.item_stats_display.item_description_line1.text = ''
                self.item_stats_display.item_description_line2.text =""

        #key based interaction
        if not self.key_pressed and keys[pygame.K_ESCAPE] and self.is_active:
            self.owner.overlay.position_crew_icons(self.crew_list)
            self.exit()
            self.key_pressed = True

        if keys[pygame.K_RETURN] and not self.key_pressed and self.is_active:
            self.menu_refresh()
            self.key_pressed = True

        if keys[pygame.K_u] and not self.is_active and not self.key_pressed:
            self.show_menu(giver_of_items=self.player)
            self.key_pressed = True

    def update(self, dt):
        if self.is_active:
            self.input()

    def exit(self) -> None:
        #resolve any final actions and remove this object from display
        self._clear_inventory_squares()
        self._clear_crew_squares()
        for item in self.menu_ui:
            self.group.remove(item)  #stop showing anything on the screen
        self.is_active = False
        self.owner.resume_timers()
    