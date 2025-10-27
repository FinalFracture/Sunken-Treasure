import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite
from math import ceil, floor
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites
from src.event_managing import EVENT_HANDLER

class Overlay(pygame.sprite.Sprite):
    def __init__(self, owner):
        super().__init__(overlay_sprites)
        self.master = owner
        self.image = pygame.image.load('assets\images\hud/heads_up.png').convert_alpha()
        self.rect = self.image.get_rect(centerx=screen_width/2, bottom=screen_height)
        self.z = overlay_layers['hud']
        self.gold = Textbox(self, z=overlay_layers['hud_elements'], offset=(135, 10), position='relative')
        self.bearing = Textbox(self, z=overlay_layers['hud_elements'], offset=(395, 35), position='relative')
        self.storage = Textbox(self, z=overlay_layers['hud_elements'], offset=(135, 50), position='relative')
        self.knots = Textbox(self, z=overlay_layers['hud_elements'], offset=(280, 35), position='relative')
        self.textboxes = [self.gold, self.bearing, self.storage, self.knots]
        self.crew_icon_topleft_positions ={'crew_member_1': (self.rect.x + 16, self.rect.y+30)
                                            ,'crew_member_2': (self.rect.x+40,self.rect.y+30)
                                            ,'crew_member_3': (self.rect.x+65,self.rect.y+30)
                                            ,'crew_member_4': (self.rect.x+16,self.rect.y+54)
                                            ,'crew_member_5': (self.rect.x+40,self.rect.y+54)
                                            ,'crew_member_6': (self.rect.x+65,self.rect.y+54)
                                            }
        self.crew_list = {}

    def update(self, dt):
        self._update_textboxes()

    def _update_textboxes(self) -> None:
        if self in overlay_sprites and (self.textboxes not in overlay_sprites):
            overlay_sprites.add(self.textboxes)
        self.gold.text = str(self.master.gold)
        self.bearing.text = (str(self.master.gps_coord))
        self.storage.text = self.master.get_inv_level()
        self.knots.text = str(self.master.knotical_speed)
    

    def position_crew_icons(self, crew_list):
        for member_number, member_role in enumerate(crew_list):
            self.crew_list[member_number] = member_role
        for crew_index, crew_icon in self.crew_list.items():
            overlay_sprites.add(crew_icon)
            crew_icon.rect.topleft = self.crew_icon_topleft_positions[f'crew_member_{crew_index+1}']

class ItemStatBox(pygame.sprite.Sprite):
    #the sprite to display an items value, description, weight, and other values
    #while the inventory menu is active
    def __init__(self, relative_rect: pygame.rect.Rect, offset: tuple, z=overlay_layers['menu_aux']):    
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets\images\HUD/item_stat_textbox.png')
        self.rect = self.image.get_rect(topleft = (relative_rect.x + offset[0], relative_rect.y + offset[1]))
        self.item_name_display = HoverMessage(self, offset = (10, 5), fontsize=12)
        self.item_value_display = HoverMessage(self, offset = (10,20), fontsize=12)
        self.item_description_line1 = HoverMessage(self, offset = (10,35), fontsize=12)
        self.item_description_line2 = HoverMessage(self, offset = (10,50), fontsize=12)
        self.z = z
        self.ui_elements = [self.item_name_display, self.item_value_display, self.item_description_line1, self.item_description_line2]

