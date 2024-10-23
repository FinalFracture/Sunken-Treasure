import pygame
from SETTINGS import *
from item_stat_dicts import *

class Crew(pygame.sprite.Sprite):
    """This class will create a crew member character and funciton as a tool for the player class 'ship'"""
    def __init__(self, sprite_group, crew_role, owner, z = overlay_layers['hud_elements']):
        super().__init__(sprite_group)
        self.owner = owner
        self.group = sprite_group
        self.status = 'unselected'
        self.role = crew_role 
        self.stats = crew_stats[self.role].copy()
        self.stats['name'] = generate_name()
        self.stats['tool_modifier'] = generate_tool_modifier()
        self.name = self.stats['name']
        self.tool_modifier = self.stats['tool_modifier']
        self.value = self.stats['value']
        self.tool = {self.stats['tool']:self.stats['tool_class'](self.group, self.owner, crew=self)}
        self.image = self.stats[self.status][0]
        self.rect = self.image.get_rect()
        self.z = z

    def toggle_status(self) -> None:
        #change the image and status of the icon
        if self.status == 'selected':
            self.status = 'unselected'
        elif self.status == 'unselected':
            self.status = 'selected'
        self.image = self.stats[self.status][0]
