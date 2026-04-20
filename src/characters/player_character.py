import pygame
import random
from src.event_managing import Trigger, EVENT_HANDLER
from src.utils.settings import * 
from src.utils.timer import Timer
from src.utils.cameras import all_sprites, screen_update
from src.utils.enumerations import ViewID
from src.display.character_sprites import CharacterSprite
#from src.display.screen_components import InventoryDisplay
from src.display.Inventory_menu import InventoryMenu
from src.characters import Character, BOAT_STATS
from src.display.screen_components import HUDCard

class PlayerCharacter(Character): 
    def __init__(self, ship_type):
        super().__init__(ship_type)
        self.sprite = CharacterSprite(self, starting_pos=(0,0), ship_type=ship_type)
        self.stats = BOAT_STATS[ship_type]
        self.inventory = []
        self.timers = {}
        self.gps_coord:tuple[int, int] = (0,0)
        self.speed = self.stats.get("speed")
        self.gold = 0

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
        knotical_speed = 0
        if self.sprite.moving:
            EVENT_HANDLER.emit(Trigger("UPDATE_BEARING", self.gps_coord))
            knotical_speed = round((((self.speed-100)/100)*7.9)+11.8) 
        else:
            knotical_speed = 0

    def _stat_error_handling(self):
        #this will check for stats that attempt to go over the maximum, like gold exceeding 99,999,999
        if self.gold > 99999999:
            self.gold = 99999999

    def update(self,dt):
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
                EVENT_HANDLER.emit(Trigger("OPEN_INVENTORY", self.inventory))

            if key_num > 0:
                _activate_crew(key_num)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                _single_click_operations(event)
            if event.type == pygame.KEYDOWN:
                _single_press_operations(event)
        self._set_triggers()

    def _set_triggers(self) -> None:
        self._set_speed_and_coords()
        self._stat_error_handling()

    def resume_play(self):
        self.overlay.position_crew_icons(self.crew_list)
        return super().resume_play()
            
    def add_to_inventory(self, item):
        return self.inventory.add(item)
    
    def update_money(self, coins:int) -> None:
        self.gold += coins
        self.hud_cards['coin'].update

    def add_crew(self, crew_member) -> None:
        super().add_crew(crew_member)
        EVENT_HANDLER.emit(Trigger("ADD_CREW", crew_member))
        if hasattr(crew_member, "hud_card"):
            hud_card = crew_member.hud_card
            EVENT_HANDLER.emit(Trigger("ACTIVATE_HUD_CARD", hud_card))