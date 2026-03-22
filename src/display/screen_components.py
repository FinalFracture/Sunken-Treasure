import pygame
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.rect import Rect
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites

class Overlay(Sprite):
    def __init__(self, owner):
        super().__init__(overlay_sprites)
        self.master = owner
        self.image = pygame.image.load('assets/images/hud/heads_up.png').convert_alpha()
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH/2, bottom=SCREEN_HEIGHT)
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
        self.gold.set_text(str(self.master.gold))
        self.bearing.set_text(str(self.master.gps_coord))
        self.storage.set_text(self.master.get_inv_level())
        self.knots.set_text(str(self.master.knotical_speed))
    

    def position_crew_icons(self, crew_list):
        for member_number, member_role in enumerate(crew_list):
            self.crew_list[member_number] = member_role
        for crew_index, crew_icon in self.crew_list.items():
            overlay_sprites.add(crew_icon)
            crew_icon.rect.topleft = self.crew_icon_topleft_positions[f'crew_member_{crew_index+1}']

class ItemStatBox(Sprite):
    #the sprite to display an items value, description, weight, and other values
    #while the inventory menu is active
    def __init__(self, relative_rect: pygame.rect.Rect, offset: tuple, z=overlay_layers['menu_aux']):    
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets/images/HUD/item_stat_textbox.png')
        self.rect = self.image.get_rect(topleft = (relative_rect.x + offset[0], relative_rect.y + offset[1]))
        self.item_name_display = HoverMessage(self, offset = (10, 5), fontsize=12)
        self.item_value_display = HoverMessage(self, offset = (10,20), fontsize=12)
        self.item_description_line1 = HoverMessage(self, offset = (10,35), fontsize=12)
        self.item_description_line2 = HoverMessage(self, offset = (10,50), fontsize=12)
        self.z = z
        self.ui_elements = [self.item_name_display, self.item_value_display, self.item_description_line1, self.item_description_line2]

