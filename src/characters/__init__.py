from src.mechanics import Crew, build_crew_member

BOAT_STATS = {
    'galleon':{
        'speed':40,
        'crew_slots':3,
        'inv_pages':6
    },
    'raft':{
        'speed':30,
        'crew_slots':1,
        'inv_pages':1
    },
    'sloop':{
        'speed':50,
        'crew_slots':2,
        'inv_pages':2
    },
    'canoe':{
        'speed':50,
        'crew_slots':2,
        'inv_pages':1
    },
    'troller':{
        'speed':50,
        'crew_slots':2,
        'inv_pages':2
    },
    'frigate':{
        'speed':50,
        'crew_slots':3,
        'inv_pages':6
    }
}

class Character():
    """This class will provide identical shared mechanics that all vessels will use, not related to animation or drawing"""
    def __init__(self, ship_type):
        self.stats = BOAT_STATS[ship_type]
        self.gold:int = 50
        self.timers:dict = {}
        self.crew_list:list[Crew] = [build_crew_member(self, 'angler'),build_crew_member(self, 'explorer')] 
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

    def get_crew(self, crew_member:Crew) -> None:
        self.crew_list.append(crew_member)

    def give_crew(self, new_owner, crew_name:str) -> Crew:
        """
        Transfer ownership of a crew member to another character.

        Args:
            new_owner (Character): Character to take ownership of the crew.
            crew_name (str): Full name of the crew being requested.
        """
        for crew in self.crew_list:
            if crew.name == crew_name:
                new_owner.get_crew(crew)
                self.crew_list.remove(crew)
