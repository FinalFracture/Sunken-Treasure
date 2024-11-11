from pygame import sprite, image, surface, rect
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from SETTINGS import *

{'collision':True}

WORLD_LAYERS = {
     'land':{
         'collision':True
         ,'fishing':[]
         ,'mining':[]
         ,'hitbox_mod':5
         ,'movement_mod':{'x':0
                          ,'y':0}
     }
     ,'edge':{
        'collision':True
         ,'fishing':[]
         ,'mining':[]
         ,'hitbox_mod':1
         ,'movement_mod':{'x':0
                          ,'y':0}
     }
     ,'small-waves':{
        'collision':False
         ,'fishing':['-carp', '-catfish', '-salmon']
         ,'mining':[]
         ,'hitbox_mod':1
         ,'movement_mod':{'x':0.9
                          ,'y':0.9}
     }
}

class Map():
    def __init__(self, display_group:sprite.Group, collision_group, map_path:str) -> None:
        """
        A generic map class that will load a tmx file and visualize the tiles on screen

        Parameters:
        
            display_group:sprite.Group Display group for pygame

            collision_group:sprite.Group Sprite group for collision detection

            map_path:str relative path from root directory to the tmx file
        """
        self.map:TiledMap = load_pygame(map_path)
        self.display_group:sprite.Group = display_group
        self.collision_Group:sprite.Group = collision_group
        self.tiles:list[MapTile] = []
        self._visualize_map()
        

    def _visualize_map(self) -> None:
        for index, layer in enumerate(self.map.visible_layers):
            for x_coord, y_coord, tile_image in layer.tiles():
                properties = self.map.get_tile_properties(x_coord, y_coord, index)
                if properties is not None:
                    tile_type = properties['type']
                tile_sprite:sprite.Sprite = MapTile(self.display_group, self.collision_Group, tile_image, (x_coord, y_coord), tile_type=tile_type)
                self.tiles.append(tile_sprite)

class MapTile(sprite.Sprite):
    _all_tiles:list = []

    def __init__(self, display_group:sprite.Group, collision_group:sprite.Group, image:surface.Surface, tile_coord:tuple[int, int], tile_type='land', z=cameragroup_layers['overworld']):
        """
        Sprite for map tiles. Contains logic for collisions, action modifiers, and basic sprite logic.

        Parameters:

            display_group:sprite.Group Display group for the sprite

            collision_group:sprite.Group Group for collidable objects

            image:surface.Surface Rendered image of the map tile

            tile_coord:tuple[int,int] Position of the tile within the map. Not the actual position of the image in the game

            tile_type:str Tile class as assigned in Tiled Map Maker. Determines collision and player modifiers
        """
        super().__init__(display_group)
        MapTile._all_tiles.append(self)
        self.group:sprite.Group = display_group
        self.tile_type = tile_type
        self.z:int = z
        self.image:surface.Surface = image
        tile_size:int = 64
        self.rect:rect.Rect = self.image.get_rect(x=tile_coord[0]*tile_size, y=tile_coord[1]*tile_size)
        self.timers:dict = {}
        self.properties = WORLD_LAYERS[tile_type] 
        self.hitbox = self.rect.copy()   
        self.hitbox.width=self.rect.width*self.properties['hitbox_mod']
        self.hitbox.height=self.rect.height*self.properties['hitbox_mod']
        self.hitbox.center = self.rect.center
        if self.properties['collision']:
            collision_group.add(self) 

    def update(self, dt) -> None:
        self.hitbox.center = self.rect.center

    @classmethod
    def get_tile_fishing_mod(self, player:sprite.Sprite) -> str | None:
        for tile in MapTile._all_tiles:
            if tile.rect.collidepoint(player.rect.center):
                return WORLD_LAYERS[tile.tile_type]['fishing']