import pygame
import math

from src.characters.mechanics import GameItem
from src.overlays.screen_components import Icon_bg, ItemStatBox, Clipboard
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, overlay_layers, cameragroup_layers
from src.event_managing import EVENT_HANDLER

class InventoryMenu(pygame.sprite.Sprite):
    def __init__(self, owner:pygame.sprite.Sprite, top_left_pos:tuple, max_inv_pages:int, crew_slots:int) -> None:
        super().__init__(overlay_sprites)
        self.is_active:bool = False
        self.z:int = overlay_layers['menu']
        self.master:pygame.sprite.Sprite = owner
        self.key_pressed:bool = False
        self._menu_setup(top_left_pos, max_inv_pages, crew_slots)
        self.stop_showing = False
        overlay_sprites.remove(element for element in self.menu_ui)  #remove from group to prevent from rendering.

    def _menu_setup(self, top_left_pos:tuple[int,int], max_inv_pages:int, crew_slots:int) -> None:
        """set the position for each element of the menu and assign its logic"""
        
        def _setup_inv_slots() -> None:
            #configure the inventory grid and inventory pages
            vertical_spacing = 7
            horizontal_spacing = 9
            for page_num in range(max_inv_pages):
                page = {}
                slot_num = 0
                for row_num in range(self.inv_page_rows):
                    for col_num in range(self.inv_page_cols):
                        slot = Icon_bg(None, (0,0))
                        overlay_sprites.remove(slot)
                        slot_width = slot.rect.width
                        slot_height = slot.rect.height
                        slot.rect.centery = vertical_spacing + (row_num * slot_height) + (slot_height/2) + (row_num*vertical_spacing) + self.item_stats_display.rect.bottom
                        slot.rect.centerx = horizontal_spacing + (col_num * slot_width) + (slot_width/2) + (col_num*horizontal_spacing)
                        page[slot_num] = slot
                        self.all_slots.append(slot)
                        slot_num += 1
                self.inv_pages[page_num] = page 
                    
        #menu setup
        self.inv_page_index = 0
        self.inv_page_rows = 8
        self.inv_page_cols = 6
        self.full_slots = 0
        self.all_slots:list[Icon_bg] = []
        self.image = pygame.image.load('assets\images\hud/menu_bg.png')
        self.rect = self.image.get_rect(topleft = top_left_pos)
        self.exit_button = pygame.Rect(0,0, 11, 11)
        self.exit_button.center = ((self.rect.left + 339, self.rect.top + 12))
        self.item_stats_display = ItemStatBox(self.rect, (25,10))
        self.sidebar = Clipboard((self.rect.right+15, self.rect.top), self)
        self.crew_menu = CrewQuarters((self.rect.left, self.rect.bottom + 10), crew_slots)

        #items to display setup
        self.menu_ui = [self, self.item_stats_display, self.sidebar, self.crew_menu] + self.item_stats_display.ui_elements
        self.inv_pages:dict[int, dict[int, Icon_bg]] = {}
        _setup_inv_slots()
        self.active_inv_page:dict[int, Icon_bg] = self.inv_pages[self.inv_page_index]
        
    def show_menu(self) -> None:
        """ display to the screen and add to players inventory"""
        if self.is_active == False:
            self.is_active = True
            self.sidebar.show()
            self.menu_refresh()
            for item in self.menu_ui:
                overlay_sprites.add(item)

        page_check = self.inv_page_index
        EVENT_HANDLER.run(self.input)
        
        if page_check != self.inv_page_index:
            self.menu_refresh()

        if self.stop_showing == True:
            self.exit()
            return 'normal'

    def menu_refresh(self):
        #run all commands when the menu needs to be refreshed
        
        def _clear_inventory_squares() -> None:  
            #remove all inventory items from display groups.
            overlay_sprites.remove(self.active_inv_page.values())
            for slot in self.active_inv_page.values(): 
                if slot.subject:
                    overlay_sprites.remove(slot.subject)

        def _show_inv_page() -> None: 
            """assign each item an inventory slot"""

            for slot in self.active_inv_page.values():
                overlay_sprites.add(slot)
                if slot.subject is not None:
                    overlay_sprites.add(slot.subject)
                    if slot.subject.selected == True:
                        slot.click(toggle=1) 
                    else:
                        slot.click(toggle=0) 
                else:
                    slot.click(toggle=0)   

        def _get_inv_page():
            if self.inv_page_index > max(self.inv_pages.keys()):
                self.inv_page_index = min(self.inv_pages.keys())
            if self.inv_page_index < min(self.inv_pages.keys()):
                self.inv_page_index = max(self.inv_pages.keys())
            self.active_inv_page = self.inv_pages[self.inv_page_index]

        _clear_inventory_squares()
        _get_inv_page()
        self.full_slots = len([slot for slot in self.all_slots if slot.subject is not None])
        if self.stop_showing == False:
            _show_inv_page()
            self.sidebar.update_buttons()

    def input(self, keys, mouse_pos, dt) -> None:
        #set flags to use for preventing code from running repeatedly with key presses

        def _click_inputs():
            for slot in self.active_inv_page.values():
                if slot.rect.collidepoint(mouse_pos):

                    if pygame.mouse.get_pressed()[0]:
                        if keys[pygame.K_LCTRL]:
                            self.select_all(slot.subject)
                        else:
                            print('calling')
                            slot.click()
                    elif pygame.mouse.get_pressed()[2] :
                        [inv_slot.click(toggle=0) for inv_slot in self.active_inv_page.values()]

        def _key_inputs():
            #key based interaction
            if keys[pygame.K_ESCAPE]:
                self.stop_showing = True

            if keys[pygame.K_d]:
                self.inv_page_index += 1

            elif keys[pygame.K_a]:
                self.inv_page_index -= 1

            self.menu_refresh()

        def _update_item_window(slot)->None:
            if slot is not None and slot.subject is not None:
                self.item_stats_display.item_name_display.text =f"Name : {slot.subject.name}"
                self.item_stats_display.item_value_display.text = f'Value : {str(slot.subject.stats["value"])}'
                self.item_stats_display.item_description_line1.text = slot.subject.stats['description1']
                self.item_stats_display.item_description_line2.text = slot.subject.stats['description2']
            else:
                self.item_stats_display.item_name_display.text = ''
                self.item_stats_display.item_value_display.text = ''
                self.item_stats_display.item_description_line1.text =''
                self.item_stats_display.item_description_line2.text =""

        if any(keys[key] for key in EVENT_HANDLER.menu_keys):
            if self.key_pressed == False:
                _key_inputs() 
            self.key_pressed = True
        else:
            self.key_pressed = False

        if any(pygame.mouse.get_pressed()):
            if self.clicking == False:
                _click_inputs()
                self.clicking = True

        else:
            self.clicking = False

        for slot in self.active_inv_page.values():
            if slot.rect.collidepoint(mouse_pos):
                _update_item_window(slot)

            elif not any(slot.rect.collidepoint(mouse_pos) for slot in self.active_inv_page.values()):
                _update_item_window(None)
            
    def update(self, dt) -> None:
        pass

    def exit(self) -> None:
        #resolve any final actions and remove this object from display
        for slot in self.active_inv_page.values():
            slot.click(toggle=0)
        self.menu_refresh
        for item in self.menu_ui:
            overlay_sprites.remove(item)  #stop showing anything on the screen
        self.is_active = False
        self.stop_showing = False
        self.sidebar.exit()
        
    def reorder(self, sort_type=None, reversed=False) -> None:
        all_items = [slot.subject for slot in self.all_slots if slot.subject is not None]
        if sort_type is not None:
            if sort_type == 'alphabetical':
                all_items = sorted(all_items, key=lambda item: item.name)
            if sort_type == 'value':
                all_items = sorted(all_items, key=lambda item: item.value)

        for index, slot in enumerate(self.all_slots):
            slot.subject = None
            try:
                slot.subject = all_items[index]
            except IndexError:
                pass # skip ones with no subject
        self.menu_refresh()

    def drop_item(self) -> None:
        for slot in self.all_slots:
            if slot.subject is not None and slot.subject.selected:
                overlay_sprites.remove(slot.subject)
                slot.subject = None
            slot.click(toggle=0)
        self.reorder()
    
    def add_to_inventory(self, item:GameItem) -> bool:
        """
        Try to add an item to players inventory. If inventory is full, return false

        Parameters
        ----------
        - item : GameItem    
        """
        for page_num, page in self.inv_pages.items():
            for slot_num, slot in page.items():
                if slot.subject is None:
                    slot.subject = item
                    self.full_slots += 1
                    return True
        return False        

    def select_all(self, slot_item:pygame.sprite.Sprite) -> None:
        for slot in self.active_inv_page.values():
            if slot.subject is not None and slot.subject.name == slot_item.name:
                slot.click()

