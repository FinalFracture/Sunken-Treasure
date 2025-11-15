import pygame
import random 
from pygame.sprite import Sprite
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites
from src.event_managing import EVENT_HANDLER
from src.overlays.screen_components import Textbox, Generic
from src.characters.crew import Crew
from src.story.dialoge.generic_dialogue import get_dialoge

class DialogBox(Sprite):
    
    relations:dict[list[str, str], dict[str, str | int]] = {} 
    #eg.  {'gerald lopez and harmony wheeler', {'crew':['gerald lopez', 'harmony wheeler'],'interatctions':4} }

    def __init__(self):
        super().__init__(overlay_sprites)
        self.fontsize  = 12
        self.screen_offset=(27,400)
        self.z = overlay_layers['menu']
        self.dialoge:list[str]
        self.text:str
        self.image = pygame.image.load('assets\images\HUD\dialog_box.png')
        self.rect = self.image.get_rect(topleft=self.screen_offset)
        self.text_box = Textbox(self, self.fontsize, offset=(100,0), position='middleleft')
        self.display_items = [self, self.text_box]
        overlay_sprites.remove(self.display_items)

    def start_dialoge(self, player_crew:Crew, interactee_crew:Crew) -> None:
        #initialize textbox, subject image, and relative display items
        self.dialoge:list[str] = get_dialoge(self._update_relations(player_crew, interactee_crew))
        self.dialogue_index:int = 0
        self.dialogue_identifier = ''
        self._change_dialogue()
        self.dialoge_end = False
        self.ready_to_continue:bool
        print(self.dialoge)
        
    def update(self, dt):
        pass 

    def run(self) -> str:
        
        EVENT_HANDLER.run(self.dialoge_input) 
        if self.dialoge_end == True:
            return self._end_dialoge()
        
        self._animate_text()      

    def _animate_text(self):
        self.text_on_screen_index += self._text_scroll_direction * EVENT_HANDLER.dt * TEXT_SPEED

        if self.text_on_screen_index > len(self.shown_characters) -1:
            self.text_on_screen_index = len(self.shown_characters) -1  #cap index at max length of string

        if self.text_on_screen_index < 0: #cap min value of index at 0
            self.text_on_screen_index = 0

        self.text_box.text = self.shown_characters[int(self.text_on_screen_index)]

    def _check_dialogue_state(self):
        if self.dialogue_index > len(self.dialoge) -1:
            self.dialogue_index = len(self.dialoge) -1
        if self.dialogue_index <= 0:
            self.dialogue_index = 0
        if self.dialogue_index == len(self.dialoge)-1 and self.text_on_screen_index == len(self.shown_characters) -1:
            self.ready_to_continue = True
        if self.text != self.dialoge[self.dialogue_index]['text']:
            self._change_dialogue()
        elif self.ready_to_continue == True:
            match self.dialogue_identifier:
                case '%':
                    pass
                case '*':
                    pass
                case '&':
                    pass
                case '':
                    self.dialoge_end = True

    def _change_dialogue(self) -> None:
        #dialoging setup
        print(self.dialogue_index)
        self.speaker = self.dialoge[self.dialogue_index]['speaker']
        try:
            self.subject_box.kill()
            self.speaker_icon.kill()
        except AttributeError:
            pass # skip initial call, when they don't exist

        self.subject_box=Generic(overlay_sprites
                                 ,(0,0)
                                 ,self.speaker.master.sprite.image
                                 ,z=overlay_layers['menu_elements']
                                 ,offset=(20,20)
                                 ,relative_rect=self.rect)
        self.speaker_icon = Generic(overlay_sprites
                                    ,(0,0)
                                    ,self.speaker.image
                                    ,z=overlay_layers['text']
                                    ,offset=(95,10)
                                    ,relative_rect=self.rect)
        self.display_items.append(self.speaker_icon)
        self.display_items.append(self.subject_box)
        overlay_sprites.add(self.display_items)

        self._text_scroll_direction = 0
        self.text_on_screen_index = 0
        self.shown_characters = []
        self.text = self.dialoge[self.dialogue_index]['text']
        if len(self.text) < 40:
            self.shown_characters.append(self.text)
        else:
            for character in range(len(self.text)-40):
                self.shown_characters.append(self.text[character:character+40])
        print(self.dialogue_index)

    def _end_dialoge(self) -> str:
        overlay_sprites.remove(self.display_items)
        self.display_items = [self, self.text_box]
        return 'normal'

    def dialoge_input(self, keys, mouse_pos, dt) -> None:
        def _single_press_operations():
            if keys[pygame.K_w]:
                self.dialogue_index -= 1
                self._check_dialogue_state()

            elif keys[pygame.K_s]:
                self.dialogue_index += 1
                self._check_dialogue_state()

            if keys[pygame.K_RETURN]:
                self._check_dialogue_state()
            
            if keys[pygame.K_ESCAPE] or (keys[pygame.K_RETURN] and self.dialoge_end):
                self.dialoge_end = True

        self._text_scroll_direction = 0
        if keys[pygame.K_d]:
            self._text_scroll_direction = 1

        elif keys[pygame.K_a]:
            self._text_scroll_direction = -1

        if EVENT_HANDLER.is_key_pressed == False:
                _single_press_operations()
    
    def _update_relations(self, player_crew:Crew, interactee:Crew) -> dict:
        """
        Add a relation between 2 world crew members and start counting interactions. Update interaction count if
        relation exists already. Set the next dialoge they would have. 
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


DIALOGE = DialogBox()