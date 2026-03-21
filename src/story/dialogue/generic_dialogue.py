import random
from src.mechanics.crew import Crew, role_vocabularies, archetype_vocabularies

## ---------- Insertion characters ---------------##
# @ = insert a crew name
# # = insert a quantity
# ^ = insert a location name
# $ = insert an item name
# = = insert time of day
# ~ = insert subject phrase
## -----------------------------------------------##


## ---------- End of string indicators -----------##
# * = EOS will open a menu
# % = EOS will invoke a yes/no prompt
## -----------------------------------------------##

general_dialog_trees = {
    'shop': {
        'new':{
            'initiate':[
                [
                    'Hello, can I interest you in any of my goods?',
                    "Yes, lets look at what you have for sale.*",
                    "Travel safe, come back again sometime."],
                [
                    "You there, come see my goods!",
                    "OK. . . *that was abrupt**",
                    "Thanks, now off with you. I have other customers waiting!&"    
                ]
            ],
            'respond':[
                [
                    "Hello, we are new in the area. Do you have goods for sale?",
                    "Hello! Always glad to see a new face in the area. Yes, look at my goods.*"
                    "We'll come by again if we need other goods."
                ],
                [
                    "Good =. *cough cough* Do you have anything for allergies? I'm not used to the air here.",
                    "Not sure about allergies, but you can take a look at my goods. . . *",
                    "Well, i'll keep looking just in case."
                ]
            ]
        },

        'acquaintance':{
            'initiate':[
                [
                    'Hello, can I interest you in any of my goods?',
                    "Yes, lets look at what you have for sale.*",
                    "Travel safe, come back again sometime."],
                [
                    "You there, come see my goods!",
                    "OK. . . *that was abrupt**",
                    "Thanks, now off with you. I have other customers waiting!"    
                ]
            ],
            'respond':[
                [
                    "Hello, we are new in the area. Do you have goods for sale?",
                    "Hello! Always glad to see a new face in the area. Yes, look at my goods.*"
                    "We'll come by again if we need other goods."
                ],
                [
                    "Good =. *cough cough* Do you have anything for allergies? I'm not used to the air here.",
                    "Not sure about allergies, but you can take a look at my goods. . . *",
                    "Well, i'll keep looking just in case."
                ]
            ]
        },

        'familiar':{
            'initiate':[
                [
                    'Hello, can I interest you in any of my goods?',
                    "Yes, lets look at what you have for sale.*",
                    "Travel safe, come back again sometime."],
                [
                    "You there, come see my goods!",
                    "OK. . . *that was abrupt**",
                    "Thanks, now off with you. I have other customers waiting!"    
                ]
            ],
            'respond':[
                [
                    "Hello, we are new in the area. Do you have goods for sale?",
                    "Hello! Always glad to see a new face in the area. Yes, look at my goods.*"
                    "We'll come by again if we need other goods."
                ],
                [
                    "Good =. *cough cough* Do you have anything for allergies? I'm not used to the air here.",
                    "Not sure about allergies, but you can take a look at my goods. . . *",
                    "Well, i'll keep looking just in case."
                ]
            ]
        },

        'trusted':{
            'initiate':[
                [
                    'Hello, can I interest you in any of my goods?',
                    "Yes, lets look at what you have for sale.*",
                    "Travel safe, come back again sometime."],
                [
                    "You there, come see my goods!",
                    "OK. . . *that was abrupt**",
                    "Thanks, now off with you. I have other customers waiting!"    
                ]
            ],
            'respond':[
                [
                    "Hello, we are new in the area. Do you have goods for sale?",
                    "Hello! Always glad to see a new face in the area. Yes, look at my goods.*"
                    "We'll come by again if we need other goods."
                ],
                [
                    "Good =. *cough cough* Do you have anything for allergies? I'm not used to the air here.",
                    "Not sure about allergies, but you can take a look at my goods. . . *",
                    "Well, i'll keep looking just in case."
                ]
            ]
        },

        'revered':{
            'initiate':[
                [
                    'Hello, can I interest you in any of my goods?',
                    "Yes, lets look at what you have for sale.*",
                    "Travel safe, come back again sometime."],
                [
                    "You there, come see my goods!",
                    "OK. . . *that was abrupt**",
                    "Thanks, now off with you. I have other customers waiting!"    
                ]
            ],
            'respond':[
                [
                    "Hello, we are new in the area. Do you have goods for sale?",
                    "Hello! Always glad to see a new face in the area. Yes, look at my goods.*"
                    "We'll come by again if we need other goods."
                ],
                [
                    "Good =. *cough cough* Do you have anything for allergies? I'm not used to the air here.",
                    "Not sure about allergies, but you can take a look at my goods. . . *",
                    "Well, i'll keep looking just in case."
                ]
            ]
        }
    },

    'generic': {
        'new':{
            'initiate':[
                [
                    "Hey, are you new here? This place doesn't usually take kindly to strangers.",
                    "We are. Thanks for the advice, we will tread carefully."
                ],
                [
                    "The last newcomers who passed through here didn't stay long.",
                    "What happened? Were there hostilities?",
                    "The Ephatrix deal in secret. All we know is, one of the crew members were found dead in the water. The next day, the ship and her crew were gone."   
                ]
            ],
            'respond':[
                [
                    "Hello, we arrived here by mistake. Where are we?",
                    "Bad luck I suppose. You've wandered into ^, known for ~.",
                    ". . . They still do that?"
                ],
                [
                    "Excuse me, can you direct me to the nearest island?",
                    "The island of Epithets lies far to the north, beware the icebergs.",
                    "I said nearest. . .",
                    "Sorry, I was programmed with flavor dialogue. . ."
                ]
            ]
        },

        'acquaintance':{
            'initiate':[
                [
                    "Hey, are you new here? This place doesn't usually take kindly to strangers.",
                    "We are. Thanks for the advice, we will tread carefully."
                ],
                [
                    "The last newcomers who passed through here didn't stay long",
                    "What happened? Were there hostilities?",
                    "The Ephatrix deal in secret. All we know is, one of the crew members were found dead in the water. The next day, the ship and her crew were gone."   
                ]
            ],
            'respond':[
                [
                    "Hello, we arrived here by mistake. Where are we?",
                    "Bad luck I suppose. You've wandered into ^, known for ~.",
                    ". . . They still do that?"
                ],
                [
                    "Excuse me, can you direct me to the nearest island?",
                    "The island of Epithets lies far to the north, beware the icebergs.",
                    "I said nearest. . .",
                    "Sorry, I was programmed with flavor dialogue. . ."
                ]
            ]
        },

        'familiar':{
            'initiate':[
                [
                    "Hey, are you new here? This place doesn't usually take kindly to strangers.",
                    "We are. Thanks for the advice, we will tread carefully."
                ],
                [
                    "The last newcomers who passed through here didn't stay long",
                    "What happened? Were there hostilities?",
                    "The Ephatrix deal in secret. All we know is, one of the crew members were found dead in the water. The next day, the ship and her crew were gone."   
                ]
            ],
            'respond':[
                [
                    "Hello, we arrived here by mistake. Where are we?",
                    "Bad luck I suppose. You've wandered into ^, known for ~.",
                    ". . . They still do that?"
                ],
                [
                    "Excuse me, can you direct me to the nearest island?",
                    "The island of Epithets lies far to the north, beware the icebergs.",
                    "I said nearest. . .",
                    "Sorry, I was programmed with flavor dialogue. . ."
                ]
            ]
        },

        'trusted':{
            'initiate':[
                [
                    "Hey, are you new here? This place doesn't usually take kindly to strangers.",
                    "We are. Thanks for the advice, we will tread carefully."
                ],
                [
                    "The last newcomers who passed through here didn't stay long",
                    "What happened? Were there hostilities?",
                    "The Ephatrix deal in secret. All we know is, one of the crew members were found dead in the water. The next day, the ship and her crew were gone."   
                ]
            ],
            'respond':[
                [
                    "Hello, we arrived here by mistake. Where are we?",
                    "Bad luck I suppose. You've wandered into ^, known for ~.",
                    ". . . They still do that?"
                ],
                [
                    "Excuse me, can you direct me to the nearest island?",
                    "The island of Epithets lies far to the north, beware the icebergs.",
                    "I said nearest. . .",
                    "Sorry, I was programmed with flavor dialogue. . ."
                ]
            ]
        },

        'revered':{
            'initiate':[
                [
                    "Hey, are you new here? This place doesn't usually take kindly to strangers.",
                    "We are. Thanks for the advice, we will tread carefully."
                ],
                [
                    "The last newcomers who passed through here didn't stay long",
                    "What happened? Were there hostilities?",
                    "The Ephatrix deal in secret. All we know is, one of the crew members were found dead in the water. The next day, the ship and her crew were gone."   
                ]
            ],
            'respond':[
                [
                    "Hello, we arrived here by mistake. Where are we?",
                    "Bad luck I suppose. You've wandered into ^, known for ~.",
                    ". . . They still do that?"
                ],
                [
                    "Excuse me, can you direct me to the nearest island?",
                    "The island of Epithets lies far to the north, beware the icebergs.",
                    "I said nearest. . .",
                    "Sorry, I was programmed with flavor dialogue. . ."
                ]
            ]
        }
    }
}

