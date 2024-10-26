import pygame
from SETTINGS import *
from input_manager import EventHandler
from ship import Ship
from shop import BoatShop
from npcs import NPCGenerator
from sprite_files.items import Crew
from item_stat_dicts import items_init

class Level:
    """The main game loop. Highest level logic"""
    def __init__(self, game) -> None:
        self.game = game
        items_init()

        #get the display surface
        self.main_surface = pygame.display.get_surface()

        #sprite groups
        self.all_sprites = CameraGroup()
        self.overlay_sprites = Overlay_group()
        self.collision_group = pygame.sprite.Group()
        self.draw_groups = {'all':self.all_sprites, 'overlay':self.overlay_sprites, 'collision':self.collision_group}

        self.setup()

    def setup(self) -> None:
        """Initialize major game assets"""
        #Initialize the player and assets
        self.player = Ship(self, self.draw_groups, 'galleon')
        self.event_handler = EventHandler(self.player)
        self.npc_generator = NPCGenerator()

        # npc's needs a generating function/logic to get rid of this awful list idea. Next important move i guess
        self.interactables = [BoatShop(self.draw_groups, 'raft'), self.npc_generator.generate_npc(self.draw_groups, 'sloop')]
        
        #lists and dicts
        self.game_state = 'normal'
        self.dialoge_boxes = [npc.dialog_box for npc in self.interactables if npc.dialog_box]
        self.pause_overworld_ui_list = [self.player.inventory_ui, self.interactables[0].inventory_ui]
        self.maps = []

    def run(self, dt):
        #start every frame with a clean screen
        self._check_game_state()
        self.main_surface.fill('blue')   

        #draw to the screen and update positions
        self.event_handler.run(dt, self.game_state)
        self.update_timers()
        if self.game_state == 'normal':
            self.overlay_sprites.update(dt)
            self.all_sprites.update(dt)
        elif self.game_state in ('menu', 'dialoge'):
            self.overlay_sprites.update(dt)
            self.update_menus(dt)
        self.all_sprites.custom_draw(self.player) 
        self.overlay_sprites.custom_draw()

    def update_menus(self, dt):
        #determine when to update menu objects
        if any(menu.is_active for menu in self.pause_overworld_ui_list):
            for menu in self.pause_overworld_ui_list:
                menu.update(dt)

    def update_timers(self) -> None:
        """Update any time or clock based functions for each sprite.""" 
        for sprite in self.all_sprites:
            for timer in sprite.timers.values():
                timer.update()

    def _check_game_state(self) -> None:
        if any(menu.is_active for menu in self.pause_overworld_ui_list):
            self.game_state = 'menu'
        elif any(dialoge_box.is_active for dialoge_box in self.dialoge_boxes):
            self.game_state = 'dialoge'
        else:
            self.game_state = 'normal'

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
                #if type(sprite) == Crew:
                    #self.display_surface.blit(sprite.image, sprite.rect)
