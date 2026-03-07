import pygame
import random
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, overlay_layers, cameragroup_layers
from src.mechanics.tools import Tool, item_stats, generate_name, generate_tool_modifier
from src.mechanics.tools.fishing import FishingPole
from src.mechanics.tools.mining import Pickaxe
from src.characters.crew_archetypes import ARCHETYPES

def get_tool_class(tool_name:str) -> Tool:
    if tool_name == 'fishing_pole':
        return FishingPole
    elif tool_name == 'pickaxe':
        return Pickaxe

class Crew(pygame.sprite.Sprite):
    """This class will create a crew member character and funciton as a tool for the player class 'ship'"""
    def __init__(self, crew_role:str, master:pygame.sprite.Sprite, z=overlay_layers['menu_items']):
        """
        A Crew will contain an tool used for finding items or performing in game mechanics based on its role.

        Parameters
        - sprite_group: Overlay camera Group

        - crew_role : str
            Name of the role that the class will perform. Determines what tools can be used.

        - owner: 
            Sprite sub-class such as an NPC or the player

        - z : int 
            Drawing layer
        """
        super().__init__(overlay_sprites)
        overlay_sprites.remove(self)
        self.master:pygame.sprite.Sprite = master
        self.status:str = 'unselected'
        self.type = 'generic'
        self.archetype = random.choice(list(ARCHETYPES.keys()))
        self.role:str = crew_role 
        self.stats:dict = item_stats['crew'][self.role].copy()
        self.stats['name'] = generate_name()
        self.stats['tool_modifier'] = generate_tool_modifier()
        self.name:str = self.stats['name']
        self.tool_modifier:float = self.stats['tool_modifier']
        self.value:str = self.stats['value']
        self.tool:Tool = get_tool_class(self.stats['tool'])(self.master, crew=self)
        self.image:pygame.Surface = self.stats[self.status][0]
        self.rect:pygame.Rect = self.image.get_rect()
        self.z:int = z

    def toggle_status(self) -> None:
        #change the image and status of the icon
        if self.status == 'selected':
            self.status = 'unselected'
        elif self.status == 'unselected':
            self.status = 'selected'
        self.image = self.stats[self.status][0]

    def deselect(self):
        self.status = 'unselected'
        self.image = self.stats[self.status][0]
    
    def update(self, dt):
        #print(self.z)
        if self.status == 'selected':
            self.tool.use()
