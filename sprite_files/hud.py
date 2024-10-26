import pygame
from math import ceil, floor
from SETTINGS import *

class Overlay(pygame.sprite.Sprite):
    def __init__(self, group, owner):
        super().__init__(group)
        self.group = group
        self.owner = owner
        self.image = pygame.image.load('images/hud/heads_up.png').convert_alpha()
        self.rect = self.image.get_rect(centerx=screen_width/2, bottom=screen_height)
        self.z = overlay_layers['hud']
        self.gold = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(135, 10), position='relative')
        self.bearing = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(395, 35), position='relative')
        self.storage = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(135, 50), position='relative')
        self.knots = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(280, 35), position='relative')
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
        if self in self.group and (self.textboxes not in self.group):
            self.group.add(self.textboxes)
        self.gold.text = str(self.owner.gold)
        self.bearing.text = (str(self.owner.gps_coord))
        self.storage.text = str(len(self.owner.inventory))
        self.knots.text = str(self.owner.knotical_speed)
    

    def position_crew_icons(self, crew_list):
        for member_number, member_role in enumerate(crew_list):
            self.crew_list[member_number] = member_role
        for crew_index, crew_icon in self.crew_list.items():
            crew_icon.group.add(crew_icon)
            crew_icon.rect.topleft = self.crew_icon_topleft_positions[f'crew_member_{crew_index+1}']
            crew_icon.z = overlay_layers['hud_elements']

class ItemStatBox(pygame.sprite.Sprite):
    #the sprite to display an items value, description, weight, and other values
    #while the inventory menu is active
    def __init__(self, display_group: pygame.sprite.Group, relative_rect: pygame.rect.Rect, offset: tuple, z=overlay_layers['menu_aux']):    
        super().__init__(display_group)
        self.image = pygame.image.load('images/HUD/item_stat_textbox.png')
        self.rect = self.image.get_rect(topleft = (relative_rect.x + offset[0], relative_rect.y + offset[1]))
        self.item_name_display = HoverMessage(display_group, self, offset = (10, 5), fontsize=12)
        self.item_value_display = HoverMessage(display_group, self, offset = (10,20), fontsize=12)
        self.item_description_line1 = HoverMessage(display_group, self, offset = (10,35), fontsize=12)
        self.item_description_line2 = HoverMessage(display_group, self, offset = (10,50), fontsize=12)
        self.z = z
        self.ui_elements = [self.item_name_display, self.item_value_display, self.item_description_line1, self.item_description_line2]

class UiButton(pygame.sprite.Sprite):
    def __init__(self, display_group:pygame.sprite.Group, button_text:str, button_func:callable, refrence_rect:pygame.Rect, topleft_offset:tuple[int,int], z=overlay_layers['menu_elements']):
        super().__init__(display_group)
        self.group = display_group
        self.name = button_text
        self.image = self._image_setup()
        self.rect = self.image.get_rect(topleft = (refrence_rect.x + topleft_offset[0], refrence_rect.y + topleft_offset[1]))
        self.z = z
        self.function = button_func
        self.textboxes = [Textbox(display_group, self, text=button_text)]

    def update(self, dt) -> None:
        self._update_textboxes()
 
    def _update_textboxes(self) -> None:
        if (self in self.group) and (self.textboxes not in self.group):
            self.group.add(self.textboxes)

    def position(self, reference_rect:pygame.Rect, offset:tuple[int,int]) -> None:
        self.rect.x = reference_rect.x + offset[0]
        self.rect.y = reference_rect.y + offset[1]

    def _image_setup(self) -> pygame.Surface:
        image_path = 'images/HUD/sidebar.png'
        image = pygame.image.load(image_path)
        return image

    def click(self) -> None:
        self.function()

