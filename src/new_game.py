import pygame
from src.utils.settings import *
from src.utils.cameras import screen_update
from src.utils.timer import Timer
from src.characters.character_loadouts.player_character import Player_Character
from src.characters.character_loadouts.non_player_character import Non_Player_Character
from src.characters.character_loadouts.shop import BoatShop
#from maps import Map
from src.mechanics.tools import items_init
from src.event_managing import EVENT_HANDLER

class main_loop:
    """The main game loop. Highest level logic"""
    def __init__(self, game) -> None:
        self.game = game
        items_init()

        #get the display surface
        self.setup()

    def setup(self) -> None:
        """Initialize major game assets"""
        #Initialize the player and assets
        self.player = Player_Character(self, 'galleon')
        self.test_npc = Non_Player_Character('raft', (15, 32))

        #self.active_map = Map(self.all_sprites, self.collision_group, 'maps/Map1.tmx')
        
        #lists and dicts
        self.maps = []

    def run(self):
        #start every frame with a clean screen
        screen_update(focus=self.player)
        Timer.update_all()

        #draw to the screen and update positions
        
        
