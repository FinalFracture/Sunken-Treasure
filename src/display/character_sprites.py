import random
import pygame
from pygame import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite, spritecollide
from pygame.surface import Surface

from src.utils.support import import_folder
from src.utils.settings import *
from src.utils.cameras import collidable_sprites, all_sprites, cameragroup_layers, overlay_sprites

character_image_paths = 'assets/images/characters//'

class CharacterSprite(Sprite):
    """
    A sprite class that all overworld character sprites will use. 
    
    Attributes
    ----------
    - z:int
        Camera layer to be drawn on the screen
    - master
        Class instance invoking this one as its sprite
    - ship_type:str
        Type of the ship, determines sprite. Must be derived from assets/images/characters.
    - animations:list of list
        Contains a lists of images to loop through for animations
    - image:Surface
        Pygame surface object, this is what is drawn to the screen
    - rect:Rect
        Rectangle representing the bouding box of the image drawn to the screen.
    - hitbox:Rect
        A copt of the image rect, but scaled and used to determine collisions
    - using_tool:bool
        Boolean to indicate what animations to use
    - selected_tool:Tool
        A Tool class. It's name attribute dictate tool use animations
    - status:str
        Indicates what the sprite is doing and direction to face
    - status_hold:str
        Stores the value to revert back to when an animation is over, and keep the correct orientation
    - frame_index:int
        Increments with animation
    - status_rect:Rect
        A rectangle to lay over the top left of the sprite. Used to indicate status and events. 
    - moving:bool
        Boolean to indicate whether or not the sprite is moving
    - collideable:bool
        Boolean to indicate if the object can be colided with
    - speed_multiplier:int
        Integer to alter how fast the sprite moves
    - pos:Vector2
        A vector used for calculating movement of the sprite
    - direction:Vector2
        Vector for determing a normalized direction of sprite movement. 
    """
    def __init__(self, master, starting_pos:tuple, ship_type:str):
        super().__init__(all_sprites)
        collidable_sprites.add(self)
        self.z = cameragroup_layers['main']
        self.master = master
        self.animations:dict[str, list] = {'left': [], 'right': []}
        self.ship_type = ship_type
        self.import_assets('pickaxe')
        self.import_assets('fishing_pole')
        self._animation_setup()
        self._image_setup(starting_pos)
        self._movement_setup()

    def import_assets(self, tool_name):
        """tool_name: name of tool that player uses
            e.g. tool_name = fishing_pole
            This class will locate the file path of each image for the player and store it in a class list"""
        
        for direction in ('left_', 'right_'):
            if not self.animations.get(direction+tool_name):
                self.animations[direction+tool_name] = []

        for animation, image_list in self.animations.items():
            full_path = f'{character_image_paths}{self.ship_type}/' + animation
            self.animations[animation] = import_folder(full_path)
        
    def _image_setup(self, starting_pos):
        #self image and rect
        self.image:Surface = self.animations[self.animation_string][self.frame_index]
        self.rect:Rect = self.image.get_rect()
        self.rect.center = (starting_pos)

        #hitbox
        self.hitbox = self.rect.inflate(0.9, 0.9)

        # interaction space
        self.interaction_box = self.rect.inflate(1.5, 1.5)

        #player indicator image and rect
        self.status_rect = Rect(0,0,20,20) #display small status indicators to the player in this location

    def _animation_setup(self):
        #flags
        self.interacting = False
        self.selected_tool = ''
        self.pointing_dir = 'left' #status to indicate what the sprite is doing/direction to face
        self.animation_string:str = self.pointing_dir + self. selected_tool
        self.frame_index = 0 #increments with animation

    def _movement_setup(self):
        self.moving = False
        self.pos = Vector2(self.rect.center) 
        self.direction = Vector2()
    
    def movement_input(self, keys:list, mouse_pos:tuple[int, int], dt:float):
        #movement normalizing
        if keys[pygame.K_a]: # move left
            self.direction.x = -1
            self.pointing_dir = 'left'

        elif keys[pygame.K_d]: # move right
            self.direction.x = 1
            self.pointing_dir = 'right'
        
        else: #no horizontal movement
            self.direction.x = 0

        if keys[pygame.K_w]: #move up
            self.direction.y = -1

        elif keys[pygame.K_s]: # move down
            self.direction.y = 1

        else: # No vertical movement
            self.direction.y = 0

        self._check_collisions()
        if self.direction.magnitude() > 0:
            self.moving = True
            self.direction = self.direction.normalize()
            self.pos += self.direction * player_speed * dt 
            self.rect.center = self.pos

        else:
            self.moving = False
            
    def _check_collisions(self):
        #detect a colision, and put the player at a position where it is not coliding.
        collided_sprites:list[Sprite] = spritecollide(self, collidable_sprites, False)
        collided_sprites.remove(self)

        def _check_vertical_collisions(rect:Rect) -> int:
            collided_cols:int = 0
            for i in range(self.rect.left, self.rect.right +1): # for each horizontal coord
                if i in range(rect.left, rect.right + 1): # if overlapping with collided object horizontal coord
                    collided_cols += 1
            return collided_cols
   
                
        def _check_horizontal_collisions(rect:Rect) -> int:
            collided_rows:int = 0
            for i in range(self.rect.top, self.rect.bottom +1):
                if i in range(rect.top, rect.bottom + 1):
                    collided_rows += 1
            return collided_rows
        
        def _alter_movement(rows:int, cols:int, collide_rect:Rect) -> None:
            if rows > cols: # horizontal collision
                if self.rect.centerx < collide_rect.centerx and self.direction.x == 1: 
                    # collide on right side of player and moving right
                    self.direction.x = 0

                if self.rect.centerx > collide_rect.centerx and self.direction.x == -1: 
                    # collide on left side of player and moving left
                    self.direction.x = 0

            if cols > rows:
                # vertical collision
                if self.rect.centery < collide_rect.centery and self.direction.y == 1: 
                    # collide on right side of player and moving right
                    self.direction.y = 0
                    
                if self.rect.centery > collide_rect.centery and self.direction.y == -1: 
                    # collide on left side of player and moving left
                    self.direction.y = 0

        for sprite in collided_sprites:
            overlapping_cols:int = _check_vertical_collisions(sprite.rect)
            overlapping_rows:int = _check_horizontal_collisions(sprite.rect)
            _alter_movement(overlapping_rows, overlapping_cols, sprite.rect)
        
    def animate(self, dt):
        self.status_rect.center = (self.rect.centerx, self.rect.top)
        self.frame_index +=4 *dt
        self.animation_string = self.pointing_dir + self.selected_tool

        if self.frame_index >= len(self.animations[self.animation_string]):
            self.frame_index = 0

        self.image = self.animations[self.animation_string][int(self.frame_index)]

    def _update_auxilarry_rects(self):
        #update things like the hitbox rect, status numbers/icons, any element that is suppost to follow the player. 
        #self.hitbox = self.rect.inflate(.8,.5)
        self.hitbox.center = self.rect.center
        self.interaction_box.center = self.rect.center
            
    def update(self, dt):
        self._update_auxilarry_rects()
        self.master.update(dt)
        self.animate(dt)

    def toggle_tool(self, tool_name='', toggle=None):
        if toggle is None:
            if self.selected_tool == '':
                self.selected_tool = '_' + tool_name
            else:
                self.selected_tool = ''
        elif toggle == 0:
            self.selected_tool = ''
