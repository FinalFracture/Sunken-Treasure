import random
import pygame
from actions import Tool
from support import import_folder
from SETTINGS import *

fish_stats = {
            'tuna': {
                    'image': []
                    ,'value': 250
                    ,'weight': 55
                    ,'rarity': 'Rare' 
                    ,'description1': 'A massive fish. Just'
                    ,'description2': '1 can feed a village.'
                }
            ,'catfish': {
                    'image': []
                    ,'value': 35
                    ,'weight': 5
                    ,'rarity': 'uncommon'
                    ,'description1': 'Large bottom feeding fish.' 
                    ,'description2':'Easier to find while still.' 
                }
            ,'salmon': {
                    'image': []
                    ,'value': 23
                    ,'weight': 3
                    ,'rarity': 'common' 
                    ,'description1': 'A treat to some groups.' 
                    ,'description2':'Prefers colder climates.'
                }
            ,'carp': {
                'image': []
                ,'value': 5
                ,'weight': 8
                ,'rarity': 'common' 
                ,'description1':'Extremely common, carp ' 
                ,'description2':'are an invasive species.'
            }
}

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
                find = Fish(self.group, random.choice(possible_finds))
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
            multiplier = 100/(1+0.09*fish_stats[fish]['value'])
            for i in range(round(multiplier)):
                possible_finds.append(fish)
        return possible_finds

class Fish(pygame.sprite.Sprite):
    """Managing class for the fish itself. recieve """
    def __init__(self, group, item_name, z = cameragroup_layers['items']):
        super().__init__(group)
        self.name = item_name 
        self.stats = fish_stats[self.name]
        self.import_assets()
        self.image = self.stats['image'][0]
        self.rect = self.image.get_rect()
        self.z = z
        group.remove(self)
        self.value = self.stats['value']
            
    def import_assets(self):
            full_path = 'images/items//fish/' + self.name
            self.stats['image'] = import_folder(full_path)