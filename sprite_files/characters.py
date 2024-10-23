import pygame
import random
from .sprites import DialogBox
from support import import_folder
from timer import Timer
from SETTINGS import *
from sprite_files.items import Crew



class All_Characters(pygame.sprite.Sprite):
    """This class will provide identical shared mechanics that all vessels will use"""
    def __init__(self, groups, starting_pos:tuple, ship_type:str):
        super().__init__(groups['all'])
        self.display_groups = groups
        self.z = cameragroup_layers['main']
        self.starting_pos = starting_pos
        self.ship_type = ship_type
        self._general_setup()
        self.import_assets('pickaxe')
        self.import_assets('fishing_pole')
        self._animation_setup()
        self._image_setup()
        self._movement_setup()

    def import_assets(self, tool_name):
        """tool_name: name of tool that player uses
            e.g. tool_name = fishing_pole
            This class will locate the file path of each image for the player and store it in a class list"""
        if tool_name:
            directions = ('left_', 'right_')
            for direction in directions:
                if not self.animations.get(direction+tool_name):
                    self.animations[direction+tool_name] = []
        for animation, list_of_images in self.animations.items():
            full_path = f'images/characters/{self.ship_type}/' + animation
            self.animations[animation] = import_folder(full_path)
        
    def _general_setup(self):
        #stats setup
        self.gold = 50
        self.inventory = []
        self.timers = {}
        self.crew_list = [Crew(self.display_groups['overlay'], 'rockhound',owner=self), Crew(self.display_groups['overlay'], 'angler',owner=self)] # all characters start with an angler for now
        self.tools = {}
        self.animations = {'left': [], 'right': []}
        for crew in self.crew_list:
            for tool_name, tool in crew.tool.items():
                self.tools[tool_name] = tool
        self.display_groups['collision'].add(self)
        
    def _image_setup(self):
        #self image and rect
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.starting_pos)

        #hitbox
        self.hitbox = self.rect
        self.hitbox.height = self.rect.height*.75
        self.hitbox.top = self.rect.top

        #player indicator image and rect
        self.status_rect= pygame.Rect(0,0,20,20) #display small status indicators to the player in this location

    def _animation_setup(self):
        #flags
        self.using_tool = False
        self.interacting = False
        self.selected_tool = None
        self.status = 'left' #status to indicate what the sprite is doing/direction to face
        self.status_hold = self.status #This stores the value to revert back to when an animation is over, and keep the correct orientation
        self.frame_index = 0 #increments with animation

    def _movement_setup(self):
        self.moving = False
        self.collideable = True
        self.speed_multiplier = 1
        self.pos = pygame.Vector2(self.rect.center) 
        self.direction = pygame.Vector2()
    
    def _move(self, dt):
        #movement normalizing
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.pos += self.direction * self.speed * dt 
            self.rect.center = self.pos
            
    def interrupt(self):
        self.direction.x = 0
        self.direction.y = 0
        for timer in self.timers.values():
            timer.pause()

    def _check_collisions(self):
        #detect a colision, and put the player at a position where it is not coliding. 
        collisions = pygame.sprite.spritecollide(self, self.display_groups['collision'], False)
        if collisions:
            for collided_object in collisions:
                if collided_object != self:
                    if self.hitbox.left > collided_object.rect.centerx:
                        if self.direction.x < 0:
                            self.direction.x = 0
                    elif self.hitbox.right < collided_object.rect.centerx:
                        if self.direction.x > 0:
                            self.direction.x = 0
                    if self.hitbox.top > collided_object.rect.centery:
                        if self.direction.y < 0:
                            self.direction.y = 0
                    elif self.hitbox.bottom < collided_object.rect.centery:
                        if self.direction.y > 0:
                            self.direction.y = 0

    def _get_status(self, dt): 
        """Check for an interaction, tool use, or menu useage"""

        #get tool status
        if self.selected_tool is not None and self.using_tool:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool
            self.tools[self.selected_tool].use(dt)
        elif not self.using_tool:
            self.status = self.status_hold
            #self.tools[self.selected_tool].current_find.kill() #get rid of the sprite that lingers on screen when you stop using the tool during a catch animation.
        #else:  
  
    def animate(self, dt):
        self.status_rect.center = (self.rect.centerx, self.rect.top)
        self.frame_index +=4 *dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def _update_auxilarry_rects(self):
        #update things like the hitbox rect, status numbers/icons, any element that is suppost to follow the player. 
        #self.hitbox = self.rect.inflate(.8,.5)
        self.hitbox.top = self.rect.top

    def _update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
        
    def resume_timers(self):
        for timer in self.timers.values():
            timer.resume()
            
    def update(self, dt):
        self._check_collisions()
        self._get_status(dt)
        self._update_auxilarry_rects()
        self.animate(dt)
        self._update_timers()

class NonPlayerCharacter(All_Characters):
    """The non player character class will encompass all self moving objects that are not the player."""
    def __init__(self, groups, ship_type, starting_pos=(0,0)):
        super().__init__(groups, starting_pos, ship_type)
        #initialization setup
        self._npc_setup(groups)
        self.dialog_box = DialogBox(groups
                                    ,self
                                    ,random.choice(self.crew_list)
                                    ,self.image
                                    )

    def _npc_setup(self, groups):
        #stats/metric setup
        groups['overlay'].remove(self.crew_list)
        self.speed = 40
        self.wander_duration = 4000
        self.pause_duration = 2000
        self.wander_range = 150 #can move 75 pixels in any direction from spawn
        self.wander_area = pygame.rect.Rect(self.rect.centerx - self.wander_range, 
                                            self.rect.centery - self.wander_range,
                                            self.wander_range *2,
                                            self.wander_range * 2 )
        self.direction = pygame.Vector2()
        self.pos = self.rect.center

        #logic setup
        wander_timer = Timer(self.wander_duration,starting_func= self._get_direction, running_func= self._move)
        pause_timer = Timer(self.pause_duration, ending_func= wander_timer.activate)
        wander_timer.ending_func = pause_timer.activate
        self.timers['wander'] = wander_timer
        self.timers['pause_wander']= pause_timer
        self.timers['wander'].activate()

    def _get_direction(self):
        if self.rect.x > self.wander_area.right:
            self.direction.x = -1
        elif self.rect.x < self.wander_area.left:
            self.direction.x = 1
        else:
            self.direction.x = random.randint(-1, 1)

        if self.rect.y > self.wander_area.bottom:
            self.direction.y = -1
        elif self.rect.y < self.wander_area.top:
            self.direction.y = 1
        else:
            self.direction.y = random.randint(-1, 1)
        
        self._get_tool_use()

    def _get_tool_use(self) -> None:
        #roll a dice to determine if this ship will be fishing, wandering, etc.
        if len(self.inventory) < 10:
            self.using_tool = True
        else:
            self.using_tool = False

    def _get_movement_status(self) -> None:
        #just check for movment and change the self.movement flag
        if self.direction.x !=0 and self.direction.y != 0:
            self.moving = False
        else:
            self.moving = True