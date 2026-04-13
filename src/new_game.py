import pygame
from src.event_managing import EVENT_HANDLER
from src.utils.settings import *
from src.utils.cameras import screen_update
from src.utils.timer import Timer
from src.utils.enumerations import ViewID
from src.display.overlays import ViewsManager
from src.characters.player_character import PlayerCharacter
#from maps import Map


class main_loop:
    """The main game loop. Highest level logic"""
    def __init__(self, game) -> None:
        self.game = game
        self.player = PlayerCharacter('galleon')
        self.view_manager = ViewsManager(self.player)
        self.view_manager.change_view(ViewID.OVERWORLD)
        self.maps = []        

    def run(self):
        #start every frame with a clean screen
        EVENT_HANDLER.run()
        self.view_manager.recieve_triggers(EVENT_HANDLER.trigger_queue)
        screen_update(focus=self.player)
        Timer.update_all()
        EVENT_HANDLER.clear_triggers()

        #draw to the screen and update positions
        