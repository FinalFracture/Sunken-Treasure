from pygame.surface import Surface
from pygame.rect import Rect
from src.event_managing import EVENT_HANDLER, Trigger
from src.utils.settings import SCREEN_HEIGHT, SCREEN_WIDTH
from src.utils.cameras import overlay_layers, overlay_sprites
from src.utils.timer import Timer
from src.utils.enumerations import ViewID
from src.display.screen_components import *
from src.characters.player_character import PlayerCharacter



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
        self.screen_objs:list[Sprite] = [] # all top level children of the view
        self.screen_obj_positions:dict[str, tuple[int,int]]
        self.view_id = ViewID.NULL

    def activate(self) -> None:
        self._position_screen_objs()
        for obj in self.screen_objs:
            try:
                obj.activate()
                overlay_sprites.add(obj)
            except:
                print(f"{type(obj)} does not have activate method")

    def deactivate(self) -> None:
        for obj in self.screen_objs:
            try:
                obj.deactivate()
            except:
                print(f"{type(obj)} does not have deactivate method")

    def _position_screen_objs(self) -> None:
        for obj in self.screen_objs:
            try:
                coord:dict[str, int] = self.screen_obj_positions.get(type(obj))
                obj.set_position(**coord)
            except Exception as e:
                pass
    
    def check_triggers(self, triggers:list[Trigger]) -> None:
        for obj in self.screen_objs:
            if hasattr(obj, "check_triggers"):
                obj.check_triggers(triggers)

class OverworldView(View):
    def __init__(self, player):
        super().__init__()
        self.view_id = ViewID.OVERWORLD
        self.screen_obj_positions:dict[str, tuple[int,int]] = {
            # (x_left, y_top)
            CoinCard: {'left': 0, 'top': 3},
            CargoCard: {'left': 0, 'top': 70},
            SpeedCard: {'left': 0, 'top': 137},
            BearingCard: {'left': 0, 'top': 204},
            'hud_card_time': {'left': 0, 'top': 271},
            'hud_card_wind': {'left': 0, 'top': 338},
            'hud_card_weather': {'left': 0, 'top': 405},
            CrewDisplay: {'bottom': SCREEN_HEIGHT, 'centerx':SCREEN_WIDTH/2},
        }
        self.screen_objs.append(player)
        self._build_view()
        
    def _build_view(self) -> None:
        self.coin_card = CoinCard()
        self.cargo_card = CargoCard()
        self.bearing_card = BearingCard()
        self.speed_card = SpeedCard()
        self.crew_display = CrewDisplay()
        self.screen_objs.append(self.crew_display)

    def add_screen_obj(self, *screen_objs:Sprite):
        self.screen_objs.extend(screen_objs)

    def check_triggers(self, triggers:list[Trigger]):
        for trigger in triggers:
            if trigger.type == f"ACTIVATE_HUD_CARD":
                match trigger.payload:
                    case CardID.BEARING:
                        self.screen_objs.append(self.bearing_card)
                        self.bearing_card.activate()
                    case CardID.SPEED:
                        self.screen_objs.append(self.speed_card)
                        self.speed_card.activate()
                    case CardID.CARGO: 
                        self.screen_objs.append(self.cargo_card)
                        self.cargo_card.activate()
                    case CardID.COIN:
                        self.screen_objs.append(self.coin_card)
                        self.coin_card.activate()
                self._position_screen_objs()

            if trigger.type == "ADD_CREW":
                self.crew_display.populate(trigger.payload)
                
        super().check_triggers(triggers)

class DiaogueView(View):
    def __init__(self, player):
        super().__init__()
        self.view_id = ViewID.DIALOGUE
        self.screen_obj_positions:dict[str, tuple[int,int]] = {
            # (x_left, y_top)
            CoinCard: {'left': 0, 'top': 3},
            CargoCard: {'left': 0, 'top': 70},
            SpeedCard: {'left': 0, 'top': 137},
            BearingCard: {'left': 0, 'top': 204},
            'hud_card_time': {'left': 0, 'top': 271},
            'hud_card_wind': {'left': 0, 'top': 338},
            'hud_card_weather': {'left': 0, 'top': 405},
            CrewDisplay: {'bottom': SCREEN_HEIGHT, 'centerx':SCREEN_WIDTH/2},
            DialogBox: {'left': 0, 'top': 0},
            'yes_no_box': {'left': 0, 'top': 0},
        }
        self.screen_objs.append(player)
        self._build_view()
        
    def _build_view(self) -> None:
        self.coin_card = CoinCard()
        self.cargo_card = CargoCard()
        self.bearing_card = BearingCard()
        self.speed_card = SpeedCard()
        self.dialogue_box = DialogBox()
        self.crew_display = CrewDisplay()
        self.screen_objs.append(self.coin_card)
        self.screen_objs.append(self.cargo_card)
        self.screen_objs.append(self.bearing_card) 
        self.screen_objs.append(self.speed_card)
        self.screen_objs.append(self.dialogue_box)
        self.screen_objs.append(self.crew_display)

    def add_screen_obj(self, *screen_objs:Sprite):
        self.screen_objs.extend(screen_objs)

class InventoryView(View):
    def __init__(self) -> None:
        super().__init__()
        self.view_id = ViewID.INVENTORY
        self.screen_obj_positions:dict[str, tuple[int,int]] = {
            InventoryDisplay: (55,3),
            CrewDisplay: (0,0), #fill out on desktop
            ClipboardDisplay: (320,3), #adjust on desktop
            'exit': (0,0)
        }

        self._build_view()

    def _build_view(self) -> None:
        bg = Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill('black')
        self.background = Generic(overlay_sprites, bg, z=overlay_layers['hud_background'])
        self.inventory_display = InventoryDisplay()
        self.screen_objs.extend([self.background,
                                self.inventory_display])
        
class ViewsManager:
    def __init__(self, player) -> None:
        self.active_view:View = None
        self.views:dict[int, View] = {
            ViewID.OVERWORLD: OverworldView(player),
            ViewID.INVENTORY: InventoryView()
        }
        for view in self.views.values():
            view.deactivate()

    def change_view(self, view_number:int) -> None:
        if not self.active_view:
            self.active_view = self.views[view_number]
            self.active_view.activate()
        else:
            self.active_view.deactivate()
            self.active_view = self.views[view_number]
            self.active_view.activate()
        EVENT_HANDLER.set_context(self.active_view.screen_objs)
              
    def run(self) -> None:
        self._check_triggers()

    def _check_triggers(self) -> None:
        triggers:list[Trigger] = EVENT_HANDLER.get_triggers()

        self.active_view.check_triggers(triggers)

        for trigger in triggers:
            if trigger.type == "OPEN_INVENTORY":
                self.change_view(ViewID.INVENTORY)
            if trigger.type == "CLOSE_INVENTORY":
                self.change_view(ViewID.OVERWORLD)