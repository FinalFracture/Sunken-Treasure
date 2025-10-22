import pygame
from pygame.sprite import Sprite

from src.utils.settings import *
from src.event_managing import EVENT_HANDLER

pygame.display.set_mode((screen_width, screen_height)) #calling from settings, set the height and width of the display window
pygame.display.set_caption('Treasures of the Surf')
pygame.display.set_icon(pygame.image.load('assets\images\items\\fish\carp\carp.png'))
DISPLAY_SURFACE = pygame.display.get_surface()

# drawing layers
cameragroup_layers = {
    'ocean': 10,
    'overworld': 20,
    'events': 30,
    'main': 40,
    'overlay+': 45,
    'hud': 50,
    'items': 60,
    'text': 70
}

overlay_layers = {
    'hud': 10,
    'hud_elements': 20,
    'menu': 30,
    'menu_aux': 35,
    'menu_elements': 40,
    'menu_items': 50,
    'text': 60
}



class Camera_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, surface):
        self.offset.x = player.rect.centerx - screen_width / 2
        self.offset.y = player.rect.centery - screen_height / 2
        for layer in cameragroup_layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    surface.blit(sprite.image, offset_rect)

    def update(self):
        super().update(EVENT_HANDLER.dt)

class Overlay_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def custom_draw(self, surface):
        for layer in overlay_layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    surface.blit(sprite.image, sprite.rect)

    def update(self):
        super().update(EVENT_HANDLER.dt)

#sprite groups
all_sprites = Camera_Group()
overlay_sprites = Overlay_group()
collidable_sprites = pygame.sprite.Group()

def screen_update(focus:Sprite):
    DISPLAY_SURFACE.fill(screen_color)  
    overlay_sprites.update()
    all_sprites.update()
    all_sprites.custom_draw(focus.sprite, DISPLAY_SURFACE) 
    overlay_sprites.custom_draw(DISPLAY_SURFACE)
    pygame.display.update()
