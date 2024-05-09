import random
from sprite_files.items import Fish
from sprite_files.sprites import Generic
from timer import Timer
from SETTINGS import *

standard_catch_list = ['tuna',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'carp',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'salmon',
                       'catfish',
                       'catfish',
                       'catfish',
                       'catfish',
                       'catfish',
                       'catfish'
]

class FishingPole:
    def __init__(self, group, owner):
        self.base_catch_rate = 0.1
        self.owner = owner
        self.catch_rate_modifiers = {}
        self._determine_fish_catch_rate()
        self.group = group
        self.possible_catches = standard_catch_list[:]
        self.frame_counter = 0 # used to attempt a fish catch every few seconds
        self.animation_timer = Timer(1250, running_func= self.animation_move_up)
        
    def use(self, dt) -> None:
        """every 4 seconds, roll " a dice" to see if you catch a fish"""
        self.frame_counter += 1 * dt
        if self.frame_counter > 4:
            self._determine_fish_catch_rate()
            success_check = random.random()
            if success_check <= self.catch_rate:
                catch = Fish(self.group, random.choice(self.possible_catches))
                self.owner.inventory.append(catch)
                self._animate_a_catch(catch, dt)
            self.frame_counter = 0
        self.animation_timer.update()

    def _animate_a_catch(self, caught_item, dt):
        self.current_catch = Generic(self.owner.status_rect.topleft, caught_item.image, self.owner.groups[0], z = cameragroup_layers['hud'])
        self.catch_image_pos = [self.owner.status_rect.left, self.owner.status_rect.top]
        self.animation_timer.ending_func = self.current_catch.kill
        self.animation_timer.activate()

    def animation_move_up(self, dt):
        self.catch_image_pos[1] -= 40 * dt
        self.current_catch.rect.center = (self.catch_image_pos[0], self.catch_image_pos[1])

    def _determine_fish_catch_rate(self):
        #look at factors that should change catch rate for fishing, and then alter the rate
        if self.owner.moving == False:
            self.catch_rate_modifiers['movement'] = 0.1
        else:
            self.catch_rate_modifiers['movement'] = 0

        for member in self.owner.crew_list:
            if member.role == 'fisherman':
                self.catch_rate_modifiers['crew'] = member.stats['tool_modifier']
        self.catch_rate = self.base_catch_rate + sum(values for values in self.catch_rate_modifiers.values())
