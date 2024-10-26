import pygame
import random
from SETTINGS import *
from support import import_folder
from actions import Tool



mineral_stats = {
            'slate': {
                    'image': []
                    ,'value': 4
                    ,'weight': 8
                    ,'rarity': 'Common' 
                    ,'description1': 'Flat stone pieces.'
                    ,'description2': 'Can contain fossils.'
                }
            ,'sandstone': {
                    'image': []
                    ,'value': 2
                    ,'weight': 5
                    ,'rarity': 'Common' 
                    ,'description1': 'Coarse brittle rock.'
                    ,'description2': 'Absorbs water well.'
                }
}

class Pickaxe(Tool):
    def __init__(self, group, owner, crew):
        super().__init__(group, owner, crew)
        self.name = 'pickaxe'
        
    def use(self, dt) -> None:
        """every 4 seconds, roll " a dice" to see if you find a fish"""
        mineral = 'sandstone'
        self.frame_counter += 1 * dt
        self.timers['using'].activate()
        if self.frame_counter > 4:
            self._determine_find_rate()
            success_check = random.random()
            if success_check <= self.find_rate:
                find = Mineral(self.group, mineral)
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

class Mineral(pygame.sprite.Sprite):
    """Managing class for the fish itself. recieve """
    def __init__(self, group, item_name, z = cameragroup_layers['items']):
        super().__init__(group)
        self.name = item_name 
        self.stats = mineral_stats[self.name]
        self.import_assets()
        self.image = self.stats['image'][0]
        self.rect = self.image.get_rect()
        self.z = z
        group.remove(self)
        self.value = self.stats['value']
            
    def import_assets(self):
            full_path = 'images/items/minerals/' + self.name
            self.stats['image'] = import_folder(full_path)
