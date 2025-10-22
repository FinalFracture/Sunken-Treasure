import random
from src.characters.mechanics import Tool, GameItem, item_stats
from src.utils.settings import *
from src.event_managing import EVENT_HANDLER
#from maps import MapTile


class FishingPole(Tool):
    def __init__(self, owner, crew):
        super().__init__(owner, crew)
        self.name = 'fishing_pole'
        self.catch_interval = 0.2
        self.find_list = ['tuna',
                       'carp',
                       'salmon',
                       'catfish']
       
    def use(self) -> None:
        """every 4 seconds, roll " a dice" to see if you find a fish"""
        self.frame_counter += 1 * EVENT_HANDLER.dt
        if self.frame_counter > self.catch_interval:
            self._determine_find_rate()
            possible_finds = self._determine_finds()
            success_check = random.random()
            if success_check <= self.find_rate:
                find = GameItem('fish', random.choice(possible_finds))
                self.master.inventory.append(find)
                self._animate_a_find(find)
            self.frame_counter = 0

    def _determine_find_rate(self):
        #look at factors that should change find rate for fishing, and then alter the rate
        if self.master.sprite.moving == False:
            self.find_rate_modifiers['movement'] = 0.1
        else:
            self.find_rate_modifiers['movement'] = 0

        for member in self.master.crew_list:
            if member.role == 'angler':
                self.find_rate_modifiers['crew'] = member.stats['tool_modifier']
        self.find_rate = self.base_find_rate + sum(values for values in self.find_rate_modifiers.values()) + 1

    def _determine_finds(self) -> list[str]:
        possible_finds = []
        find_list = self.find_list[:]
        """
        map_mods:None | list[str] = MapTile.get_tile_fishing_mod(self.master)
        if map_mods is not None:
            for fish in map_mods:
                if fish[0] == '-':
                    try:
                        find_list.remove(fish[1:])
                    except ValueError:
                        continue
                else:
                    find_list.append(fish)
            """
        for fish in find_list:
            multiplier = 100/(1+0.09*item_stats['fish'][fish]['value'])
            for i in range(round(multiplier)):
                possible_finds.append(fish)
        return possible_finds
    