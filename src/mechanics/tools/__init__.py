import random
import os
from pygame import sprite, Surface, Rect
from src.event_managing import EVENT_HANDLER
from src.utils.timer import Timer
from src.utils.support import import_folder
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, cameragroup_layers, overlay_layers, all_sprites
from src.overlays.screen_components import Generic

crew_image_paths = 'assets\images\crew/'
item_image_paths = 'assets\images\items/'

item_stats:dict[str:dict] = {'fish':{
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
            ,'crew':{
                    'angler': {
                        'name': ''
                        ,'value':'C'
                        ,'tool_modifier': 0
                        ,'tool': 'fishing_pole'
                        ,'rarity': 'Common' 
                        ,'description1': 'Anglers provide many'
                        ,'description2': 'options to catching fish.'
                        ,'selected':[]
                        ,'unselected':[]
                },
                    'rockhound': {
                        'name': ''
                        ,'value':'C'
                        ,'tool_modifier': 0
                        ,'tool': 'pickaxe'
                        ,'rarity': 'Common' 
                        ,'description1': 'Rockhounds specialize in'
                        ,'description2': 'finding rocks and gems.'
                        ,'selected':[]
                        ,'unselected':[]
                }
    }
}

USED_NAMES:list[str] = []

_FIRST_NAMES:list[str] = [
'Aaron',
'Adam',
'Aiden',
'Alan',
'Albert',
'Alex',
'Alexander',
'Andrew',
'Anthony',
'Arthur',
'Austin',
'Benjamin',
'Blake',
'Bradley',
'Brandon',
'Brian',
'Caleb',
'Calvin',
'Cameron',
'Carl',
'Carlos',
'Charles',
'Christian',
'Christopher',
'Cody',
'Colin',
'Conor',
'Craig',
'Damian',
'Daniel',
'David',
'Dean',
'Derek',
'Dominic',
'Dylan',
'Edward',
'Elijah',
'Elliot',
'Elon',
'Eric',
'Ethan',
'Evan',
'Felix',
'Finn',
'Francis',
'Frank',
'Gabriel',
'Gary',
'George',
'Graham',
'Grant',
'Gregory',
'Harry',
'Henry',
'Isaac',
'Jack',
'Jackson',
'Jacob',
'James',
'Jason',
'Jeffrey',
'Jeremy',
'Jesse',
'Joel',
'John',
'Jonathan',
'Jordan',
'Joseph',
'Joshua',
'Julian',
'Justin',
'Keith',
'Kevin',
'Kyle',
'Lance',
'Lawrence',
'Liam',
'Logan',
'Lucas',
'Luke',
'Marcus',
'Mark',
'Martin',
'Matthew',
'Max',
'Michael',
'Nathan',
'Nicholas',
'Noah',
'Oliver',
'Oscar',
'Owen',
'Patrick',
'Paul',
'Peter',
'Philip',
'Quentin',
'Raymond',
'Richard',
'Robert',
'Ryan',
'Samuel',
'Scott',
'Sean',
'Seth',
'Shane',
'Simon',
'Spencer',
'Stephen',
'Thomas',
'Timothy',
'Toby',
'Tony',
'Travis',
'Trevor',
'Tyler',
'Vincent',
'William',
'Zachary',
'Abigail',
'Alice',
'Amelia',
'Anna',
'Aria',
'Ava',
'Bella',
'Brianna',
'Camila',
'Charlotte',
'Chloe',
'Claire',
'Daisy',
'Elizabeth',
'Ella',
'Emily',
'Emma',
'Grace',
'Hannah',
'Harper',
'Isabella',
'Isla',
'Jasmine',
'Julia',
'Kaitlyn',
'Kayla',
'Leah',
'Lila',
'Lily',
'Lucy',
'Luna',
'Melody',
'Madelyn',
'Madison',
'Maya',
'Mia',
'Natalie',
'Olivia',
'Penelope',
'Rachel',
'Rylee',
'Riley',
'Rose',
'Samantha',
'Sarah',
'Scarlett',
'Sofia',
'Sophia',
'Sophie',
'Victoria',
'Valeria',
'Violet',
'Zoe'
]

_LAST_NAMES:list[str] = [
'Adams',
'Ahmed',
'Alvarez',
'Anderson',
'Bailey',
'Baker',
'Banerjee',
'Barnes',
'Bell',
'Bennett',
'Bhattacharya',
'Black',
'Brown',
'Burgess',
'Burns',
'Butler',
'Campbell',
'Chang',
'Chapman',
'Chen',
'Cheng',
'Chowdhury',
'Clark',
'Coleman',
'Collins',
'Cook',
'Cooper',
'Cox',
'Cruz',
'Das',
'Davies',
'Davis',
'Dean',
'Diaz',
'Dutta',
'Edwards',
'Evans',
'Fernandez',
'Fisher',
'Foster',
'Fowler',
'Fox',
'Garcia',
'Ghosh',
'Gibson',
'Gomez',
'Gonzalez',
'Gordon',
'Graham',
'Grant',
'Green',
'Gupta',
'Gutierrez',
'Hall',
'Hamilton',
'Hansen',
'Harris',
'Harrison',
'Hart',
'Hernandez',
'Hill',
'Hopkins',
'Hossain',
'Howard',
'Hughes',
'Hunter',
'Iqbal',
'Islam',
'Jackson',
'James',
'Jenkins',
'Jensen',
'Johnson',
'Jones',
'Kapoor',
'Kelly',
'Kennedy',
'Khan',
'Kim',
'King',
'Kumar',
'Kwon',
'Lee',
'Leung',
'Lewis',
'Li',
'Liang',
'Liu',
'Long',
'Lopez',
'Ma',
'Malik',
'Marshall',
'Martin',
'Martinez',
'Mason',
'Mathur',
'Matthews',
'Meyer',
'Miller',
'Mitchell',
'Mohamed',
'Moore',
'Morgan',
'Morris',
'Mukherjee',
'Murphy',
'Murray',
'Musk',
'Nagy',
'Nakamura',
'Nelson',
'Ng',
'Nguyen',
'Nishi',
'Obrien',
'Oconnor',
'Olson',
'Ortiz',
'Owen',
'Pal',
'Pandey',
'Park',
'Patel',
'Perez',
'Perry',
'Phillips',
'Powell',
'Price',
'Rahman',
'Raj',
'Ramos',
'Reed',
'Reyes',
'Reynolds',
'Richardson',
'Rivera',
'Roberts',
'Robinson',
'Rodriguez',
'Rogers',
'Ross',
'Russell',
'Sanchez',
'Sanders',
'Sarkar',
'Schmidt',
'Schneider',
'Scott',
'Shah',
'Shankar',
'Shaw',
'Shelby',
'Shen',
'Sherman',
'Singh',
'Smith',
'Snyder',
'Stark',
'Stevens',
'Stewart',
'Stone',
'Sullivan',
'Suzuki',
'Tan',
'Taylor',
'Thakur',
'Thomas',
'Thompson',
'Torres',
'Tran',
'Turner',
'Vega',
'Wagner',
'Walker',
'Wallace',
'Wang',
'Ward',
'Washington',
'Watson',
'Weber',
'West',
'White',
'Williams',
'Wilson',
'Wong',
'Wood',
'Wright',
'Wu',
'Xu',
'Yamamoto',
'Yang',
'Yi',
'Young',
'Zhang',
'Zhou',
'Zhu'
]

_STATUSES:list[str] = ['selected', 'unselected']

def generate_name() -> str:
    #this class will generate a name for crew members and ensure that only unique names are used.
   getting_name = True
   while getting_name:
    first_name = random.choice(_FIRST_NAMES)
    last_name = random.choice(_LAST_NAMES)
    full_name = f'{first_name.capitalize()} {last_name.capitalize()}'
    if full_name not in USED_NAMES:
      USED_NAMES.append(full_name)
      getting_name = False
      return(full_name)

def generate_tool_modifier():
  bottom_of_range = .05
  top_of_range = .25
  generated_number = random.random()
  adjusted_number = bottom_of_range + generated_number * (top_of_range - bottom_of_range)
  return adjusted_number

def _import_crew_assets():
  for role, crew_stat_dict in item_stats['crew'].items():
    for status in _STATUSES:
      full_path = crew_image_paths + role +'/' + status
      crew_stat_dict[status] = import_folder(full_path)

def _import_game_item_assets() -> None:
   for type_name, item_type in item_stats.items():   
      if type_name != 'crew':
         for item_name,  gameitem in item_type.items():
            full_path = f'{item_image_paths}{type_name}/{item_name}'
            gameitem['image'] = import_folder(full_path)
    
def items_init():
  _import_crew_assets()
  _import_game_item_assets()

class Tool:
    def __init__(self, master, crew):
        self.base_find_rate = 0.1
        self.master = master
        self.crew = crew
        self.find_rate_modifiers = {}
        self.frame_counter = 0 # used to attempt a fish find every few seconds
        self.timers = {}# {'using':Timer(3000, ending_func = None)}

    def retrieve(self, caught_item):
        find_accepted:bool = self.master.add_to_inventory(caught_item) # bool to determine if there is inv space

        if find_accepted == True:
            current_find = Generic(all_sprites, caught_item.image, z = cameragroup_layers['items'], topleft_pos=self.master.sprite.status_rect.center)
        
            def _move_up(dt):
                current_find.rect.y -= 75 * EVENT_HANDLER.dt
                
            current_find.timers = {current_find:Timer(1250, running_func=_move_up, ending_func=current_find.kill)}
            current_find.timers[current_find].activate()

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
            
__all__=['item_stats'
        ,'Tool'
        ,'GameItem'
        ,'items_init'
        ,'generate_tool_modifier'
        ,'generate_name']