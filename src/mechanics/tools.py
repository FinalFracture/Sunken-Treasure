# Describe the logic for each tool, what it does, and how it functions

import random
from src.mechanics.items import GameItem, item_stats
from src.utils.settings import *
from src.utils.timer import Timer
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites
from src.event_managing import EVENT_HANDLER
from src.overlays.screen_components import Generic

def generate_tool_modifier():
  bottom_of_range = .05
  top_of_range = .25
  generated_number = random.random()
  adjusted_number = bottom_of_range + generated_number * (top_of_range - bottom_of_range)
  return adjusted_number


class Tool:
    def __init__(self, master):
        self.base_find_rate = 0.1
        self.master = master
        self.find_rate_modifiers = {}
        self.frame_counter = 0 # used to attempt a fish find every few seconds
        self.timers = {} # {'using':Timer(3000, ending_func = None)}

    def retrieve(self, caught_item):
        find_accepted:bool = self.master.master.add_to_inventory(caught_item) # bool to determine if there is inv space

        if find_accepted == True:
            current_find = Generic(all_sprites, self.master.master.sprite.status_rect.center, caught_item.sprite.image, z = cameragroup_layers['items'])
        
            def _move_up(dt):
                current_find.rect.y -= 75 * EVENT_HANDLER.dt
                
            current_find.timers = {current_find:Timer(1250, running_func=_move_up, ending_func=current_find.kill)}
            current_find.timers[current_find].activate()


class FishingPole(Tool):
    def __init__(self, master):
        super().__init__(master)
        self.name = 'fishing_pole'
        self.catch_interval = 0.2
        self.find_list = [
            'tuna',
            'carp',
            'salmon',
            'catfish'
            ]
       
    def use(self) -> None:
        """every 4 seconds, roll " a dice" to see if you find a fish"""
        self.frame_counter += 1 * EVENT_HANDLER.dt
        print(self.frame_counter)
        if self.frame_counter > self.catch_interval:
            self._determine_find_rate()
            possible_finds = self._determine_finds()
            success_check = random.random()
            print(success_check)
            print(self.find_rate)
            if success_check <= self.find_rate:
                find = GameItem('fish', random.choice(possible_finds))
                self.retrieve(find)
            self.frame_counter = 0

    def _determine_find_rate(self):
        #look at factors that should change find rate for fishing, then alter the rate
        if self.master.master.sprite.moving == False:
            self.find_rate_modifiers['movement'] = 0.1
        else:
            self.find_rate_modifiers['movement'] = 0

        self.find_rate_modifiers['crew'] = self.master.tool_effeciency_modifier
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


class Harpoon(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class FishingNet(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Pickaxe(Tool):
    def __init__(self, master):
        super().__init__(master)
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


class TNT(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class StoneCutter(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Clipboard(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Oar(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class MalletAndSaw(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Cutlery(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Scale(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class NeedleAndThread(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class SeaClaw(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class SeerStone(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Compass(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Tap(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class ShovelAndPail(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Spear(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Lockpick(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class Map(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


class BookAndQuill(Tool):
    def __init__(self) -> None:
        pass

    def update(self, *args, **kwargs) -> None:
        pass


TOOL_MAP: dict = {
    'fishing_pole': FishingPole,
    'harpoon': Harpoon,
    'fishing_net': FishingNet,
    'pickaxe': Pickaxe,
    'tnt': TNT,
    'stone_cutter': StoneCutter,
    'clipboard': Clipboard,
    'oar': Oar,
    'mallet_and_saw': MalletAndSaw,
    'cutlery': Cutlery,
    'scale': Scale,
    'needle_and_thread': NeedleAndThread,
    'sea_claw': SeaClaw,
    'seer_stone': SeerStone,
    'compass': Compass,
    'tap': Tap,
    'shovel_and_pail': ShovelAndPail,
    'spear': Spear,
    'lockpick': Lockpick,
    'map': Map,
    'book_and_quill': BookAndQuill,
}

__all__ = [
    'Tool',
    'FishingPole',
    'Harpoon',
    'FishingNet',
    'Pickaxe',
    'TNT',
    'StoneCutter',
    'Clipboard',
    'Oar',
    'MalletAndSaw',
    'Cutlery',
    'Scale',
    'NeedleAndThread',
    'SeaClaw',
    'SeerStone',
    'Compass',
    'Tap',
    'ShovelAndPail',
    'Spear',
    'Lockpick',
    'Map',
    'BookAndQuill',
]

