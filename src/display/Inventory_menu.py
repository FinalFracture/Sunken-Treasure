import pygame
from math import floor
from src.mechanics.tools import GameItem
from src.display.screen_components import IconBG, ItemStatBox, UiButton
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, overlay_layers, cameragroup_layers
from src.event_managing import EVENT_HANDLER

class InventoryMenu(pygame.sprite.Sprite):
    def __init__(self, owner:pygame.sprite.Sprite, inv_pages:int, crew_slots:int) -> None:
        super().__init__(overlay_sprites)
        self.is_active:bool = False
        self.z:int = overlay_layers['menu']
        self.master:pygame.sprite.Sprite = owner
        self.key_pressed:bool = False
        self.interactable_slots:list[IconBG] = []
        self._menu_setup(inv_pages, crew_slots)
        self.stop_showing = False
        overlay_sprites.remove(element for element in self.menu_ui)  #remove from group to prevent from rendering.

    def _menu_setup(self, inv_pages:int, crew_slots:int) -> None:
        """set the position for each element of the menu and assign its logic"""
        
        def _setup_inv_slots() -> None:
            #configure the inventory grid and inventory pages
            vertical_spacing = 7
            horizontal_spacing = 9
            for page_num in range(inv_pages):
                page = {}
                slot_num = 0
                for row_num in range(self.inv_page_rows):
                    for col_num in range(self.inv_page_cols):
                        slot = IconBG(None, (0,0))
                        overlay_sprites.remove(slot)
                        slot_width = slot.rect.width
                        slot_height = slot.rect.height
                        slot.rect.centery = vertical_spacing + (row_num * slot_height) + (slot_height/2) + (row_num*vertical_spacing) + self.item_stats_display.rect.bottom
                        slot.rect.centerx = horizontal_spacing + (col_num * slot_width) + (slot_width/2) + (col_num*horizontal_spacing)
                        page[slot_num] = slot
                        self.all_slots.append(slot)
                        slot_num += 1
                self.inv_pages[page_num] = page 
                    
        #inventory menu setup
        self.inv_page_index = 0
        self.inv_page_rows = 8
        self.inv_page_cols = 6
        self.full_slots = 0
        self.crew_list = []
        self.all_slots:list[IconBG] = []
        self.image = pygame.image.load('assets/images/hud/menu_bg.png')
        self.rect = self.image.get_rect()
        self.exit_button = pygame.Rect(0,0, 11, 11)
        self.exit_button.center = ((self.rect.left + 339, self.rect.top + 12))
        self.item_stats_display = ItemStatBox(self.rect, (25,10))

        # crew menu setup
        self.crew_menu = CrewQuarters((self.rect.left, self.rect.bottom + 10), crew_slots)

        #items to display setup
        self.menu_ui = [self, self.item_stats_display, self.crew_menu] + self.item_stats_display.ui_elements
        self.inv_pages:dict[int, dict[int, IconBG]] = {}
        _setup_inv_slots()
        self.active_inv_page:dict[int, IconBG] = self.inv_pages[self.inv_page_index]
        
    def show_menu(self, crew_list:list = []) -> None:
        """ display to the screen and add to players inventory"""
        if self.is_active == False:
            self.is_active = True
            self.crew_list = crew_list

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
            for slot in self.active_inv_page.values(): 
                if slot.subject:
                    overlay_sprites.remove(slot.subject.sprite)
            self.interactable_slots.clear()
            overlay_sprites.remove(self.active_inv_page.values())
            
        def _show_inv_page() -> None: 
            """assign each item an inventory slot"""
            for slot in self.active_inv_page.values():
                overlay_sprites.add(slot)
                if slot.subject is not None:
                    overlay_sprites.add(slot.subject.sprite)
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
        self.interactable_slots.extend(self.active_inv_page.values())
        if len(self.crew_list) > 0:
                self.interactable_slots.extend(self.crew_menu.show(self.crew_list))
        self.full_slots = len([slot for slot in self.all_slots if slot.subject is not None])
        print(len(self.interactable_slots))
        if self.stop_showing == False:
            _show_inv_page()









    def input(self, keys, mouse_pos, dt) -> None:
        #set flags to use for preventing code from running repeatedly with key presses

        def _click_inputs():
            for slot in self.active_inv_page.values():
                if slot.rect.collidepoint(mouse_pos):

                    if pygame.mouse.get_pressed()[0]:
                        if keys[pygame.K_LCTRL]:
                            self.select_all(slot.subject)
                        else:
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
                self.item_stats_display.item_value_display.text = f'Value : {str(slot.subject.rarity) if hasattr(slot.subject,"rarity") else str(slot.subject.value)}'
                self.item_stats_display.item_description_line1.text = slot.subject.description[0]
                self.item_stats_display.item_description_line2.text = slot.subject.description[1]
            else:
                self.item_stats_display.item_name_display.text = ''
                self.item_stats_display.item_value_display.text = ''
                self.item_stats_display.item_description_line1.text =''
                self.item_stats_display.item_description_line2.text =""

        if any(keys[key] for key in EVENT_HANDLER.single_press_keys):
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

        for slot in self.interactable_slots:
            if slot.rect.collidepoint(mouse_pos):
                _update_item_window(slot)

            elif not any(slot.rect.collidepoint(mouse_pos) for slot in self.interactable_slots):
                _update_item_window(None)
            
    def update(self, dt) -> None:
        pass

    def exit(self) -> None:
        #resolve any final actions and remove this object from display
        for slot in self.active_inv_page.values():
            slot.click(toggle=0)
        self.menu_refresh
        for element in self.menu_ui:
            overlay_sprites.remove(element)  #stop showing anything on the screen
        self.is_active = False
        self.stop_showing = False
        self.crew_menu.exit()
        
    def reorder(self, sort_type=None, reversed=False) -> None:
        all_items = [slot.subject for slot in self.all_slots if slot.subject is not None]
        if sort_type is not None:
            if sort_type == 'alphabetical':
                all_items = sorted(all_items, key=lambda item: item.name)
            if sort_type == 'value':
                all_items = sorted(all_items, key=lambda item: item.value, reverse=True)

        for index, slot in enumerate(self.all_slots):
            slot.subject = None
            try:
                slot.subject = all_items[index]
            except IndexError:
                continue # skip ones with no subject
        self.menu_refresh()

    def drop_item(self, arg) -> None:
        for slot in self.all_slots:
            if slot.subject is not None and slot.subject.selected:
                overlay_sprites.remove(slot.subject.sprite)
                slot.subject = None
            slot.click(toggle=0)
        self.reorder()
    
    def add_to_inventory(self, item) -> bool:
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
    def __init__(self, top_left_pos:tuple[int, int], crew_slots:int):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets/images/hud/crew_menu.png')
        self.rect = self.image.get_rect(topleft=top_left_pos)
        self.z = overlay_layers['menu']
        overlay_sprites.remove(self)
        self._setup_crew_slots(crew_slots)

    def _setup_crew_slots(self, crew_slots):
        #Crew slots setup
        self.crew_cap = crew_slots
        self.crew_slots:list[IconBG] = []
        self.max_slot_rows = 3
        self.max_slot_cols = 9

        vertical_spacing = 7
        horizontal_spacing = 9
        slot_num = 0
        for row_num in range(self.max_slot_rows):
            for col_num in range(self.max_slot_cols):
                if slot_num < self.crew_cap:
                    slot = IconBG(None, (0,0))
                    overlay_sprites.remove(slot)
                    slot_width = slot.rect.width
                    slot_height = slot.rect.height
                    slot.rect.centery = vertical_spacing + (row_num * slot_height) + (slot_height/2) + (row_num*vertical_spacing) +  self.rect.top
                    slot.rect.centerx = horizontal_spacing + (col_num * slot_width) + (slot_width/2) + (col_num*horizontal_spacing)
                    self.crew_slots.append(slot)
                    slot_num += 1

    def _clear_crew_squares(self) -> None:  
    #remove all inventory items from display groups.
        for slot in self.crew_slots.values(): 
            if slot.subject:
                overlay_sprites.remove(slot.subject.sprite)
                slot.subject = None #clear what is stored in each slot.

    def show(self, crew_list:list) -> list[IconBG]:
        
        for index, crew_slot in enumerate(self.crew_slots):
            overlay_sprites.add(crew_slot)
            try:
                crew_slot.subject = crew_list[index]
                crew_slot.subject.sprite.rect.center = crew_slot.rect.center
            except IndexError:
                pass # 
        return self.crew_slots

    def exit(self):
        for crew_slot in self.crew_slots:
            overlay_sprites.remove(crew_slot)

