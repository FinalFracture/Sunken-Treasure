import pygame
from SETTINGS import *
from actions import Tool, item_stats, generate_name, generate_tool_modifier
from actions.fishing import FishingPole
from actions.mining import Pickaxe


def get_tool_class(tool_name:str) -> Tool:
    if tool_name == 'fishing_pole':
        return FishingPole
    elif tool_name == 'pickaxe':
        return Pickaxe

class Crew(pygame.sprite.Sprite):
    """This class will create a crew member character and funciton as a tool for the player class 'ship'"""
    def __init__(self, sprite_group:pygame.sprite.Group, crew_role:str, owner:pygame.sprite.Sprite, z=overlay_layers['hud_elements']):
        """
        A Crew will contain an tool used for finding items or performing in game mechanics based on its role.

        Args:
            sprite_group: Overlay camera Group

            crew_role: Name of the role that the class will perform. Determines what tools can be used.

            owner: Sprite sub-class such as an NPC or the player

            z: Drawing layer
        """
        super().__init__(sprite_group)
        self.owner:pygame.sprite.Sprite = owner
        self.group:pygame.sprite.Group = sprite_group
        self.status:str = 'unselected'
        self.role:str = crew_role 
        self.stats:dict = item_stats['crew'][self.role].copy()
        self.stats['name'] = generate_name()
        self.stats['tool_modifier'] = generate_tool_modifier()
        self.name:str = self.stats['name']
        self.tool_modifier:float = self.stats['tool_modifier']
        self.value:str = self.stats['value']
        self.tool = {self.stats['tool']:get_tool_class(self.stats['tool'])(self.group, self.owner, crew=self)}
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
