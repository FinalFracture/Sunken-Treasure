import pygame, random
from support import import_folder
from npc_dialog_trees import NPC_dialoge_1

from sprite_files.characters import NonPlayerCharacter


class NPCGenerator:
    def __init__(self):
        self.npcs = []

    def generate_npc(self, camera_group, ship_type):
        self.npc1 = GenericNPC(camera_group, (150, 150), ship_type)
        return self.npc1

class GenericNPC(NonPlayerCharacter):
    def __init__(self, camera_group:pygame.sprite.Group, starting_loc:tuple[int,int], ship_type:str, *crew):
        self.ship_type = ship_type
        self._import_assets()
        super().__init__(camera_group, starting_loc)
        self.starting_loc = starting_loc
        self.image = self.animations[self.status][self.frame_index]
        self.relation = 'new'
        self.dialoge = NPC_dialoge_1['greetings'][self.relation]

    def _import_assets(self):
        """load each animation frame for the corresponding direction, into the list of images for that direction."""
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [], 
                           'up_fishing_pole':[], 'down_fishing_pole':[], 'left_fishing_pole':[], 'right_fishing_pole':[]
                             }
        for animation in self.animations.keys():
            full_path = f'images/characters/npcs/{self.ship_type}/{animation}'
            self.animations[animation] = import_folder(full_path)
            
    def interact(self, interactor):
        #this will be interesting to overcome. Will likey need to make another dictionary with interaciton stuff. 
        dialoge = NPC_dialoge_1['greetings'][self.relation]
        self.dialog_box.process_text(dialoge, interactor, random.choice(self.crew_list))
        self.relation = 'familiar'

    def update(self, dt) -> None:
        pass