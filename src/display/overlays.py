from enum import Enum, auto
from pygame.surface import Surface
from pygame.rect import Rect
from src.utils.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.utils.cameras import overlay_layers, overlay_sprites
from src.utils.timer import Timer
from src.display.screen_components import CrewQuartersHUD, Textbox, Generic,ItemStatBox, UiButton, HoverMessage, IconBG, UpgradeIconBg
from src.display.character_sprites import CharacterSprite
from src.display.Inventory_menu import InventoryMenu
from src.display.items_ui import ItemSprite, CrewSprite
from src.characters.player_character import PlayerCharacter

class ViewID(Enum):
    OVERWORLD = auto()
    INVENTORY = auto()
    TRADE = auto()
    UPGRADE = auto()

CREW_QUARTERS = CrewQuartersHUD()

_trade:dict[str, tuple[int,int]] = {
    'player_inventory': (55, 3),
    'interactee_inventory': (SCREEN_WIDTH-55,3),
    'confirm': (0,0),
    'reset': (0,0),
    'exit': (0,0)
}

_upgrades:dict[str, tuple[int,int]] = {
    'player_inventory': (55, 3),
    'upgrade_item_select': (0,0),
    'upgrade_stat_select': (0,0),
    'upgrade_rune_table': (0,0),
    'confirm': (0,0),
    'reset': (0,0),
    'exit': (0,0)
}

_compendium:dict[str, tuple[int,int]] = {
    ''
}

class View:
    def __init__(self) -> None:
        bg_surface = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        view_bg = Generic(overlay_sprites, bg_surface, z=overlay_layers['hud_background'])
        self.child_objects = [view_bg]

    def activate(self, player) -> None:
        overlay_sprites.add(self.child_objects)
        self._assign_player(player)

    def deactivate(self) -> None:
        overlay_sprites.remove(self.child_objects)

    def _assign_player(self, player:PlayerCharacter) -> None:
        player_crew = player.crew_list
        CREW_QUARTERS.populate(player_crew)

class OverworldView(View):
    def __init__(self):
        super().__init__()
        self.view_id = ViewID.OVERWORLD
        self.child_object_positions:dict[str, tuple[int,int]] = {
            #(x_left,y_top)
            'hud_card_coin':(0,3),
            'hud_card_cargo':(0,70),
            'hud_card_speed':(0,137),
            'hud_card_bearing':(0,204),
            'hud_card_time': (0,271),
            'hud_card_wind':(0,338),
            'hud_card_weather':(0,405),
            'crew_quarters': None, #use math to place centerx = SCREEN_WIDTH/2
            'dialogue_box': (0,0), #fill out on desktop
            'yes_no_box': (0,0),
        }
        self.child_objects.append(CREW_QUARTERS)
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
            coord = self.child_object_positions['hud_card_' + card.card_type]
            card.set_position(top=coord[1], left=coord[0])

    def change_hud_cards(self, hud_cards:dict) -> None:
        self.hud_cards = hud_cards
        self._position_hud_cards()
    
    def flash_hud_cards(self) -> None:
        self.timers['flash_cards'].activate()

class InventoryView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_id = ViewID.INVENTORY
        self.child_object_positions:dict[str, tuple[int,int]] = {
            'inventory': (55,3),
            'crew_quarters': (0,0), #fill out on desktop
            'clipboard': (320,3), #adjust on desktop
            'exit': (0,0)
        }
        self.child_objects.append(CREW_QUARTERS)
    
    def _assign_player(self, player:PlayerCharacter) -> None:
        super()._assign_player(player)
        player_inv = player.inventory_ui
        if player_inv not in self.child_objects:
            self.child_objects.append(player_inv)
        inv_cord_top = self.child_object_positions['inventory'][1]
        inv_cord_left = self.child_object_positions['inventory'][0]
        player_inv.set_position(top=inv_cord_top, left=inv_cord_left)

        
class ViewsManager:
    def __init__(self) -> None:
        self.active_view:View = None
        self.views:dict[int, View] = {
            0: OverworldView(),
            1: InventoryView()
        }
        self.change_view(ViewID.OVERWORLD)

    def change_view(self, view_number:int, player) -> None:
        if self.active_view:
            self.active_view.deactivate()
            self.active_view = self.views[view_number]
            self.active_view.activate(player)
