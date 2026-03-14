import pygame
from src.display.screen_components import CrewQuartersHUD, Textbox, Generic,ItemStatBox, UiButton, HoverMessage, IconBG, UpgradeIconBg
from src.display.character_sprites import CharacterSprite
from src.display.Inventory_menu import InventoryMenu
from src.display.items_ui import ItemSprite, CrewSprite

class HeadsUpDisplay:
    def __init__(self) -> None:
        self.crew_quarters_hud = CrewQuartersHUD()

HUD = HeadsUpDisplay()