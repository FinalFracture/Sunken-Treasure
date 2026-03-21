import random
from pygame.rect import Rect
from pygame import Vector2
from src.event_managing import EVENT_HANDLER
from src.utils.settings import * 
from src.utils.timer import Timer
from src.utils.cameras import all_sprites
from src.characters.character_loadouts import Character
from src.overlays.character_sprites import Character_Sprite
from src.mechanics import Crew
from src.story.dialogue.dialogue_box import DIALOGUE

class Non_Player_Character(Character):
    """The non player character class will encompass all self moving objects that are not the player."""
    def __init__(self, ship_type, starting_pos=(0,0)):
        super().__init__(ship_type)
        self.sprite:Character_Sprite = Character_Sprite(self, starting_pos, ship_type)
        #initialization setup
        self._npc_setup()
        
    def _npc_setup(self):
        #stats/metric setup
        all_sprites.remove(self.crew_list)
        self.speed = 40
        self.wander_duration = 4000
        self.pause_duration = 2000
        self.wander_range = 150 #can move 75 pixels in any direction from spawn
        self.wander_area = Rect(self.sprite.rect.centerx - self.wander_range, 
                                            self.sprite.rect.centery - self.wander_range,
                                            self.wander_range *2,
                                            self.wander_range * 2 )
        self.direction = Vector2()
        self.pos = self.sprite.rect.center
        self.state = 'normal'

        #logic setup
        wander_timer = Timer(self.wander_duration,starting_func = self._get_direction, running_func= self.move)
        pause_timer = Timer(self.pause_duration, ending_func= wander_timer.activate)
        wander_timer.ending_func = pause_timer.activate
        self.timers['wander'] = wander_timer
        self.timers['pause_wander']= pause_timer
        self.timers['wander'].activate()

    def _get_direction(self):
        if self.sprite.rect.x > self.wander_area.right:
            self.direction.x = -1
        elif self.sprite.rect.x < self.wander_area.left:
            self.direction.x = 1
        else:
            self.direction.x = random.randint(-1, 1)

        if self.sprite.rect.y > self.wander_area.bottom:
            self.direction.y = -1
        elif self.sprite.rect.y < self.wander_area.top:
            self.direction.y = 1
        else:
            self.direction.y = random.randint(-1, 1)

    def move(self, dt):
        self.sprite._check_collisions()
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.pos += self.direction * player_speed * dt 
            self.sprite.rect.center = (0,0) # self.pos
        
    def _get_tool_use(self) -> None:
        #roll a dice to determine if this ship will be fishing, wandering, etc.
        pass
        """
        if len(self.inventory) < 10:
            active_crew:Crew = random.choice(self.crew_list)
            active_crew.tool.use
            #self.tools[active_crew.].use(dt)
        else:
            self.sprite.using_tool = False
            self.sprite.selected_tool = None
        """

    def _get_movement_status(self) -> None:
        #just check for movment and change the self.movement flag
        if self.direction.x !=0 and self.direction.y != 0:
            self.moving = False
        else:
            self.moving = True

    def interact(self, interactor:Crew) -> None:
        #boatshops should give their introduction, then display inventory and trade menu.
        if self.state == 'normal':
            self.state = 'dialog'
            speaking_crew = random.choice(self.crew_list)
            DIALOGUE.start_dialogue(interactor, speaking_crew)

        self.state = DIALOGUE.run()
        return self.state

    def update(self, dt) -> None:
        self._get_tool_use()

class NPCGenerator:
    def __init__(self):
        self.npcs = []
 
    def generate_npc(self, camera_group, ship_type):
        self.npc1 = Non_Player_Character(camera_group, (150, 150), ship_type)
        return self.npc1
