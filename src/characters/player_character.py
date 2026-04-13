import pygame
import random
from src.event_managing import Trigger, EVENT_HANDLER
from src.utils.settings import * 
from src.utils.timer import Timer
from src.utils.cameras import all_sprites, screen_update
from src.utils.enumerations import ViewID
from src.display.character_sprites import CharacterSprite
from src.display.screen_components import InventoryDisplay
from src.display.Inventory_menu import InventoryMenu
from src.characters import Character, BOAT_STATS
from src.display.screen_components import HUDCard

class PlayerCharacter(Character): 
    def __init__(self, ship_type):
        super().__init__(ship_type)
        self.sprite = CharacterSprite(self, starting_pos=(0,0), ship_type=ship_type)
        self.stats = BOAT_STATS[ship_type]
        self.inventory = []
        self.inventory_ui = InventoryMenu(self, self.stats['inv_pages'])
        self.timers = {}
        self.gps_coord:tuple[float, float] = (0,0)
        self.speed = self.stats.get("speed")
        self.knotical_speed = 0
        self.gold = 0
        self.is_clicking = False
        self.is_key_pressed = False
        self.hud_cards:dict[str, HUDCard] = {}
        self._start_hud_cards()

    def _interact(self):
        #check for interactions with the worlds objects
        self.state = 'interacting'
        for interactable_object in all_sprites:
            if self.sprite.interaction_box.colliderect(interactable_object) and hasattr(interactable_object.master, 'interact'):
                Timer.pause_all()
                self.deselect_tools()
                interactable_object.master.deselect_tools()
                player_crew = random.choice(self.crew_list)
                while self.state != 'normal':
                    self.state = interactable_object.master.interact(player_crew)
                    screen_update(focus=self)
                break

        Timer.resume_all()
        self.state = 'normal'
        return

    def _set_speed_and_coords(self) -> None:
        # add card function here to update speed and gpd coords
        self.gps_coord = (int(self.sprite.rect.x / 7), int((self.sprite.rect.y / 7)*-1))
        bearing_card = self.hud_cards.get('bearing')
        if bearing_card:
            bearing_card.update_textbox(self.gps_coord)
        if self.sprite.moving:
            self.knotical_speed = round((((self.speed-100)/100)*7.9)+11.8) 
        else:
            self.knotical_speed = 0
        # speed_card = self.hud_cards.get('speed')

    def _stat_error_handling(self):
        #this will check for stats that attempt to go over the maximum, like gold exceeding 99,999,999
        if self.gold > 99999999:
            self.gold = 99999999

    def _start_hud_cards(self) -> None:
        for crew in self.crew_list:
            if hasattr(crew, "hud_card"):
                hud_card_type = crew.hud_card_type
                hud_card = crew.hud_card
                hud_card.activate()                
                self.hud_cards[hud_card_type] = hud_card

    def update(self,dt):
        if self.state == 'normal':
            self._stat_error_handling()
            self._set_speed_and_coords()
            super().update(dt)
  
    def input(self, keys, mouse_pos, buttons, events, dt):
        self.sprite.movement_input(keys, mouse_pos, dt, self.speed)

        def _single_click_operations(event):
            if event.button == 1:
                for crew in self.crew_list:
                    if crew.sprite.rect.collidepoint(mouse_pos):
                        self.is_clicking = True
                        key_num = self.crew_list.index(crew) + 1
                        _activate_crew(key_num)

        def _activate_crew(key_num):
            try:
                self.active_crew = self.crew_list[key_num-1]
                self.deselect_tools(self.active_crew)
                self.sprite.toggle_tool(self.active_crew.tool.name)
                self.active_crew.toggle_selected()
            except IndexError as ie:
                pass
                # play reject sound

        def _single_press_operations(event):
            key_num = 0

            if event.key == pygame.K_1:
                key_num = 1

            elif event.key ==pygame.K_2:
                key_num = 2

            elif event.key == pygame.K_SPACE: #interact with objects
                self._interact()

            elif event.key ==pygame.K_LCTRL: #Overlay hints
                pass

            elif event.key ==pygame.K_e:
                print("Called")
                EVENT_HANDLER.emit(Trigger("OPEN_INVENTORY", self.inventory))

            if key_num > 0:
                _activate_crew(key_num)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                _single_click_operations(event)
            if event.type == pygame.KEYDOWN:
                _single_press_operations(event)


    def resume_play(self):
        self.overlay.position_crew_icons(self.crew_list)
        return super().resume_play()

    def show_inventory(self) -> bool:
        self.state = 'inventory'
        Timer.pause_all()
        self.deselect_tools()
        while self.state != 'normal':
            self.state = self.inventory_ui.show_menu(self.crew_list)
            screen_update(focus=self)
        Timer.resume_all()
        return True
            
    def add_to_inventory(self, item):
        return self.inventory_ui.add_to_inventory(item)

    def get_inv_level(self) -> str:
        """
        Return an int as a string, representing the number of full inv_slots for the player"
        """
        return str(self.inventory_ui.full_slots)
    
    def update_money(self, coins:int) -> None:
        self.gold += coins
        self.hud_cards['coin'].update

    def get_crew(self, crew_member) -> None:
        super().get_crew(crew_member)
        if hasattr(crew_member, "hud_card"):
            hud_card = self.hud_cards[crew_member.hud_card_type]
            self.hud_cards[hud_card] = crew_member.hud_card
            hud_card.activate()
            #OVERLAY.change_hud_cards(self.hud_cards)