class UiButton(pygame.sprite.Sprite):
    def __init__(self, button_text:str, button_func:callable, func_arg, refrence_rect:pygame.Rect, topleft_offset:tuple[int,int], z=overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.name = button_text
        self.image = self._image_setup()
        self.rect = self.image.get_rect(topleft = (refrence_rect.x + topleft_offset[0], refrence_rect.y + topleft_offset[1]))
        self.z = z
        self.function = button_func
        self.arg = func_arg
        self.textboxes = [Textbox(self, text=button_text)]

    def update(self, dt) -> None:
        self._update_textboxes()
 
    def _update_textboxes(self) -> None:
        if (self in overlay_sprites) and (self.textboxes not in overlay_sprites):
            overlay_sprites.add(self.textboxes)

    def position(self, reference_rect:pygame.Rect, offset:tuple[int,int]) -> None:
        self.rect.x = reference_rect.x + offset[0]
        self.rect.y = reference_rect.y + offset[1]

    def _image_setup(self) -> pygame.Surface:
        image_path = 'assets\images\HUD/sidebar.png'
        image = pygame.image.load(image_path)
        return image

    def click(self) -> None:
        self.function(self.arg)

class Icon_bg(pygame.sprite.Sprite):
    def __init__(self, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets\images\HUD/icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator:bool = None
        self.value_display = Textbox(self, fontsize= 8, z=overlay_layers['text'])
        self.indicator:MenuIndicator = MenuIndicator(self.rect)
        overlay_sprites.remove(self.indicator)

    def update(self, dt): 
        if self.subject:
            self.subject.rect.center = self.rect.center
            self.value_display.text=str(self.subject.value)
            self.value_display.rect.center = (self.rect.x, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.text=''
    
    def click(self, toggle=None):
        #define what happens when the mouse clicks while in the rect boundary of an icon bg.
        if toggle == 0:
            self.indicator.de_indicate()
            if self.subject is not None:
                self.subject.selected = False
        elif toggle == 1:
            self.subject.selected = True
            self.indicator.indicate()   
        else:
            if self.subject is not None and not self.subject.selected:
                self.click(toggle=1)
            elif self.subject is not None and self.subject.selected:
                self.click(toggle=0)

class UpgradeIconBg(pygame.sprite.Sprite):
    def __init__(self, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets\images\HUD/upgrade_icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator = None
        self.selected = False 
        self.value_display = Textbox(self, fontsize= 8, z=overlay_layers['text'])

    def update(self, dt): 
        if self.subject:
            self.subject.rect.center = self.rect.center
            self.value_display.text=str(self.subject.value)
            self.value_display.rect.center = (self.rect.x-5, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.text=''
            
    def deselect(self):
        #this will be called any time we need the inventory item to be deselected by any process
        self.indicator.kill()
    
    def click(self, toggle=None):
        #define what happens when the mouse clicks while in the rect boundary of an icon bg.
        if toggle == 0:
            self.deselect()
        elif toggle == 1:
            self.indicator = MenuIndicator(self.rect)
            self.selected = True
        else:
            if self.subject and not self.selected:
                self.indicator = MenuIndicator(self.rect)
                self.selected = True
            if self.subject and self.selected:
                self.deselect()

class MenuIndicator(pygame.sprite.Sprite):
    """When the player selects items to purchase, this class highlights the selected item slots to 
    visually indicate what has been selected. This will also apply to any other menues where inventory
    slots are selected, and not immediately resolved."""
    def __init__(self, owning_rect, z = overlay_layers['menu_aux']):
        super().__init__(overlay_sprites)
        self.z = z
        self.reference_rect = owning_rect
        self.image = pygame.Surface((owning_rect.width, owning_rect.height))
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width + 6
        self.rect.height = self.rect.height + 6
        self.rect.center = owning_rect.center
        self.image.fill(color='Green')

    def indicate(self) -> None:
        overlay_sprites.add(self)
        self.rect.center = self.reference_rect.center

    def de_indicate(self) -> None:
        overlay_sprites.remove(self)

class HoverMessage(pygame.sprite.Sprite):
    """This class is a message that displays at its specified coords. it is uninteractable."""
    def __init__(self
                 ,relative_surface:pygame.rect.Rect
                 ,fontsize = 20
                 ,z = overlay_layers['menu_elements']
                 ,offset = (0,0)
                 ,max_lines = 2 
                 ,color = 'black'):
        super().__init__(overlay_sprites)
        self.relative_surface_sprite = relative_surface
        self.relative_surface = relative_surface.rect
        self.fontsize = fontsize
        self.max_line_length = 20
        self.max_lines = max_lines
        self.text = ''
        self.color = color
        self.offset = pygame.Vector2(offset)
        self.z = z

        #dialoging setup
        self._text_setup()

    def _text_setup(self):
        self.font = pygame.font.Font('assets\\fonts\\standard.ttf', self.fontsize)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect(topleft = (self.relative_surface.x + self.offset.x, self.relative_surface.y + self.offset.y))

    def update(self, dt):
        self.process_text()

    def process_text(self):
        #to be called by other classes when they need to modify this classes text
        self.image = self.font.render(self.text, False, self.color)
 
class Generic(pygame.sprite.Sprite):
    def __init__(self, display_group, topleft_pos, surface_image, z=overlay_layers['menu_items'], offset=(0,0), relative_rect=None):
        super().__init__(display_group)
        self.timers = {}
        self.image:Surface = surface_image
        if relative_rect:
            self.rect = self.image.get_rect(top=relative_rect.top+offset[1], left=relative_rect.left+offset[0])
        else:
            self.rect = self.image.get_rect(topleft=topleft_pos)
        self.z = z

    def update(self, dt) -> None:
        super().update()
        
class Textbox(pygame.sprite.Sprite):
    def __init__(self, reference_sprite:pygame.sprite.Sprite, fontsize = 12, z = overlay_layers['text'], offset=(0,0), text='', position='center'):
        """
    Display text on screen.

    Args:
        reference_sprite(pygame.sprite.Sprite): The sprite that is used as a reference for placement and parent functions
        fontsize(int): Size of the text to display
        z(int): the layer of the screen that the sprite will be displayed to. 
        offset(tuple[int,int]): X and Y coords to adjust the position of the textbox relative to the position argument and reference sprite
        position(str): References offset and reference rect.
            relative:
            center:
            topmiddle:
            bottommiddle:
            middleright:
            middleleft:
    """
        super().__init__(overlay_sprites)
        self.master=reference_sprite
        self.reference_rect = reference_sprite.rect
        self.fontsize = fontsize
        self.text = text
        self.color = 'black'
        self.z = z
        self.is_active = False
        self.position = position
        self.offset = offset
        self._text_setup()
        self.set_position()
        overlay_sprites.remove(self)

    def _text_setup(self):
        self.font = pygame.font.Font('C:\Windows\Fonts\\vgafix.fon', self.fontsize)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect()

    def set_position(self) -> None:
        padding = 5
        if self.position == 'relative':
            self.rect.x = self.reference_rect.x + self.offset[0]
            self.rect.y = self.reference_rect.y + self.offset[1]
        else:
            if self.position == 'center':
                self.rect.centerx = self.reference_rect.centerx
                self.rect.centery = self.reference_rect.centery
            elif self.position == 'topmiddle':
                self.rect.centerx = self.reference_rect.centerx
                self.rect.top = self.reference_rect.top + padding
            elif self.position == 'bottommiddle':
                self.rect.centerx = self.reference_rect.centerx
                self.rect.bottom = self.reference_rect.bottom - padding
            elif self.position == 'middleright':
                self.rect.right = self.reference_rect.right - padding
                self.rect.centery = self.reference_rect.centery
            elif self.position == 'middleleft':
                self.rect.left = self.reference_rect.left + padding
                self.rect.centery = self.reference_rect.centery

            self.rect.centerx += self.offset[0]
            self.rect.centery += self.offset[1]

    def update(self, dt):
        if self.master not in overlay_sprites:
            overlay_sprites.remove(self)
        self.image = self.font.render(self.text.title(), True, self.color)

class DialogBox(pygame.sprite.Sprite):
    def __init__(self, owner:pygame.sprite.Sprite, font_size=12, font_color='black'):
        super().__init__(overlay_sprites)
        self.master = owner
        self.fontsize = font_size
        self.screen_offset=(27,400)
        self.z = overlay_layers['menu']
        self.dialoge:str = ''
        self.text = ''
        self.image = pygame.image.load('assets\images\HUD\dialog_box.png')
        self.rect = self.image.get_rect(topleft=self.screen_offset)
        self.text_box = Textbox(self, font_size, offset=(100,0), position='middleleft')
        self.display_items = [self, self.text_box]
        overlay_sprites.remove(self.display_items)
        self.is_active = False

    def setup_display_items(self, speaking_crew:Sprite) -> None:
        #initialize textbox, subject image, and relative display items
        self.is_active = True
        self.text = f'{speaking_crew.name}: {self.dialoge}'
        self.dialoge_identifier = self.text[-1]
        self.subject_box=Generic(overlay_sprites
                                 ,(0,0)
                                 ,self.master.sprite.image
                                 ,z=overlay_layers['menu_elements']
                                 ,offset=(20,20)
                                 ,relative_rect=self.rect)
        self.speaker_icon = Generic(overlay_sprites
                                    ,(0,0)
                                    ,speaking_crew.image
                                    ,z=overlay_layers['text']
                                    ,offset=(95,10)
                                    ,relative_rect=self.rect)
        self.display_items.append(self.speaker_icon)
        self.display_items.append(self.subject_box)
        overlay_sprites.add(self.display_items)

        #dialoging setup
        self.ready_to_continue = False
        self._text_scroll_direction = 0
        self.text_on_screen_index = 0
        self.shown_characters = []
        self.dialoge_end = False

    def update(self, dt):
        pass 

    def process_text(self, dt):
        EVENT_HANDLER.run(self.dialoge_input) 
        state = self._check_state()
        if state == 'normal':
            self._end_dialoge()
            return state
        
        for character in range(len(self.text)-40):
            self.shown_characters.append(self.text[character:character+40])
        self._animate_text(dt)      

    def _animate_text(self, dt):
        if self.text_on_screen_index > len(self.shown_characters) -1:
            self.text_on_screen_index = len(self.shown_characters) -1  #cap index at max length of string
            self.dialoge_end = True

        elif self.text_on_screen_index < 0: #cap min value of index at 0
            self.text_on_screen_index = 0

        else:  #allow text scrolling between 0 and max index value
            self.text_on_screen_index += self._text_scroll_direction * dt * TEXT_SPEED

        self.text = self.shown_characters[int(self.text_on_screen_index)]
        self.text_box.text = self.text
        
    def _end_dialoge(self):
        self.is_active = False
        overlay_sprites.remove(self.display_items)
        self.display_items = [self, self.text_box]

    def _check_state(self) -> str:
        if self.ready_to_continue == True:
            return 'normal'
        else:
            if self.dialoge_identifier == '*':
                return 'nemu'
            elif self.dialoge_identifier == '%':
                return 'yes/no'
            elif self.dialoge_identifier == '&':
                return 'dialoge'

    def dialoge_input(self, keys, mouse_pos, dt) -> None:
        self._text_scroll_direction = 0
        if keys[pygame.K_d]:
            self._text_scroll_direction = 1
        elif keys[pygame.K_a]:
            self._text_scroll_direction = -1
        
        if keys[pygame.K_ESCAPE] or (keys[pygame.K_RETURN] and self.dialoge_end):
            self.ready_to_continue = True

