from pygame.surface import Surface
from pygame.rect import Rect
from src.utils.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.utils.cameras import overlay_layers, overlay_sprites
from src.utils.timer import Timer
from src.display.screen_components import CrewQuartersHUD, Textbox, Generic,ItemStatBox, UiButton, HoverMessage, IconBG, UpgradeIconBg
from src.display.character_sprites import CharacterSprite
from src.display.Inventory_menu import InventoryMenu
from src.display.items_ui import ItemSprite, CrewSprite

#overworld play
_overworld_overlay:dict[str, tuple[int,int]] = {
    #(x_left,y_top)
            'hud_card_coin':(0,3),
            'hud_card_cargo':(0,70),
            'hud_card_speed':(0,137),
            'hud_card_bearing':(0,204),
            'hud_card_time': (0,271),
            'hud_card_wind':(0,338),
            'hud_card_weather':(0,405),
            'crew_quarters': (0,0), #fill out on desktop
            'dialogue_box': (0,0), #fill out on desktop
            'yes_no_box': (0,0),
        }

# viewing player inventory
_player_inventory:dict[str, tuple[int,int]] = {
    'inventory': (55,3),
    'crew_quarters': (0,0), #fill out on desktop
    'clipboard': (0,3), #adjust on desktop
} 

_inventories:dict[str, tuple[int,int]] = {
    'player_inventory': (55, 3),
    'interactee_inventory': (SCREEN_WIDTH-55,3),
    'player_rune_inventory': (SCREEN_WIDTH-55,3),
    'player_upgrade_item_select': (0,0),
    'player_upgrade_stat_select': (0,0),
    'player_upgrade_rune_table': (0,0)
}

_compendium:dict[str, tuple[int,int]] = {
    ''
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
            coord = _overworld_overlay['hud_card_' + card.card_type]
            card.set_position(top=coord[1], left=coord[0])

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