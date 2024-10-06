import pygame
from sprite_files.sprites import Textbox
from SETTINGS import *


class Overlay(pygame.sprite.Sprite):
    def __init__(self, group, owner):
        super().__init__(group)
        self.group = group
        self.owner = owner
        self.image = pygame.image.load('images/hud/heads_up.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (0, 425))
        self.z = overlay_layers['hud']
        self.gold = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(135, 10))
        self.bearing = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(395, 35))
        self.storage = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(132, 50))
        self.knots = Textbox(self.group, self, z=overlay_layers['hud_elements'], offset=(280, 35))
        self.crew_icon_topleft_positions ={'crew_member_1': (self.rect.x + 16, self.rect.y+30)
                                            ,'crew_member_2': (self.rect.x+40,self.rect.y+30)
                                            ,'crew_member_3': (self.rect.x+65,self.rect.y+30)
                                            ,'crew_member_4': (self.rect.x+16,self.rect.y+54)
                                            ,'crew_member_5': (self.rect.x+40,self.rect.y+54)
                                            ,'crew_member_6': (self.rect.x+65,self.rect.y+54)
                                            }
        self.crew_list = {}

    def update(self, dt):
        self.gold.text = str(self.owner.gold)
        self.bearing.text = (str(self.owner.gps_coord))
        self.storage.text = str(len(self.owner.inventory))
        self.knots.text = str(self.owner.knotical_speed)

    def position_crew_icons(self, crew_list):
        for member_number, member_role in enumerate(crew_list):
            self.crew_list[member_number] = member_role
        for crew_index, crew_icon in self.crew_list.items():
            crew_icon.rect.topleft = self.crew_icon_topleft_positions[f'crew_member_{crew_index+1}']

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
    def __init__(self, display_group, image, relative_surface_rect, position_on_relative_surface, z=overlay_layers['menu_elements']):
        super().__init__(display_group)
        self.group = display_group
        self.image = image
        self.rect = self.image.get_rect(topleft = (relative_surface_rect.x + position_on_relative_surface[0], relative_surface_rect.y + position_on_relative_surface[1]))
        self.z = z

class Icon_bg(pygame.sprite.Sprite):
    def __init__(self, group, subject = None, pos = (0,0), z = overlay_layers['menu_elements']):
        super().__init__(group)
        self.group = group
        self.image = pygame.image.load('images/HUD/icon_bg.png').convert_alpha()
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
            self.value_display.rect.center = (self.rect.x, self.rect.y)
        else:
            #remove the value display from the display group
            self.value_display.text=''
            

    def deselect(self):
        #this will be called any time we need the inventory item to be deselected by any process
        try:
            self.indicator.kill()
        except:
            pass
        finally:
            self.selected = False
    
    def click(self):
        #define what happens when the mouse clicks while in the rect boundary of an icon bg.
        if self.subject and self.selected:
            self.deselect()
        elif self.subject and not self.selected:
            self.indicator = MenuIndicator(self.group, self.rect)
            self.selected = True

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
        try:
            self.indicator.kill()
        except:
            pass
        finally:
            self.selected = False
    
    def click(self):
        #define what happens when the mouse clicks while in the rect boundary of an icon bg.
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
 