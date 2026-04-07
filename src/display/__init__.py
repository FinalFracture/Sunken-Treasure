from pygame.surface import Surface
from pygame.rect import Rect
from src.utils.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.utils.cameras import overlay_layers, overlay_sprites
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

    def _activate_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            card.activate()

    def _deactivate_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            card.deactivate()

    def _position_hud_cards(self) -> None:
        for card in self.hud_cards.values():
            top_cord = _hud_card_top_positions[card.card_type]
            card.set_position(top=top_cord, left=0)

    def change_hud_cards(self, hud_cards:dict) -> None:
        self.hud_cards = hud_cards
        self._position_hud_cards()
    
    def flash_hud_cards(self) -> None:
        self.timers['flash_cards'].activate()

    def overworld_pause(self, *callables) -> None:
        """
        Pause the game world to interact with a new overlay showing items, stats, etc. 

        Parameters
        ----------
        - callables: add callables in the order you want them called

        """
        pause_screen_image = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pause_screen_rect = pause_screen_image.get_rect()
        pause_screen = Generic(overlay_sprites, pause_screen_image, z=overlay_layers['hud_background'])
        unpaused = False
        self._activate_hud_cards()
        while not unpaused:
            for callable in callables:
                try:
                    unpaused = callable()
                except:
                    continue
        pause_screen.kill()
        self._deactivate_hud_cards()

OVERLAY = HeadsUpDisplay()