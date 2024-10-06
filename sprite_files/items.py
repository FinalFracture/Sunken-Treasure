import pygame
from support import import_folder
from SETTINGS import *
from item_stat_dicts import *
from fishing import FishingPole

class Crew(pygame.sprite.Sprite):
    """This class will create a crew member character and funciton as a tool for the player class 'ship'"""
    def __init__(self, sprite_group, crew_role, owner, z = overlay_layers['hud_elements']):
        super().__init__(sprite_group)
        self.import_assets()
        self.owner = owner
        self.status = 'unselected'
        self.role = crew_role 
        self.stats = crew_stats[self.role].copy()
        self.stats['name'] = generate_name()
        self.stats['tool_modifier'] = generate_tool_modifier()
        self.name = self.stats['name']
        self.tool_modifier = self.stats['tool_modifier']
        self.tools = {'fishing_pole': FishingPole(sprite_group, self.owner)}
        self.image = crew_role_list[self.role][self.status][0]
        self.rect = self.image.get_rect()
        self.z = z
        #group.remove(self)
            
    def import_assets(self):
        for role, status in crew_role_list.items():
            for status in status.keys():
                full_path = 'images/characters/crew/' + role +'/'+ status
                crew_role_list[role][status] = import_folder(full_path)

    def update_status(self, status:str) -> None:
        #change the image and status of the icon
        self.image = crew_role_list[self.role][status][0]