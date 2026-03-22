import pygame
import random
from src.utils.settings import *
from src.overlays.trade_menu import TradeMenu
from src.overlays.Inventory_menu import InventoryMenu
from src.mechanics import Crew, build_crew_member
from src.characters.non_player_character import Non_Player_Character


class BoatShop(Non_Player_Character):
    def __init__(self, ship_type, starting_pos) -> None:
        super().__init__(starting_pos = starting_pos, ship_type=ship_type)
        self.speed = 20
        self.type = 'shop'
        self.inventory_ui = InventoryMenu(self, (600, 15), self.stats['inv_pages'], self.stats['crew_slots'])
        self.trade_ui = TradeMenu(self)

        #inventory management setup
        self.gold = 100
        self.inventory = []

    def update(self, dt):
        super().update(dt)
        self._get_movement_status()

    def interact(self, interactor):
        super().interact(interactor)    