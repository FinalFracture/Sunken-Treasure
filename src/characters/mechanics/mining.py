import random
from src.utils.settings import *
from src.characters.mechanics import Tool, GameItem
from src.event_managing import EVENT_HANDLER

class Pickaxe(Tool):
    def __init__(self, owner, crew):
        super().__init__(owner, crew)
        self.name = 'pickaxe'
        
    def use(self) -> None:
        """every 4 seconds, roll " a dice" to see if you find a stone item"""
        mineral_name = 'sandstone'
        self.frame_counter += 1 * EVENT_HANDLER.dt
        if self.frame_counter > 4:
            self._determine_find_rate()
            success_check = random.random()
            if success_check <= self.find_rate:
                find = GameItem(item_type='mineral', item_name=mineral_name)
                self.retrieve(find)
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
        self.find_rate = self.base_find_rate + sum(values for values in self.find_rate_modifiers.values())

