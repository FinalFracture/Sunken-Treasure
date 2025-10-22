import pygame
import random
from src.utils.settings import *
from src.characters.npc_dialog_trees import boat_shop_dialog
from src.overlays.trade_menu import TradeMenu
from src.overlays.Inventory_menu import InventoryMenu
from src.characters.mechanics.crew import *
from src.characters.character_loadouts.non_player_character import Non_Player_Character


class BoatShop(Non_Player_Character):
    def __init__(self, ship_type, starting_pos) -> None:
        super().__init__(starting_pos = starting_pos, ship_type=ship_type)
        self.relation = 'new'
        self.ship_type = ship_type
        self.selected_tool = None
        self.dialoge = boat_shop_dialog['greetings'][self.relation]
        self.speed = 20
        self.inventory_ui = InventoryMenu(self, (600, 15))
        self.trade_ui = TradeMenu(self)

        #inventory management setup
        self.gold = 100
        self.inventory = []

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
        