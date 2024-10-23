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
        super().__init__(camera_group, self.ship_type, starting_loc)
        self.starting_loc = starting_loc
        self.relation = 'new'
        self.dialoge = NPC_dialoge_1['greetings'][self.relation]
            
    def interact(self) -> None:
        #boatshops should give their introduction, then display inventory and trade menu.
        self.dialog_box.dialoge = NPC_dialoge_1["greetings"][self.relation]
        self.relation = 'familiar'
        self.dialog_box.speaking_crew = random.choice(self.crew_list)
        self.interrupt()
        return self.dialog_box

    def update(self, dt) -> None:
        pass