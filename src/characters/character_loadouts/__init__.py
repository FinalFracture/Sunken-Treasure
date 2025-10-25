from src.characters.mechanics.crew import Crew
from src.characters.mechanics import Tool

BOAT_STATS = {
    'galleon':{
        'speed':30,
        'crew_slots':6,
        'max_inv_pages':6
    },
    'raft':{
        'speed':30,
        'crew_slots':2,
        'max_inv_pages':1
    },
    'sloop':{
        'speed':50,
        'crew_slots':3,
        'max_inv_pages':2
    }
}

class Character():
    """This class will provide identical shared mechanics that all vessels will use, not related to animation or drawing"""
    def __init__(self, ship_type):
        self.stats = BOAT_STATS[ship_type]
        self.gold:int = 50
        self.timers:dict = {}
        self.crew_list:list[Crew] = [Crew(crew_role='rockhound',owner=self), Crew(crew_role='angler',owner=self)] 
        self.active_crew:Crew = None
        self.state = 'normal'
        self.animations:dict = {'left': [], 'right': []}
        
    def resume_play(self):
        for timer in self.timers.values():
            timer.resume()
            
    def pause_timers(self):
        for timer in self.timers.values():
            timer.pause()

    def deselect_tools(self, ignore_crew=None) -> None:
        """deselect each crew member"""
        if ignore_crew == None:
            self.active_crew = None
            self.sprite.toggle_tool(toggle=0)
            
        for crew in self.crew_list:
            if crew != ignore_crew:
                crew.deselect()

    def update(self, dt):
        pass
