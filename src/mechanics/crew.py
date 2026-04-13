import random
from pygame.sprite import Sprite
from pygame.image import load
from src.utils.enumerations import CardID
from src.utils.settings import *
from src.utils.cameras import overlay_sprites, overlay_layers, cameragroup_layers
from src.story.vocabularies import *
from src.mechanics.tools import Tool, TOOL_MAP
from src.display.screen_components import HUDCard, CARD_MAP

image_paths:str = 'assets/images/crew/tool_'

first_names:list[str] = [
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

last_names:list[str] = [
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

used_names:list[str] = []

crew_roles:list[dict] = [
   {
        'role_name':'angler',
        'tool':'fishing_pole',
        'class':'fisher',
        'rarity':'Common',
        'hud_card': CardID.NULL,
        'description1': 'Use an array of rods',
        'description2': 'to catch many fish.'
    },
    {
        'role_name':'harpooner',
        'tool':'harpoon',
        'class':'fisher',
        'rarity':'Uncommon',
        'hud_card': CardID.NULL,
        'description1': 'Sharpshooting fishers.',
        'description2': 'Slow, but big catches.'
    },
    {
        'role_name':'netter',
        'tool':'fishing_net',
        'class':'fisher',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Netters can haul vast',
        'description2': 'quantities of sea life.'
    },
    {
        'role_name':'miner',
        'tool':'pickaxe',
        'class':'rockhound',
        'rarity':'Common',
        'hud_card': CardID.NULL,
        'description1': 'Miners pick away at',
        'description2': 'rocks to find ores.'
    },
    {
        'role_name':'powderman',
        'tool':'tnt',
        'class':'rockhound',
        'rarity':'Uncommon',
        'hud_card': CardID.NULL,
        'description1': 'Can blast apart stones',
        'description2': 'for numerous minerals.'
    },
    {
        'role_name':'quarrier',
        'tool':'stone_cutter',
        'class':'rockhound',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Delicately carve out',
        'description2': 'precious gemstones.'
    },
    {
        'role_name':'quartermaster',
        'tool':'clipboard',
        'class':'deckhand',
        'rarity':'Common',
        'hud_card': CardID.CARGO,
        'description1': 'Increase ship storage',
        'description2': 'capacity and effeciency.'
    },
    {
        'role_name':'helmsman',
        'tool':'oar',
        'class':'deckhand',
        'rarity':'Uncommon',
        'hud_card': CardID.SPEED,
        'description1': 'Experienced sailor who',
        'description2': 'makes travel faster.'
    },
    {
        'role_name':'carpenter',
        'tool':'mallet_and_saw',
        'class':'deckhand',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Upgrade and repair ',
        'description2': 'your vehicles.'
    },
    {
        'role_name':'cook',
        'tool':'cutlery',
        'class':'merchant',
        'rarity':'Uncommon',
        'hud_card': CardID.NULL,
        'description1': 'Keep the morale high',
        'description2': 'and crewmates happy.'
    },
    {
        'role_name':'trader',
        'tool':'scale',
        'class':'merchant',
        'rarity':'Common',
        'hud_card': CardID.COIN,
        'description1': 'Barter your way into',
        'description2': 'bargains and deals.'
    },
    {
        'role_name':'tailor',
        'tool':'needle_and_thread',
        'class':'merchant',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Make better sails or',
        'description2': 'dress crew to the nines.'
    },
    {
        'role_name':'scavenger',
        'tool':'sea_claw',
        'class':'artificer',
        'rarity':'Common',
        'hud_card': CardID.NULL,
        'description1': 'Reach into the depths',
        'description2': 'and bring up treasure.'
    },
    {
        'role_name':'curator',
        'tool':'seer_stone',
        'class':'artificer',
        'rarity':'Uncommon',
        'hud_card': CardID.NULL,
        'description1': 'Pick through salvage',
        'description2': 'and identify treasure.'
    },
    {
        'role_name':'explorer',
        'tool':'compass',
        'class':'artificer',
        'rarity':'Rare',
        'hud_card': CardID.BEARING,
        'description1': 'Effortlessley navigate',
        'description2': 'environmental phenomenon.',
        'note':"skills are precision and accuracy of read. + mods the precision ie 1 -> 1.000, mulltiply provides correction to read froma random number generator"
    },
    {
        'role_name':'distiller',
        'tool':'tap',
        'class':'islander',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Produce barrels of',
        'description2': 'valuable liquids.'
    },
    {
        'role_name':'farmer',
        'tool':'shovel_and_pail',
        'class':'islander',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Grow myriad of crops',
        'description2': 'for a variety of uses.'
    },
    {
        'role_name':'hunter',
        'tool':'spear',
        'class':'islander',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Hunt, slaughter, and',
        'description2': 'herd all the animals.'
    },
    {
        'role_name':'spy',
        'tool':'lockpick',
        'class':'operative',
        'rarity':'Rare',
        'hud_card': CardID.NULL,
        'description1': 'Steal shop items',
        'description2': 'and decieve crew.'
    },
    {
        'role_name':'cartographer',
        'tool':'map',
        'class':'operative',
        'rarity':'Common',
        'hud_card': CardID.NULL,
        'description1': 'Create and read maps.',
        'description2': "You'll never get lost."
    },
    {
        'role_name':'scholar',
        'tool':'book_and_quill',
        'class':'operative',
        'rarity':'Uncommon',
        'hud_card': CardID.NULL,
        'description1': 'Highly knowledgable,',
        'description2': 'improve other crew.'
    }
]

def generate_name() -> str:
    #this class will generate a name for crew members and ensure that only unique names are used.
   getting_name = True
   while getting_name:
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    full_name = f'{first_name.capitalize()} {last_name.capitalize()}'
    if full_name not in used_names:
      used_names.append(full_name)
      getting_name = False
      return(full_name)

class CrewSprite(Sprite):
    def __init__(self, tool_name:str, master) -> None:
       super().__init__(overlay_sprites)
       self.image = load(image_paths + tool_name + '.png').convert_alpha()
       self.rect = self.image.get_rect()
       self.z=overlay_layers['menu_items']
       self.master = master
       
    def update(self, *args, **kwargs) -> None:
       self.master.update()
       #lets make a group called an update group to avoid this up chain calling
       #children shoulnd't control parents

class Crew:
    def __init__(self, role_attrs:dict[str, str]):
        """
        A Crew will contain an tool used for finding items or performing in game mechanics based on its role.

        Parameters
        - sprite_group: Overlay camera Group

        - crew_role : str
            Name of the role that the class will perform. Determines what tools can be used.

        - owner: 
            Sprite sub-class such as an NPC or the player

        - z : int 
            Drawing layer
        """
        self.role_name:str = role_attrs.get('role_name')
        self.name = generate_name()
        self.tool:Tool = TOOL_MAP[role_attrs.get('tool')](self)
        self.class_type = role_attrs.get('class')
        self.rarity = role_attrs.get('rarity')
        self.hud_card_type:str = role_attrs.get('hud_card')
        self._setup_hud_card()
        self.description = [role_attrs.get('description1'), role_attrs.get('description2')]
        self.archetype = random.choice(list(archetype_vocabularies.keys()))
        self.sprite = CrewSprite(role_attrs.get('tool'), self)
        overlay_sprites.remove(self.sprite)
        self.master = None
        self.selected:bool = False
        self._init_skills()

    def _setup_hud_card(self) -> None:
        try:
            self.hud_card:HUDCard = CARD_MAP[self.hud_card_type]()
        except:
           pass
    
    def activate_hud_card(self) -> None:
       if self.hud_card:
           self.hud_card.activate()
    
    def deactivate_hud_card(self) -> None:
       if self.hud_card:
           self.hud_card.deactivate()

    def _init_skills(self) -> None:
        self.tool_use_rate:int = 0
        self.tool_effeciency_modifier:int = 0
        self.max_health:int = 50
        self.max_hydration:int = 50
        self.max_morale:int = 50
        self.health:int = self.max_health
        self.hydration:int = self.max_hydration
        self.morale:int = self.max_morale
        self.skills:list[int] = [
           self.tool_use_rate,
           self.tool_effeciency_modifier,
           self.max_health,
           self.max_hydration,
           self.max_morale
        ]

    def set_master(self, master) -> None:
       self.master = master

    def _select(self) -> None:
        self.selected = True

    def deselect(self) -> None:
       self.selected = False

    def update(self, *args, **kwargs) -> None:
       if self.selected:
          self.tool.use()

    def toggle_selected(self) -> None:
        if self.selected:
            self.deselect()
        else:
            self._select()

def build_crew_member(owner, role_name) -> Crew:
   for role in crew_roles:
      if role_name == role.get('role_name'):
        crew_member = Crew(role)
        crew_member.set_master(owner)
        return crew_member