class Icon_bg(pygame.sprite.Sprite):
    def __init__(self, group, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(group)
        self.group = group
        self.image = pygame.image.load('images/HUD/icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator = None
        self.selected:bool = False 
        self.value_display = Textbox(group, self, fontsize= 8, z=overlay_layers['text'])

    def update(self, dt): 
        if self.subject:
            self.subject.rect.center = self.rect.center
            self.value_display.text=str(self.subject.value)
            self.value_display.rect.center = (self.rect.x, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.text=''
            
    def deselect(self):
        #this will be called any time we need the inventory item to be deselected by any process
        if self.indicator:
            self.indicator.kill()
        self.selected = False
    
    def click(self, toggle=None):
        #define what happens when the mouse clicks while in the rect boundary of an icon bg.
        if toggle == 0:
            self.deselect()
        elif toggle == 1:
            self.indicator = MenuIndicator(self.group, self.rect)
            self.selected = True
        else:
            if self.subject and not self.selected:
                self.indicator = MenuIndicator(self.group, self.rect)
                self.selected = True
            elif self.subject and self.selected:
                self.deselect()

class UpgradeIconBg(pygame.sprite.Sprite):
    def __init__(self, group, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(group)
        self.group = group
        self.image = pygame.image.load('images/HUD/upgrade_icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator = None
        self.selected = False 
        self.value_display = Textbox(group, self, fontsize= 8, z=overlay_layers['text'])

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
            self.indicator = MenuIndicator(self.group, self.rect)
            self.selected = True
        else:
            if self.subject and not self.selected:
                self.indicator = MenuIndicator(self.group, self.rect)
                self.selected = True
            if self.subject and self.selected:
                self.deselect()

class MenuIndicator(pygame.sprite.Sprite):
    """When the player selects items to purchase, this class highlights the selected item slots to 
    visually indicate what has been selected. This will also apply to any other menues where inventory
    slots are selected, and not immediately resolved."""
    def __init__(self, group, owning_rect, z = overlay_layers['menu_aux']):
        super().__init__(group)
        self.z = z
        self.image = pygame.Surface((owning_rect.width, owning_rect.height))
        self.rect = self.image.get_rect()
        self.rect.width = self.rect.width + 6
        self.rect.height = self.rect.height + 6
        self.rect.center = owning_rect.center
        self.image.fill(color='Green')

class HoverMessage(pygame.sprite.Sprite):
    """This class is a message that displays at its specified coords. it is uninteractable."""
    def __init__(self
                 ,group:pygame.sprite.Group
                 ,relative_surface:pygame.rect.Rect
                 ,fontsize = 20
                 ,z = overlay_layers['menu_elements']
                 ,offset = (0,0)
                 ,max_lines = 2 
                 ,color = 'black'):
        super().__init__(group)
        self.group = group
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
        self.font = pygame.font.Font('misc_files\standard.ttf', self.fontsize)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect(topleft = (self.relative_surface.x + self.offset.x, self.relative_surface.y + self.offset.y))

    def update(self, dt):
        self.process_text()

    def process_text(self):
        #to be called by other classes when they need to modify this classes text
        self.image = self.font.render(self.text, False, self.color)
 
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
    def __init__(self, group:pygame.sprite.Group, reference_sprite:pygame.sprite.Sprite, fontsize = 12, z = overlay_layers['text'], offset=(0,0), text='', position='center'):
        """
    Display text on screen.

    Args:
        group(Pygame.sprite.Group): The group that determines when the sprite will show on screen
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
        super().__init__(group)
        self.group = group
        self.owner=reference_sprite
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
        self.group.remove(self)

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
        if self.owner not in self.group:
            self.group.remove(self)
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
        self.text_box = Textbox(self.group, self, font_size, offset=(100,0), position='middleleft')
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

class Clipboard(pygame.sprite.Sprite):
    def __init__(self, group:pygame.sprite.Group, offset:tuple[int], owner:pygame.sprite.Sprite, z=overlay_layers['menu']) -> None:
        super().__init__(group)
        image_path = 'images/hud/clipboard.png'
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=offset)
        self.z = z
        self.owner = owner
        self.group = group
        self.display_objects = []
        self.buttons = []
        self.active_buttons:list[UiButton] = []
        self.make_button({'name':'Sort', 'func':self.owner.sort_inventory})

    def make_button(self, button_info:dict) -> None:
        button=UiButton(display_group=self.group, button_text=button_info['name'], button_func=button_info['func'], refrence_rect=self.rect, topleft_offset=(0,0))
        self.display_objects.append(button)
        self.buttons.append(button)
        self.active_buttons.append(button)
        self.group.remove(button)

    def update_buttons(self) -> None:
        def _set_position(index:int) -> tuple[int]:
            side_padding = 25
            top_padding = 25
            height = 35
            width = 60
            max_cols = 2
            if index % max_cols == 0:
                left = side_padding
            elif index % max_cols == 1:
                left = width + side_padding * max_cols

            row = floor(index/max_cols)
            top = self.rect.top + top_padding + ((top_padding + height) * row)

            return(left,top)
        
        for button in self.active_buttons:
            if button not in self.buttons:
                self.buttons.append(button)

        for button in self.buttons:
            if button in self.active_buttons:
                offset = _set_position(self.active_buttons.index(button))
                button.position(reference_rect=self.rect, offset=offset)
                self.group.add(button)
                for textbox in button.textboxes:
                    textbox.set_position()
            else:
                self.group.remove(button)

    def show(self) -> None:
        for item in self.display_objects:
            self.group.add(item)

    def update(self, dt ) -> None:
        self._input()

    def _input(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            for button in self.active_buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.click()

    def exit(self) -> None:
        for item in self.display_objects:
            self.group.remove(item)