class CrewQuarters(pygame.sprite.Sprite):
    def __init__(self, top_left_pos:tuple[int, int], max_crew_slots:int):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets/images/hud/crew_menu.png')
        self.rect = self.image.get_rect(topleft=top_left_pos)
        self.z = overlay_layers['menu']
        overlay_sprites.remove(self)

        """
        def _setup_crew_slots():
            #Crew slots setup
            self.active_crew_page = 0 #used to decide which page of inventory to show
            self.crew_slots = {} #dict of each inventory slot
            self.crew_pages = {1:self.crew_slots}
            self.crew_rows = 1
            self.crew_icon_row_y = self.inventory_slots[41].rect.centery + self.slot_spacing
            self.crew_spots = self.inv_page_cols * self.crew_rows

            #configure the inventory grid
            crew_slots = [] #a list of each slot, will be enumerated and turned into a dictionary
            for page in range(len(self.crew_pages.keys())):
                for _ in range(self.crew_rows):
                    for col in range(self.inv_page_cols):
                        slot = Icon_bg()
                        slot.rect.center = (60 + self.rect.x + ((col -1)* self.slot_spacing), self.crew_icon_row_y)
                        crew_slots.append(slot)
                        self.menu_ui.append(slot)
                        self.menu_ui.append(slot.value_display)
                crew_slots_page = {index:item for index, item in enumerate(crew_slots)}
                self.crew_pages[page] = crew_slots_page
            self.crew_list = []
            self.crew_slots =crew_slots_page


                def _clear_crew_squares(self) -> None:  
        #remove all inventory items from display groups.
        self.crew_list = []

        for slot in self.crew_slots.values(): 
            if slot.subject:
                overlay_sprites.remove(slot.subject)
                slot.subject = None #clear what is stored in each slot.

    def _fill_crew_squares(self) -> None: 
        self.crew_list = self.master.crew_list
        overlay_sprites.add(self.crew_list)
        self.crew_slots = self.crew_pages[self.active_crew_page]
        for index, crew in enumerate(self.crew_list):
            self.crew_slots[index].subject = crew #crew slot assignemnt
            crew.z = overlay_layers['menu_items']
            """