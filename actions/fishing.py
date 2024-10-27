import random
import pygame
from actions import Tool, GameItem, item_stats
from SETTINGS import *


class FishingPole(Tool):
    def __init__(self, group, owner, crew):
        super().__init__(group, owner, crew)
        self.name = 'fishingpole'
        self.catch_interval = 0.5
        self.find_list = ['tuna',
                       'carp',
                       'salmon',
                       'catfish']
       
    def use(self, dt) -> None:
        """every 4 seconds, roll " a dice" to see if you find a fish"""
        self.frame_counter += 1 * dt
        self.timers['using'].activate()
        if self.frame_counter > self.catch_interval:
            self._determine_find_rate()
            possible_finds = self._determine_finds()
            success_check = random.random()
            if success_check <= self.find_rate:
                find = GameItem(self.group, 'fish', random.choice(possible_finds))
                self.owner.inventory.append(find)
                self._animate_a_find(find, dt)
            self.frame_counter = 0
        self._update_timers()

    def _determine_find_rate(self):
        #look at factors that should change find rate for fishing, and then alter the rate
        if self.owner.moving == False:
            self.find_rate_modifiers['movement'] = 0.7
        else:
            self.find_rate_modifiers['movement'] = 0

        for member in self.owner.crew_list:
            if member.role == 'angler':
                self.find_rate_modifiers['crew'] = member.stats['tool_modifier']
        self.find_rate = self.base_find_rate + sum(values for values in self.find_rate_modifiers.values())

    def _determine_finds(self) -> list[str]:
        possible_finds = []
        for fish in self.find_list:
            multiplier = 100/(1+0.09*item_stats['fish'][fish]['value'])
            for i in range(round(multiplier)):
                possible_finds.append(fish)
        return possible_finds
