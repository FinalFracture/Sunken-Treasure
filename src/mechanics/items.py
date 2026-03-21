from pygame import sprite, Surface, Rect
from src.event_managing import EVENT_HANDLER
from src.utils.support import import_folder
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites

item_image_paths = 'assets/images/items/'

item_stats:dict[str:dict] = {
   'fish':{
        'tuna': {
        'image': []
        ,'value': 250
        ,'weight': 55
        ,'rarity': 'Rare' 
        ,'description1': 'A massive fish. Just'
        ,'description2': '1 can feed a village.'
    }
        ,'catfish': {
        'image': []
        ,'value': 35
        ,'weight': 5
        ,'rarity': 'uncommon'
        ,'description1': 'Large bottom feeding fish.' 
        ,'description2':'Easier to find while still.' 
    }
        ,'salmon': {
        'image': []
        ,'value': 23
        ,'weight': 3
        ,'rarity': 'common' 
        ,'description1': 'A treat to some groups.' 
        ,'description2':'Prefers colder climates.'
    }
        ,'carp': {
    'image': []
    ,'value': 5
    ,'weight': 8
    ,'rarity': 'common' 
    ,'description1':'Extremely common, carp ' 
    ,'description2':'are an invasive species.'
}
    }
    ,'minerals':{
        'slate': {
            'image': []
            ,'value': 4
            ,'weight': 8
            ,'rarity': 'Common' 
            ,'description1': 'Flat stone pieces.'
            ,'description2': 'Can contain fossils.'
        }
        ,'sandstone': {
            'image': []
            ,'value': 2
            ,'weight': 5
            ,'rarity': 'Common' 
            ,'description1': 'Coarse brittle rock.'
            ,'description2': 'Absorbs water well.'
    }
    }
}

def _import_game_item_assets() -> None:
   for type_name, item_type in item_stats.items():   
      if type_name != 'crew':
         for item_name,  gameitem in item_type.items():
            full_path = f'{item_image_paths}{type_name}/{item_name}'
            gameitem['image'] = import_folder(full_path)
    

class GameItem(sprite.Sprite):
    def __init__(self, item_type:str, item_name:str, z=cameragroup_layers['items']) -> None:
        super().__init__(overlay_sprites)
        self.item_name:str = item_name 
        self.item_type:str = item_type
        self.selected:bool = False
        self.stats:dict = item_stats[self.item_type][self.item_name].copy()
        self.name:str = item_name
        self.image:Surface = self.stats['image'][0]
        self.rect:Rect = self.image.get_rect()
        self.z:int = z
        overlay_sprites.remove(self)
        self.value = self.stats['value']
 