def get_dialogue(relation:dict) -> list[dict[str, Crew |str]]:
    player = relation['crew'][0]
    interactee = relation['crew'][1]
    convo_starter:Crew = random.choice([player, interactee])
    dialogue_tree = general_dialog_trees[interactee.type]
    dialogue_branch = dialogue_tree[relation['relation_status']]
    dialogue:list[dict[str, Crew|str]] = []
    if convo_starter == player:
        dialogue_leaf = random.choice(dialogue_branch['respond'])
        for index, string in enumerate(dialogue_leaf):
            if index % 2 == 0:
                translation = _translate(string, player)
                dialogue.append({'speaker':player, 'text':translation})
            else:
                translation = _translate(string, interactee)
                dialogue.append({'speaker':interactee, 'text':translation})
    
    else:
        dialogue_leaf = random.choice(dialogue_branch['initiate'])
        for index, string in enumerate(dialogue_leaf):
            if index % 2 == 0:
                translation = _translate(string, interactee)
                dialogue.append({'speaker':interactee, 'text':translation})
            else:
                translation = _translate(string, player)
                dialogue.append({'speaker':player, 'text':translation})
    
    return dialogue


def _translate(dialogue_string:str, character:Crew) -> str:
    punctuation = dialogue_string[-1]
    words = dialogue_string[:-1].split(' ')
    new_dialogue = ''
    for word in words:
        new_word = word
        if word in archetype_vocabularies[character.archetype].keys():
            new_word = archetype_vocabularies[character.archetype].get(word)
        elif word in role_vocabularies[character.role].keys():
            new_word = role_vocabularies[character.role].get(word)
        new_dialogue += new_word + " "
    new_dialogue = new_dialogue[:-1] # cheap way to remove the unneeded empty space at the end
    new_dialogue += punctuation # add back the punctuation
    return new_dialogue


if __name__ == '__main__':
    print(_translate("this is my boom stick. please dont touch it."))