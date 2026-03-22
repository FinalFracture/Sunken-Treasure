import pygame
import random 
from pygame.sprite import Sprite
from pygame.surface import Surface
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites
from src.event_managing import EVENT_HANDLER
from src.overlays.screen_components import Textbox, Generic
from src.mechanics import Crew
from src.story.dialogue.generic_dialogue import get_dialogue

class DialogBox(Sprite):
    
    relations:dict[list[str, str], dict[str, str | int]] = {} 
    #eg. {'gerald lopez and harmony wheeler', {'crew':['gerald lopez', 'harmony wheeler'],'interatctions':4} }

    def __init__(self):
        super().__init__(overlay_sprites)
        self.fontsize  = 12
        self.screen_offset=(27,400)
        self.z = overlay_layers['menu']
        self.dialogue:list[str]
        self.text:str
        self.image = pygame.image.load('assets\images\HUD\dialog_box.png')
        self.rect = self.image.get_rect(topleft=self.screen_offset)
        self.text_box = Textbox(self, self.fontsize, offset=(100,0), position='middleleft')
        self.speaker_space_image = Surface((70,70))
        self.speaker_space=Generic(overlay_sprites
                                 ,(0,0)
                                 ,self.speaker_space_image
                                 ,z=overlay_layers['menu_elements']
                                 ,offset=(15,15)
                                 ,relative_rect=self.rect)
        self.speaker_icon = Generic(overlay_sprites
                                    ,(0,0)
                                    ,Surface((16,16))
                                    ,z=overlay_layers['text']
                                    ,offset=(95,10)
                                    ,relative_rect=self.rect)
        self.display_items = [self, self.text_box, self.speaker_space, self.speaker_icon]
        overlay_sprites.remove(self.display_items)

    def start_dialogue(self, player_crew:Crew, interactee_crew:Crew) -> None:
        #initialize textbox, subject image, and relative display items
        self.dialogue:list[dict[str, Crew |str]] = get_dialogue(self._update_relations(player_crew, interactee_crew))
        self.dialogue_index:int = 0
        self.dialogue_identifier = ''
        self.dialogue_end = False
        self.ready_to_continue:bool = False
        overlay_sprites.add(self.display_items)
        self._change_dialogue()
        
    def update(self, dt):
        pass

    def run(self) -> str:
        
        EVENT_HANDLER.run(self.dialogue_input) 
        if self.dialogue_end == True:
            return self._end_dialogue()
        else:
            self._animate_text()      

    def dialogue_input(self, keys, mouse_pos, dt) -> None:
        def _single_press_operations():
            if keys[pygame.K_w]:
                self.dialogue_index -= 1
                self._change_dialogue()

            elif keys[pygame.K_s]:
                self.dialogue_index += 1
                self._change_dialogue()
            
            if keys[pygame.K_ESCAPE] or (keys[pygame.K_RETURN]):
                self.dialogue_end = True

        self._text_scroll_direction = 0
        if keys[pygame.K_d]:
            self._text_scroll_direction = 1

        elif keys[pygame.K_a]:
            self._text_scroll_direction = -1

        if EVENT_HANDLER.is_key_pressed == False:
                _single_press_operations()
 
    def _check_dialogue_state(self):
        # change dialogue resets dialogue state and prevents exit, but calling the match exits early.
        if self.dialogue_index > len(self.dialogue)-1 and self.text_on_screen_index >= len(self.shown_characters) -1:
            match self.dialogue_identifier: 
                case '%':
                    pass
                case '*':
                    pass
                case '&':
                    pass
                case '':
                    self.dialogue_end = True        

    def _change_dialogue(self) -> None:
        #dialoging setup
        if self.dialogue_index > len(self.dialogue) -1:
            self._check_dialogue_state()
            self.dialogue_index = len(self.dialogue) -1
        elif self.dialogue_index <= 0:
            self.dialogue_index = 0
        if self.dialogue_end == True:
            return
        self.speaker_space_image.fill('black')
        self.speaker = self.dialogue[self.dialogue_index]['speaker']
        self.speaker_space.image = self.speaker.master.sprite.image
        self.speaker_icon.image = self.speaker.sprite.image
        self._text_scroll_direction = 0
        self.text_on_screen_index = 0
        self.shown_characters = []
        self.text = f"{self.dialogue[self.dialogue_index]['speaker'].name}: {self.dialogue[self.dialogue_index]['text']}"
        if len(self.text) < 40:
            self.shown_characters.append(self.text)
        else:
            for character in range(len(self.text)-39):
                self.shown_characters.append(self.text[character:character+40])

    def _end_dialogue(self) -> str:
        overlay_sprites.remove(self.display_items)
        return 'normal'

    def _animate_text(self):
        self.text_on_screen_index += self._text_scroll_direction * EVENT_HANDLER.dt * TEXT_SPEED

        if self.text_on_screen_index > len(self.shown_characters) -1:
            self.text_on_screen_index = len(self.shown_characters) -1  #cap index at max length of string

        if self.text_on_screen_index < 0: #cap min value of index at 0
            self.text_on_screen_index = 0

        self.text_box.text = self.shown_characters[int(self.text_on_screen_index)]

    def _update_relations(self, player_crew:Crew, interactee:Crew) -> dict:
        """
        Add a relation between 2 world crew members and start counting interactions. Update interaction count if
        relation exists already. Set the next dialogue they would have. 
        """
        relationship_key = str(sorted([player_crew.name, interactee.name])) #alphabetize them to ensure consistency in the future
        if relationship_key not in DialogBox.relations.keys():
            DialogBox.relations[relationship_key] = {'interactions':0, 'crew':[player_crew, interactee]} # add the relation 
        
        DialogBox.relations[relationship_key]['interactions'] +=1

        relation:dict = DialogBox.relations[relationship_key]
        interactions = relation['interactions']
        if interactions < 3:
            relation['relation_status'] = 'new'
        elif interactions < 7:
            relation['relation_status'] = 'acquaintance'
        elif interactions < 15:
            relation['relation_status'] = 'familiar'
        elif interactions < 25:
            relation['relation_status'] = 'trusted'
        elif interactions >= 40:
            relation['relation_status'] = 'revered'
        
        return relation


DIALOGUE = DialogBox()