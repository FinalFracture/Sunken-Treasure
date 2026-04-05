import pygame
from src.utils.timer import Timer
from src.display.screen_components import CrewQuartersHUD, Textbox, Generic,ItemStatBox, UiButton, HoverMessage, IconBG, UpgradeIconBg
from src.display.character_sprites import CharacterSprite
from src.display.Inventory_menu import InventoryMenu
from src.display.items_ui import ItemSprite, CrewSprite

_hud_card_top_positions = {
            'coin':3,
            'cargo':70,
            'speed':137,
            'bearing':204,
            'time': 271,
            'wind':338,
            'weather':405
        }

class HeadsUpDisplay:
    def __init__(self) -> None:
        self.crew_quarters_hud = CrewQuartersHUD()
        self.hud_cards = {}
        self.card_always_on = False
        self.timers = {
            'flash_cards':Timer(6000, starting_func=self._activate_hud_cards, ending_func=self._deactivate_hud_cards)
        }

    def flash_hud_cards(self) -> None:
        self.timers['flash_cards'].activate()

    def _activate_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            card.activate()

    def _deactivate_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            card.deactivate()

    def change_hud_cards(self, hud_cards:dict) -> None:
        self.hud_cards = hud_cards
        self._position_hud_cards()
    
    def _position_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            top_cord = _hud_card_top_positions[card.card_type]
            card.set_position(top=top_cord, left=0)

OVERLAY = HeadsUpDisplay()