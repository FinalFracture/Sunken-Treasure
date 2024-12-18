import pygame
import random
from SETTINGS import *
from support import import_folder
from actions import Tool, GameItem

class Pickaxe(Tool):
    def __init__(self, group, owner, crew):
        super().__init__(group, owner, crew)
        self.name = 'pickaxe'
        
    def use(self, dt) -> None:
        """every 4 seconds, roll " a dice" to see if you find a fish"""
        mineral_name = 'sandstone'
        self.frame_counter += 1 * dt
        self.timers['using'].activate()
        if self.frame_counter > 4:
            self._determine_find_rate()
            success_check = random.random()
            if success_check <= self.find_rate:
                find = GameItem(self.group, 'mineral', mineral_name )
                self.owner.inventory.append(find)
                self._animate_a_find(find, dt)
            self.frame_counter = 0
        self._update_timers()

    def _determine_find_rate(self):
        #look at factors that should change find rate for fishing, and then alter the rate
        if self.owner.moving == False:
            self.find_rate_modifiers['movement'] = 0.1
        else:
            self.find_rate_modifiers['movement'] = 0

        for member in self.owner.crew_list:
            if member.role == 'angler':
                self.find_rate_modifiers['crew'] = member.stats['tool_modifier']
        self.find_rate = self.base_find_rate + sum(values for values in self.find_rate_modifiers.values())

