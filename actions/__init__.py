from timer import Timer
from sprite_files.sprites import Generic
from SETTINGS import *

class Tool:
    def __init__(self, group, owner, crew):
        self.base_find_rate = 0.1
        self.owner = owner
        self.crew = crew
        self.find_rate_modifiers = {}
        self.group = group
        self.frame_counter = 0 # used to attempt a fish find every few seconds
        self.timers = {'using':Timer(3000, ending_func = None)}

    def _animate_a_find(self, caught_item, dt):
        current_find = Generic(self.owner.status_rect.topleft, caught_item.image, self.owner.display_groups['all'], z = cameragroup_layers['hud'])
        current_find_image_pos = [self.owner.status_rect.left, self.owner.status_rect.top]

        def _move_up(dt):
            current_find_image_pos[1] -= 40 * dt
            current_find.rect.center = (current_find_image_pos[0], current_find_image_pos[1])

        self.timers[current_find] = Timer(1250, running_func=_move_up, ending_func=current_find.kill)
        self.timers[current_find].activate()

