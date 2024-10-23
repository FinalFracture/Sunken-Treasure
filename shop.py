import pygame
import random
from SETTINGS import *
from npc_dialog_trees import boat_shop_dialog
from menu_files.trade_menu import TradeMenu
from menu_files.Inventory_menu import InventoryMenu
from sprite_files.items import *
from sprite_files.characters import NonPlayerCharacter

class BoatShop(NonPlayerCharacter):
    def __init__(self, display_group, ship_type) -> None:
        self.relation = 'new'
        self.ship_type = ship_type
        self.selected_tool = None
        self.dialoge = boat_shop_dialog['greetings'][self.relation]
        self.speed = 20
        self.starting_pos = 200, 200
        self.inventory_ui = InventoryMenu(display_group['overlay'], self, (600, 15))
        self.trade_ui = TradeMenu(display_group['overlay'], self)
        super().__init__(display_group, starting_pos = self.starting_pos, ship_type=self.ship_type)
        #self.tools['fishing_pole'].base_catch_rate = 0.15

        #inventory management setup
        self.gold = 100
        self.inventory = []
        for item in self.inventory:
            display_group[0].remove(item)

    def update(self, dt):
        super().update(dt)
        self._get_movement_status()
        
    def interact(self) -> None:
        #boatshops should give their introduction, then display inventory and trade menu.
        self.dialog_box.dialoge = boat_shop_dialog["greetings"][self.relation]
        self.relation = 'familiar'
        self.dialog_box.speaking_crew = random.choice(self.crew_list)
        self.interrupt()
        return self.dialog_box
        