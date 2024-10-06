import pygame
from SETTINGS import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, topleft_pos, surf, groups, z = cameragroup_layers['main'], offset=(0,0), relative_rect=None):
        super().__init__(groups)
        self.timers = {}
        self.image = surf
        if relative_rect:
            self.rect = self.image.get_rect(top=relative_rect.top+offset[1], left=relative_rect.left+offset[0])
        else:
            self.rect = self.image.get_rect(topleft = topleft_pos)
        self.group = groups
        self.z = z

class Textbox(pygame.sprite.Sprite):

    def __init__(self, group, relative_surface, fontsize = 12, z = overlay_layers['menu_elements'], offset = (0,0), owner=None):
        super().__init__(group)
        self.group = group
        self.owner=owner
        self.relative_surface_sprite = relative_surface
        self.relative_surface = relative_surface.rect
        self.fontsize = fontsize
        self.text = ''
        self.color = 'black'
        self.offset = pygame.Vector2(offset)
        self.z = z
        self.is_active = False
        self._text_setup()

    def _text_setup(self):
        self.font = pygame.font.Font('C:\Windows\Fonts\\vgafix.fon', 12)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect(topleft = (self.relative_surface.x + self.offset.x, self.relative_surface.y + self.offset.y))

    def update(self, dt):
        self.image = self.font.render(self.text.title(), True, self.color)

class DialogBox(pygame.sprite.Sprite):
    def __init__(self, groups:pygame.sprite.Group, owner:pygame.sprite.Sprite, font_size=12, font_color='black'):
        super().__init__(groups['overlay'])
        self.group = groups['overlay']
        self.owner = owner
        self.fontsize = font_size
        self.screen_offset=(27,400)
        self.z = overlay_layers['menu']
        self.dialoge = ''
        self.text = ''
        self.speaking_crew = None
        self.image = pygame.image.load('images\HUD\dialog_box.png')
        self.rect = self.image.get_rect(topleft=self.screen_offset)
        self.text_box = Textbox(self.group, self, font_size, offset=(100,50))
        self.display_items = [self, self.text_box]
        self.group.remove(self.display_items)
        self.is_active = False

    def setup_display_items(self, interactee:pygame.sprite.Sprite) -> None:
        #initialize textbox, subject image, and relative display items
        self.subject_box=Generic((0,0)
                                 ,interactee.image
                                 ,self.group
                                 ,z=overlay_layers['menu_elements']
                                 ,offset=(20,20)
                                 ,relative_rect=self.rect)
        self.speaker_icon = Generic((0,0)
                                    ,self.speaking_crew.image
                                    ,self.group
                                    ,z=overlay_layers['text']
                                    ,offset=(95,10)
                                    ,relative_rect=self.rect)
        self.display_items.append(self.speaker_icon)
        self.display_items.append(self.subject_box)


        #dialoging setup
        self.ready_to_continue = False
        self.text_scroll_direction = 0
        self.text_on_screen_index = 0
        self.shown_characters = []

    def update(self, dt):
        if self.is_active:
            self.text_box.text = self.text
            self._animate_text(dt)
            

    def process_text(self, interactee):
        self.is_active = True
        self.setup_display_items(interactee)
        self.text = f'{self.speaking_crew.name}: {self.dialoge}'
        self.group.add(self.display_items) #if having trouble removing, its probably because this gets run multiople times4
        for character in range(len(self.text)-40):
            self.shown_characters.append(self.text[character:character+40])
        self.dialoge_identifier = self.text[-1]
        self._check_status()


    def _animate_text(self, dt):
        if self.text_on_screen_index > len(self.shown_characters) -1:
            self.text_on_screen_index = len(self.shown_characters) -1  #cap index at max length of string
            self.ready_to_continue = True

        elif self.text_on_screen_index < 0: #cap min value of index at 0
            self.text_on_screen_index = 0

        else:  #allow text scrolling between 0 and max index value
            self.text_on_screen_index += self.text_scroll_direction * dt * TEXT_SPEED

        self.text = self.shown_characters[int(self.text_on_screen_index)]

    def _end_dialoge(self):
        self.is_active = False
        if self.dialoge_identifier == '&':
            self.owner.resume_timers()
        self.text_on_screen_index = 0
        self.shown_characters = []
        self.group.remove(self.display_items)

    def _check_status(self) -> None:
        if self.dialoge_identifier == '*':
            self.dialoge_type = 'menu'
        elif self.dialoge_identifier == '%':
            self.dialoge_type == 'yes/no'
        elif self.dialoge_identifier == '&':
            self.dialoge_type = 'basic'