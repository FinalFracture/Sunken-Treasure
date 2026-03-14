from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, overlay_layers, cameragroup_layers

class CrewSprite(Sprite):
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
    
    def __init__(self, selected:Surface, unselected:Surface, z=overlay_layers['menu_items']):

        super().__init__(overlay_sprites)
        overlay_sprites.remove(self)
        self.selected_image = selected
        self.unselected_image = unselected
        self.image:Surface = self.unselected_image
        self.rect:Rect = self.image.get_rect()
        self.z:int = z

class ItemSprite(Sprite):
    def __init__(self, image:Surface, z=cameragroup_layers['items']) -> None:
        super().__init__(overlay_sprites)
        self.image:Surface = image
        self.rect:Rect = self.image.get_rect()
        self.z:int = z
        overlay_sprites.remove(self)
  