class UiButton(Sprite):
    def __init__(self, button_text:str, button_func:callable, func_arg, refrence_rect:pygame.Rect, topleft_offset:tuple[int,int], z=overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.name = button_text
        self.image = self._image_setup()
        self.rect = self.image.get_rect(topleft = (refrence_rect.x + topleft_offset[0], refrence_rect.y + topleft_offset[1]))
        self.z = z
        self.function = button_func
        self.arg = func_arg
        self.textboxes = [Textbox(self, text=button_text, max_rect=refrence_rect)]

    def update(self, dt) -> None:
        self._update_textboxes()
 
    def _update_textboxes(self) -> None:
        if (self in overlay_sprites) and (self.textboxes not in overlay_sprites):
            overlay_sprites.add(self.textboxes)

    def position(self, reference_rect:pygame.Rect, offset:tuple[int,int]) -> None:
        self.rect.x = reference_rect.x + offset[0]
        self.rect.y = reference_rect.y + offset[1]

    def _image_setup(self) -> pygame.Surface:
        image_path = 'assets/images/HUD/sidebar.png'
        image = pygame.image.load(image_path)
        return image

    def click(self) -> None:
        self.function(self.arg)

class IconBG(Sprite):
    def __init__(self, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets/images/HUD/icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator:bool = None
        self.value_display = Textbox(self, max_rect=self.rect, fontsize= 8, z=overlay_layers['text'])
        self.indicator:MenuIndicator = MenuIndicator(self.rect)
        overlay_sprites.remove(self.indicator)

    def update(self, dt): 
        if self.subject:
            self.subject.sprite.rect.center = self.rect.center
            self.value_display.set_text(str(self.subject.value))
            self.value_display.rect.center = (self.rect.x, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.set_text('')
    
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

class UpgradeIconBg(Sprite):
    def __init__(self, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(overlay_sprites)
        self.image = pygame.image.load('assets/images/HUD/upgrade_icon_bg.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.subject = subject
        self.z = z
        self.indicator = None
        self.selected = False 
        self.value_display = Textbox(self, fontsize= 8, z=overlay_layers['text'])

    def update(self, dt): 
        if self.subject:
            self.subject.rect.center = self.rect.center
            self.value_display.set_text(str(self.subject.value))
            self.value_display.rect.center = (self.rect.x-5, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.set_text('')
            
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

class MenuIndicator(Sprite):
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

class HoverMessage(Sprite):
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
        self.font = pygame.font.Font('assets//fonts//standard.ttf', self.fontsize)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect(topleft = (self.relative_surface.x + self.offset.x, self.relative_surface.y + self.offset.y))

    def update(self, dt):
        self.process_text()

    def process_text(self):
        #to be called by other classes when they need to modify this classes text
        self.image = self.font.render(self.text, False, self.color)
 
class Generic(Sprite):
    def __init__(self, display_group, surface_image, z=overlay_layers['menu_items'], offset=(0,0), topleft_pos:tuple[int, int]=(0,0), relative_rect:pygame.rect.Rect|None=None):
        super().__init__(display_group)
        self.timers = {}
        self.image:Surface = surface_image
        self.relative_rect = relative_rect
        self.offset = offset
        self.topleft_pos = topleft_pos
        self.z = z
        if self.relative_rect:
                self.rect = self.image.get_rect(top=self.relative_rect.top+self.offset[1], 
                                                left=self.relative_rect.left+self.offset[0])
        else:
            self.rect = self.image.get_rect(topleft=self.topleft_pos)

    def set_position(self) -> None:
        if self.relative_rect:
                self.rect = self.image.get_rect(top=self.relative_rect.top+self.offset[1], 
                                                left=self.relative_rect.left+self.offset[0])
        else:
            self.rect = self.image.get_rect(topleft=self.topleft_pos)

    def update(self, dt) -> None:
        super().update()
        
class Textbox(Sprite):
    def __init__(self, reference_sprite:Sprite, max_rect:Rect, fontsize=12, z = overlay_layers['text'], offset=(0,0), text='', position='center'):
        """
    Display text on screen.

    **Parameters**
    --------------------
    - reference_sprite(Sprite): 
        The sprite that is used as a reference for placement and parent functions
    - fontsize(int): 
        Size of the text to display
    - z(int): 
        the layer of the screen that the sprite will be displayed to. 
    - offset(tuple[int,int]): 
        X and Y coords to adjust the position of the textbox relative to the position argument and reference sprite
    - position(str): 
        - relative: Places top left of Textbox at position(offset) within the reference_sprite rect
        - center: Place the Textbox centered within the reference_sprite rect
        - topmiddle
        - bottommiddle
        - middleright
        - middleleft
    """
        super().__init__(overlay_sprites)
        self.master=reference_sprite
        self.reference_rect = reference_sprite.rect
        self.fontsize = fontsize
        self.text = text
        self.color = 'black'
        self.z = z
        self.max_rect = max_rect
        self.position = position
        self.offset = offset
        self._text_setup()
        self.set_position()
        self.kill()


    def _text_setup(self):
        self.font = pygame.font.Font('assets/fonts/standard.ttf', self.fontsize)
        self.image = self.font.render(self.text, False, (0,0,0,0))
        self.rect = self.image.get_rect()
        self._resize()
        
    def set_text(self, text:str) -> None:
        self.text = text
        self.image = self.font.render(self.text.title(), True, self.color)
        self.rect = self.image.get_rect()
        self._resize()

    def _resize(self) -> None:
        width_ratio = self.max_rect.width / (self.rect.width + 1)
        height_ratio = self.max_rect.height / (self.rect.height + 1)
        self.image = pygame.transform.scale_by(self.image, (width_ratio, height_ratio))

    def set_position(self) -> None:
        print(self)
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
            self.kill()

class CrewQuartersHUD(Sprite):
    """A class to create and manage the UI for displaying crew on the HUD and in game menus
    
    """
    
    def __init__(self) -> None:
        super().__init__(overlay_sprites)
        image_path:str = 'assets/images/hud/crew_quarters/crew_quarters_hud.png'
        self.image:Surface = pygame.image.load(image_path)
        self.rect = self.image.get_rect(left=0, bottom=640)
        self.z = overlay_layers['hud']
        self.max_crew:int = 18
        self.current_crew_slots:list[CrewUiSlot] = []
        self.crew_slot_positions:dict[int, tuple[int,int]] = {}
        self._set_crew_slot_positions()
    
    def _set_crew_slot_positions(self) -> None:
        x_padding = 4
        x_spacing= 8
        y_padding = 4
        y_spacing = 4
        slot_rows = 2
        slot_columns = 9
        slot_width = 36
        slot_height = 52
        slot_index = 0
        for y in range(slot_rows):
            top_y_coord = ((y_spacing + slot_height) * y) + y_padding + self.rect.top
            for x in range(slot_columns):
                left_x_coord = ((x_spacing + slot_width) * x) + x_padding + self.rect.left
                coord_pair = (left_x_coord, top_y_coord)
                slot_index += 1
                self.crew_slot_positions[slot_index] = coord_pair

    def _position_crew_slots(self) -> None:
        for slot_index, slot in enumerate(self.current_crew_slots):
            slot.rect.topleft = self.crew_slot_positions[slot_index+1]

    def _create_crew_space(self) -> None:
        """Create an empty spot in UI for a crew member
        
        """
        if len(self.current_crew_slots) < self.max_crew:
            new_slot:CrewUiSlot = CrewUiSlot()
            self.current_crew_slots.append(new_slot)
        else:
            raise IndexError

    def populate(self, crew_list:list) -> None:
        self.current_crew_slots = [] # clear the list
        for index, crew in enumerate(crew_list):
            try:
                self._create_crew_space()
                self.current_crew_slots[index].fill_slot(crew)
                
            except IndexError as ie:
                print("Crew Quarters is full")
        self._position_crew_slots()

class CrewUiSlot(Sprite):
    def __init__(self) -> None:
        super().__init__(overlay_sprites)
        image_path = 'assets/images/hud/crew_quarters/crew_space.png'
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.z = overlay_layers['hud_elements']
        self.crew_icon_top_pixel = 0
        self.crew_icon_left_pixel = 0
        self.crew_title_top_pixel = 0
        self.crew_title_left_pixel = 0
        self.crew_title_textbox:Textbox = Textbox(self, 
        max_rect=Rect(0,0,32,16),
        fontsize=9, 
        offset=(self.crew_title_left_pixel, self.crew_title_top_pixel), 
                                                  position='relative')
        self.place_holder_textbox_text = "EMPTY"
        self.crew_title_textbox.set_text(self.place_holder_textbox_text)
        overlay_sprites.add(self.crew_title_textbox)
        self.place_holder_crew_sprite:Surface = Surface((32,32))
        self.place_holder_crew_sprite.fill('lightgray')
        self.crew_image_sprite:Generic = Generic(overlay_sprites,
                                                 self.place_holder_crew_sprite, 
                                                 offset=(self.crew_icon_left_pixel, self.crew_icon_top_pixel),
                                                 relative_rect=self.rect)

    def update(self, *args, **kwargs):
        if  not self.rect.colliderect(self.crew_image_sprite.rect):
            self.crew_icon_top_pixel = 17 + self.rect.top 
            self.crew_icon_left_pixel = 1 + self.rect.left 
            self.crew_title_top_pixel = 2 + self.rect.top 
            self.crew_title_left_pixel = 2 + self.rect.left
            self.crew_image_sprite.rect.top = self.crew_icon_top_pixel
            self.crew_image_sprite.rect.left = self.crew_icon_left_pixel
            self.crew_title_textbox.rect.top = self.crew_title_top_pixel
            self.crew_title_textbox.rect.left = self.crew_title_left_pixel
        return super().update(*args, **kwargs)
    
    def fill_slot(self, crew_member) -> None:
        self.crew_image_sprite.kill()
        self.crew_image_sprite = crew_member.sprite
        overlay_sprites.add(crew_member.sprite)
        self.crew_image_sprite.rect.top = self.crew_icon_top_pixel
        self.crew_image_sprite.rect.left = self.crew_icon_left_pixel
        self.crew_title_textbox.set_text(crew_member.role)
