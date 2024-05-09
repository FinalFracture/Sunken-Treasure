import pygame
from SETTINGS import *
from ship import Ship
from shop import BoatShop
from npcs import NPCGenerator

class Level:
    """This class is the root class of the game. This is the main game loop."""
    def __init__(self, game) -> None:
        self.game = game

        #get the display surface
        self.main_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.overlay_sprites = Overlay_group()
        self.collision_group = pygame.sprite.Group()
        self.draw_groups = {0:self.all_sprites, 1:self.overlay_sprites, 2:self.collision_group}

        self.setup()

    def setup(self) -> None:
        #set up sprites
        
        #Initialize the player and assets
        self.player = Ship(self, self.draw_groups)
        self.npc_generator = NPCGenerator()
        self.interactables = [BoatShop(self.draw_groups), self.npc_generator.generate_npc(self.draw_groups, 'fishing_vessel')]
        


        #lists and dicts
        self.pause_overworld_ui_list = [self.player.inventory_ui, self.interactables[0].dialog_box, self.interactables[1].dialog_box]
        self.timers = {}
        self.maps = []

    def run(self, dt):
        #start every frame with a clean screen
        self.main_surface.fill('blue')   

        #draw to the screen and update positions
        self._input()
        self._update_sprites(dt)
        self.update_timers()
        self.update_menus(dt)
        self.all_sprites.custom_draw(self.player) 
        self.overlay_sprites.custom_draw()

    def update_menus(self, dt):
        #determine when to update menu objects
        for menu in self.pause_overworld_ui_list:
            menu.update(dt)

    def update_timers(self) -> None:

        if any(self.timers):
            for timer in self.timers.values():
                timer.update()
        
        
        for sprite in self.all_sprites:
            for timer in sprite.timers.values():
                if any(menu.is_active for menu in self.pause_overworld_ui_list):
                    timer.paused = True
                else:
                    timer.paused = False

    def _input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL] and keys[pygame.K_9]:
            self._save_game()

    def _update_sprites(self, dt):
        for sprite in self.all_sprites:
            try:
                if sprite.collideable and sprite not in self.collision_group:
                    self.collision_group.add(sprite)
            except:
                None

        self.overlay_sprites.update(dt)
        if not any(menu.is_active for menu in self.pause_overworld_ui_list):
            self.all_sprites.update(dt) 

    def _save_game(self):
        save_dict = {'gold': self.player.gold,
                     'pos': (self.player.rect.x, self.player.rect.y),
                     'inventory': self.player.inventory}

        for key, value in save_dict.items():
            self.game.log.write(f'{key} : {value}\n')

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - screen_width / 2
        self.offset.y = player.rect.centery - screen_height / 2
        for layer in cameragroup_layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

class Overlay_group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for layer in overlay_layers.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)
