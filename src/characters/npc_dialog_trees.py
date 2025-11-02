import re
from copy import deepcopy
from typing import Dict, Any, List, Tuple

dialog_trees = {
    # ============================= SHOP TREES =============================
    'shop_1': {
        'greetings': {
            'quest': {
                'new': "We need supplies delivered to the outpost. Interested?%*",
                'familiar': "Back for another run? Same route, better pay.%*"
            },
            'lore': {
                'new': "Our best rope comes from the northern islands.&",
                'familiar': "You bought the last coil of deep-sea line.&"
            },
            'emotion': {
                'new': "Business is slow. Could use a good sale.&",
                'familiar': "You're our best customer this month.&"
            },
            'default': {
                'new': "Welcome. Browse our stock. Prices are marked.*",
                'familiar': "Back again. Need more provisions?*"
            }
        },
        'farewells': {
            'quest': {
                'new': "Deliver by dawn. No delays.&",
                'familiar': "You know the drop point. Don't be late.&"
            },
            'lore': {
                'new': "That silk? From a wreck off Crimson Reef.&",
                'familiar': "Still no word on the missing shipment.&"
            },
            'emotion': {
                'new': "Thanks. You saved our ledger today.&",
                'familiar': "Always a pleasure. See you next tide.&"
            },
            'default': {
                'new': "Fair trading. Safe voyage.*",
                'familiar': "Come back when you're low on rum.*"
            }
        }
    },

    'shop_2': {
        'greetings': {
            'quest': {
                'new': "Lost a crate overboard. Retrieve it for a reward.%*",
                'familiar': "You found the last one. Try again?%*"
            },
            'lore': {
                'new': "We only stock ironwood. Lasts through storms.&",
                'familiar': "That barrel you bought? Still sealed.&"
            },
            'emotion': {
                'new': "Crew's hungry. Need a big sale soon.&",
                'familiar': "Your coin keeps us afloat. Literally.&"
            },
            'default': {
                'new': "Step aboard. Fresh goods just in.*",
                'familiar': "Knew you'd return. Got new stock.*"
            }
        },
        'farewells': {
            'quest': {
                'new': "Find the red buoy. Crate's nearby.&",
                'familiar': "Same depth. Watch for sharks.&"
            },
            'lore': {
                'new': "Ironwood doesn't rot. Worth the price.&",
                'familiar': "Next shipment arrives at full moon.&"
            },
            'emotion': {
                'new': "Grateful for the trade. Truly.&",
                'familiar': "You're family now. Almost.&"
            },
            'default': {
                'new': "Good doing business. Clear skies.*",
                'familiar': "Don't spend it all in one port.*"
            }
        }
    },

    'shop_3': {
        'greetings': {
            'quest': {
                'new': "Need a message sent to Fort Charles. You sailing that way?%*",
                'familiar': "Another letter. Same contact?%*"
            },
            'lore': {
                'new': "We trade in charts. Accurate ones.&",
                'familiar': "You still have that reef map? Good.&"
            },
            'emotion': {
                'new': "Port fees are killing us. Need volume.&",
                'familiar': "Your repeat business keeps the lights on.&"
            },
            'default': {
                'new': "Open for trade. What do you need?*",
                'familiar': "Usual order? Or something new?*"
            }
        },
        'farewells': {
            'quest': {
                'new': "Seal must stay intact. Understood?&",
                'familiar': "Deliver to the quartermaster only.&"
            },
            'lore': {
                'new': "That chart shows a shortcut. Risky.&",
                'familiar': "Avoid the marked shoal at low tide.&"
            },
            'emotion': {
                'new': "Your trust means much. Thank you.&",
                'familiar': "Loyal customers are rare. Stay safe.&"
            },
            'default': {
                'new': "Transaction complete. Fair winds.*",
                'familiar': "See you on the return leg.*"
            }
        }
    },

    'shop_4': {
        'greetings': {
            'quest': {
                'new': "Buy this spyglass. Then report what you see.%*",
                'familiar': "Still using that glass? Got a job.%*"
            },
            'lore': {
                'new': "This lens came from a naval wreck.&",
                'familiar': "You spotted that ship last week. Good eye.&"
            },
            'emotion': {
                'new': "Crew's restless. Need a big score.&",
                'familiar': "Your trades keep morale high.&"
            },
            'default': {
                'new': "Rare items today. Take a look.*",
                'familiar': "Saved the best for you.*"
            }
        },
        'farewells': {
            'quest': {
                'new': "Watch the eastern horizon at dawn.&",
                'familiar': "Report back in code. Same as before.&"
            },
            'lore': {
                'new': "That glass magnifies 20 times. True.&",
                'familiar': "Next item: a compass that never lies.&"
            },
            'emotion': {
                'new': "Hope this deal turns your luck.&",
                'familiar': "You're more than a customer now.&"
            },
            'default': {
                'new': "Pleasure trading. Smooth sailing.*",
                'familiar': "Until the next haul.*"
            }
        }
    },

    # ============================= GENERAL TREES =============================
    'general_1': {
        'greetings': {
            'quest': {
                'new': "We need help fixing the mast. You handy?%*",
                'familiar': "Mast cracked again. You free?%*"
            },
            'lore': {
                'new': "This route's been safe for months.&",
                'familiar': "You took the northern passage last time?&"
            },
            'emotion': {
                'new': "Crew's tired. Long voyage.&",
                'familiar': "Missed your company out here.&"
            },
            'default': {
                'new': "Hail. You alone out here?&",
                'familiar': "Good to see a familiar sail.&"
            }
        },
        'farewells': {
            'quest': {
                'new': "Patch it before the next squall.&",
                'familiar': "You know the weak spot. Fix it.&"
            },
            'lore': {
                'new': "Watch for fog in the straits.&",
                'familiar': "That shortcut saved you three days.&"
            },
            'emotion': {
                'new': "Thanks for the chat. Lifts the spirit.&",
                'familiar': "You're always welcome aboard.&"
            },
            'default': {
                'new': "Fair winds and following seas.&",
                'familiar': "Until we cross wakes again.&"
            }
        }
    },

    'general_2': {
        'greetings': {
            'quest': {
                'new': "Need a lookout for one hour. Pay in rum.%*",
                'familiar': "Spotting duty again. You in?%*"
            },
            'lore': {
                'new': "The stars here point true north.&",
                'familiar': "You still navigate by the old way?&"
            },
            'emotion': {
                'new': "Lonely out here. Good to see another soul.&",
                'familiar': "Your visits break the monotony.&"
            },
            'default': {
                'new': "Well met. What news from the world?&",
                'familiar': "Back so soon? What's the rush?&"
            }
        },
        'farewells': {
            'quest': {
                'new': "Keep eyes on the horizon. Report anything.&",
                'familiar': "Same signal as last time. Three flashes.&"
            },
            'lore': {
                'new': "That constellation? Sailor's guide home.&",
                'familiar': "You memorized the star map yet?&"
            },
            'emotion': {
                'new': "Your kindness is remembered.&",
                'familiar': "You're a good friend of the sea.&"
            },
            'default': {
                'new': "May calm seas follow you.&",
                'familiar': "Safe journey, old friend.&"
            }
        }
    },

    'general_3': {
        'greetings': {
            'quest': {
                'new': "Share your water? We'll repay in port.%*",
                'familiar': "Running low again. Spare a barrel?%*"
            },
            'lore': {
                'new': "Rain's scarce this season.&",
                'familiar': "You still have that spare cask?&"
            },
            'emotion': {
                'new': "Thirsty work, sailing these dry waters.&",
                'familiar': "Your generosity saved us last time.&"
            },
            'default': {
                'new': "Ahoy. You look well-provisioned.&",
                'familiar': "Still carrying extra, I see.&"
            }
        },
        'farewells': {
            'quest': {
                'new': "We'll settle the debt at the next dock.&",
                'familiar': "Add it to the tab. No rush.&"
            },
            'lore': {
                'new': "Next rain's due in two days. Maybe.&",
                'familiar': "Clouds building west. Fingers crossed.&"
            },
            'emotion': {
                'new': "Grateful doesn't cover it.&",
                'familiar': "You're a lifesaver. Again.&"
            },
            'default': {
                'new': "Thanks for the talk. Onward.&",
                'familiar': "See you under better skies.&"
            }
        }
    },

    'general_4': {
        'greetings': {
            'quest': {
                'new': "Trade stories for food? We're starving for news.%*",
                'familiar': "Got any fresh tales from port?%*"
            },
            'lore': {
                'new': "No land in sight for weeks.&",
                'familiar': "You made it to the volcano island?&"
            },
            'emotion': {
                'new': "Boredom's worse than hunger sometimes.&",
                'familiar': "Your stories are worth their weight.&"
            },
            'default': {
                'new': "Hail. Got a minute to talk?&",
                'familiar': "Always time for a good yarn.&"
            }
        },
        'farewells': {
            'quest': {
                'new': "That tale will carry us through the night.&",
                'familiar': "We'll retell it at every port.&"
            },
            'lore': {
                'new': "Next landfall: three days east.&",
                'familiar': "Avoid the sargasso patch south.&"
            },
            'emotion': {
                'new': "Lifted our spirits. Thank you.&",
                'familiar': "You're a born storyteller.&"
            },
            'default': {
                'new': "Until the next crossing.&",
                'familiar': "Keep the legends alive.&"
            }
        }
    },

    # ============================= QUEST TREES =============================
    'quest_1': {
        'greetings': {
            'quest': {
                'new': "Find the lost buoy. Reward if returned.%*",
                'familiar': "Still hunting that buoy? Any sign?%*"
            },
            'lore': {
                'new': "It marks a safe channel through the reefs.&",
                'familiar': "Last seen near the whirlpool.&"
            },
            'emotion': {
                'new': "We can't navigate without it.&",
                'familiar': "You're our only hope now.&"
            },
            'default': {
                'new': "Have you seen a red buoy with a bell?&",
                'familiar': "Any luck on the search?&"
            }
        },
        'farewells': {
            'quest': {
                'new': "Bring it back intact. Bell and all.&",
                'familiar': "We'll double the reward if fast.&"
            },
            'lore': {
                'new': "Currents drag everything southwest.&",
                'familiar': "Check the seaweed clusters.&"
            },
            'emotion': {
                'new': "Desperate times. Please help.&",
                'familiar': "We trust you. Don't fail us.&"
            },
            'default': {
                'new': "Good luck. Be careful out there.&",
                'familiar': "Report back when you find it.&"
            }
        }
    },

    'quest_2': {
        'greetings': {
            'quest': {
                'new': "Deliver this letter. No questions.%*",
                'familiar': "Another sealed letter. Same recipient?%*"
            },
            'lore': {
                'new': "Addressed to someone in black sails.&",
                'familiar': "You delivered the last one safely.&"
            },
            'emotion': {
                'new': "This could change everything.&",
                'familiar': "Your discretion is appreciated.&"
            },
            'default': {
                'new': "Can you take this to the cove at dusk?&",
                'familiar': "You know the drop. Same as before.&"
            }
        },
        'farewells': {
            'quest': {
                'new': "Don't read it. Just deliver.&",
                'familiar': "Burn after reading. As usual.&"
            },
            'lore': {
                'new': "The sender paid in gold. A lot.&",
                'familiar': "Reply expected within the week.&"
            },
            'emotion': {
                'new': "Lives may depend on this.&",
                'familiar': "You're part of something bigger now.&"
            },
            'default': {
                'new': "Safe journey. And silent.&",
                'familiar': "See you on the return.&"
            }
        }
    },
}

archetype_filters = {
    'pirate': {
        'welcome': 'ahoy',
        'hello': 'ahoy',
        'you': 'ye',
        'your': 'yer',
        'our': 'me',
        'we': 'we',
        'are': 'be',
        'is': 'be',
        'browse': 'eyeball',
        'look': 'gander',
        'stock': 'wares',
        'prices': 'prices',
        'marked': 'carved in stone',
        'need': 'be needin',
        'help': 'lend a hand',
        'goodbye': 'fare thee well',
        'thanks': 'much obliged',
        'please': 'if ye please',
        'yes': 'aye',
        'no': 'nay',
        'question': 'query',
        'interested': 'keen',
        'deal': 'bargain',
        'trade': 'swap',
        'safe': 'fair winds',
        'come back': 'return to port',
        'see you': 'catch ye on the tide'
    },
    'colonial': {
        'welcome': 'good day',
        'hello': 'greetings',
        'you': 'sir',
        'your': 'your',
        'our': 'our',
        'we': 'we',
        'are': 'are',
        'is': 'is',
        'browse': 'peruse',
        'look': 'examine',
        'stock': 'inventory',
        'prices': 'rates',
        'marked': 'listed',
        'need': 'require',
        'help': 'assistance',
        'goodbye': 'farewell',
        'thanks': 'my thanks',
        'please': 'if you please',
        'yes': 'indeed',
        'no': 'I decline',
        'question': 'inquiry',
        'interested': 'intrigued',
        'deal': 'arrangement',
        'trade': 'commerce',
        'safe': 'godspeed',
        'come back': 'return at your leisure',
        'see you': 'until we meet again'
    },
    'smuggler': {
        'welcome': 'psst',
        'hello': 'oi',
        'you': 'mate',
        'your': 'yer',
        'our': 'our',
        'we': 'we',
        'are': 'are',
        'is': 'is',
        'browse': 'take a peek',
        'look': 'check',
        'stock': 'the goods',
        'prices': 'cost',
        'marked': 'final',
        'need': 'after',
        'help': 'a favor',
        'goodbye': 'keep it quiet',
        'thanks': 'owe ya',
        'please': 'c’mon',
        'yes': 'deal',
        'no': 'pass',
        'question': 'word',
        'interested': 'in',
        'deal': 'the job',
        'trade': 'swap',
        'safe': 'no trouble',
        'come back': 'next drop',
        'see you': 'later'
    }
}

role_filters = {
    'angler': {
        'stock': 'bait and tackle',
        'wares': 'nets and hooks',
        'inventory': 'fishing gear',
        'browse': 'check the nets',
        'look': 'eye the traps',
        'examine': 'inspect the lines',
        'need': 'hookin',
        'require': 'baitin',
        'help': 'a cast',
        'assistance': 'a line',
        'interesting': 'big one',
        'prime': 'monster catch',
        'rare': 'legendary fish',
        'place': 'fishin hole',
        'market': 'best tide',
        'area': 'deep drop',
        'work': 'haulin nets',
        'working': 'castin lines',
        'trade': 'swap catches',
        'deal': 'fresh haul',
        'cargo': 'barrels of fish',
        'provisions': 'salted cod',
        'safe': 'no sharks',
        'come back': 'when the tide’s right',
        'see you': 'next full moon',
        'water': 'brine',
        'sea': 'the drink',
        'storm': 'blow',
        'wind': 'breeze off the reef',
        'island': 'atoll',
        'ship': 'skiff',
        'crew': 'deckhand',
        'you': 'cap’n',
        'we': 'the crew'
    },
    'rock_hound': {
        'stock': 'picks and chisels',
        'wares': 'ore samples',
        'inventory': 'raw gems',
        'browse': 'sort the stones',
        'look': 'scan the haul',
        'examine': 'grade the rocks',
        'need': 'diggin',
        'require': 'blastin',
        'help': 'a vein',
        'assistance': 'a strike',
        'interesting': 'motherlode',
        'prime': 'high-grade seam',
        'rare': 'blood diamond',
        'place': 'quarry face',
        'market': 'refinery',
        'area': 'crater ridge',
        'work': 'breakin rock',
        'working': 'hammerin stone',
        'trade': 'swap nuggets',
        'deal': 'raw ore',
        'cargo': 'sacks of quartz',
        'provisions': 'lantern oil',
        'safe': 'no cave-ins',
        'come back': 'after the next blast',
        'see you': 'when the dust settles',
        'water': 'underground spring',
        'sea': 'dry dock',
        'storm': 'rockslide',
        'wind': 'tunnel draft',
        'island': 'volcanic peak',
        'ship': 'cargo hauler',
        'crew': 'miner',
        'you': 'foreman',
        'we': 'the crew'
    },
    'oarsman': {
        'stock': 'oars and tholes',
        'wares': 'sweat and muscle',
        'inventory': 'spare benches',
        'browse': 'check the stroke',
        'look': 'time the pull',
        'examine': 'feel the rhythm',
        'need': 'pullin',
        'require': 'rowin hard',
        'help': 'a stroke',
        'assistance': 'a beat',
        'interesting': 'strong current',
        'prime': 'tailwind run',
        'rare': 'perfect cadence',
        'place': 'open lane',
        'market': 'finish line',
        'area': 'smooth water',
        'work': 'haulin oar',
        'working': 'keepin time',
        'trade': 'swap shifts',
        'deal': 'faster passage',
        'cargo': 'light load',
        'provisions': 'water skins',
        'safe': 'no blisters',
        'come back': 'at the next tide',
        'see you': 'on the downbeat',
        'water': 'channel',
        'sea': 'the race',
        'storm': 'headwind',
        'wind': 'following breeze',
        'island': 'lee shore',
        'ship': 'longboat',
        'crew': 'rower',
        'you': 'coxswain',
        'we': 'the bench'
    },
    'trader': {
        'stock': 'cargo manifest',
        'wares': 'trade goods',
        'inventory': 'market rates',
        'browse': 'review the ledger',
        'look': 'check the margins',
        'examine': 'audit the books',
        'need': 'negotiate',
        'require': 'counter-offer',
        'help': 'a bargain',
        'assistance': 'a deal',
        'interesting': 'hot commodity',
        'prime': 'bull market',
        'rare': 'exclusive contract',
        'place': 'best market',
        'market': 'trading post',
        'area': 'port of call',
        'work': 'makin deals',
        'working': 'closing sales',
        'trade': 'barter',
        'deal': 'final price',
        'cargo': 'hold full',
        'provisions': 'luxury items',
        'safe': 'no tariffs',
        'come back': 'when prices rise',
        'see you': 'at the exchange',
        'water': 'shipping lane',
        'sea': 'trade winds',
        'storm': 'market crash',
        'wind': 'favorable rates',
        'island': 'free port',
        'ship': 'merchantman',
        'crew': 'factor',
        'you': 'buyer',
        'we': 'the house'
    },
    'carpenter': {
        'stock': 'planks and caulk',
        'wares': 'timber and tar',
        'inventory': 'spare beams',
        'browse': 'check the grain',
        'look': 'eye the damage',
        'examine': 'measure the breach',
        'need': 'patchin',
        'require': 'caulkin',
        'help': 'a mend',
        'assistance': 'a brace',
        'interesting': 'critical leak',
        'prime': 'solid oak',
        'rare': 'ironwood patch',
        'place': 'dry dock',
        'market': 'shipyard',
        'area': 'below waterline',
        'work': 'hammerin nails',
        'working': 'sawing planks',
        'trade': 'swap lumber',
        'deal': 'repair contract',
        'cargo': 'ballast stone',
        'provisions': 'pitch and oakum',
        'safe': 'no splinters',
        'come back': 'after the swell',
        'see you': 'when she’s tight again',
        'water': 'bilge',
        'sea': 'the frame',
        'storm': 'taking on water',
        'wind': 'creaking mast',
        'island': 'timber caye',
        'ship': 'hull',
        'crew': 'chipper',
        'you': 'captain',
        'we': 'the yard'
    },
    'navigator': {
        'stock': 'charts and sextants',
        'wares': 'star maps',
        'inventory': 'logbooks',
        'browse': 'plot the course',
        'look': 'take a bearing',
        'examine': 'read the stars',
        'need': 'a heading',
        'require': 'true north',
        'help': 'a fix',
        'assistance': 'a position',
        'interesting': 'uncharted waters',
        'prime': 'perfect meridian',
        'rare': 'ley line',
        'place': 'true north',
        'market': 'cartographer’s guild',
        'area': 'open ocean',
        'work': 'plotting course',
        'working': 'shooting the sun',
        'trade': 'swap bearings',
        'deal': 'secret route',
        'cargo': 'blank charts',
        'provisions': 'ink and quills',
        'safe': 'no fog',
        'come back': 'at high noon',
        'see you': 'under the same stars',
        'water': 'latitude',
        'sea': 'the grid',
        'storm': 'magnetic deviation',
        'wind': 'prevailing current',
        'island': 'uncharted isle',
        'ship': 'vessel',
        'crew': 'quartermaster',
        'you': 'captain',
        'we': 'the watch'
    },
    'surgeon': {
        'stock': 'bandages and salves',
        'wares': 'herbs and rum',
        'inventory': 'medical kit',
        'browse': 'check the wounds',
        'look': 'take a pulse',
        'examine': 'diagnose',
        'need': 'stitchin',
        'require': 'amputatin',
        'help': 'a poultice',
        'assistance': 'a dose',
        'interesting': 'plague outbreak',
        'prime': 'miracle cure',
        'rare': 'fountain herb',
        'place': 'sick bay',
        'market': 'apothecary',
        'area': 'below deck',
        'work': 'tendin wounds',
        'working': 'boilin instruments',
        'trade': 'swap remedies',
        'deal': 'health contract',
        'cargo': 'medical crates',
        'provisions': 'laudanum',
        'safe': 'no infection',
        'come back': 'after the fever breaks',
        'see you': 'when you’re whole',
        'water': 'blood',
        'sea': 'the fever',
        'storm': 'outbreak',
        'wind': 'plague wind',
        'island': 'leper colony',
        'ship': 'hospital ship',
        'crew': 'patient',
        'you': 'captain',
        'we': 'the orderlies'
    },
    'cook': {
        'stock': 'hard tack and salt pork',
        'wares': 'stew and grog',
        'inventory': 'spice rack',
        'browse': 'sample the pot',
        'look': 'check the fire',
        'examine': 'taste the broth',
        'need': 'cookin',
        'require': 'servin',
        'help': 'a ladle',
        'assistance': 'a portion',
        'interesting': 'fresh catch',
        'prime': 'five-star meal',
        'rare': 'kraken steak',
        'place': 'galley stove',
        'market': 'mess deck',
        'area': 'below deck',
        'work': 'stirrin pots',
        'working': 'peelin spuds',
        'trade': 'swap recipes',
        'deal': 'full belly',
        'cargo': 'provision crates',
        'provisions': 'fresh bread',
        'safe': 'no weevils',
        'come back': 'at mess call',
        'see you': 'when the bell rings',
        'water': 'broth',
        'sea': 'the slush',
        'storm': 'spoiled rations',
        'wind': 'kitchen draft',
        'island': 'spice atoll',
        'ship': 'galley',
        'crew': 'messmate',
        'you': 'captain',
        'we': 'the scullery'
    }
}


def filtered_dialogue(
    role: str,
    archetype: str,
    character_type: str
) -> Dict[str, Any]:
    """
    Return a **fully filtered** dialog tree for a crew member.

    Parameters
    ----------
    role : str
        Crew role (e.g. 'angler', 'trader', 'cook'). Must exist in ``role_filters``.
    archetype : str
        Personality style (e.g. 'pirate', 'colonial'). Must exist in ``archetype_filters``.
    character_type : str
        Tree key (e.g. 'shop_1', 'general_2', 'yesno_1'). Must exist in ``dialog_trees``.

    Returns
    -------
    dict
        Deep-copied and filtered dialog tree ready for ``self.dialoge``.
    """
    # 1. Load the *bland* base tree
    try:
        base_tree: Dict[str, Any] = dialog_trees[character_type]
    except KeyError:
        raise ValueError(f"Unknown character_type: {character_type!r}")

    # 2. Build the filter chain (archetype first, then role)
    chain: List[Tuple[Dict[str, str], str]] = []

    if archetype and archetype in archetype_filters:
        chain.append((archetype_filters[archetype], f"archetype:{archetype}"))

    if role and role in role_filters:
        chain.append((role_filters[role], f"role:{role}"))

    if not chain:
        # No filters → just return a safe copy
        return deepcopy(base_tree)

    # 3. Batch-filter the whole tree in one pass
    return _deep_filter_tree(base_tree, chain)


# ----------------------------------------------------------------------
# INTERNAL HELPERS
# ----------------------------------------------------------------------
def _deep_filter_tree(
    tree: Dict[str, Any],
    chain: List[Tuple[Dict[str, str], str]]
) -> Dict[str, Any]:
    """Recursively filter every string leaf while preserving dict structure."""
    result: Dict[str, Any] = {}
    for key, value in tree.items():
        if isinstance(value, dict):
            result[key] = _deep_filter_tree(value, chain)
        elif isinstance(value, str):
            result[key] = _filter_line(value, chain)
        else:
            result[key] = value
    return result


def _filter_line(text: str, chain: List[Tuple[Dict[str, str], str]]) -> str:
    """Apply the full chain to a single line, preserving the final marker."""
    if not text:
        return text

    # Extract marker (*, %, &) if present
    marker = ''
    if text[-1] in '*%&':
        marker = text[-1]
        text = text[:-1].rstrip()

    current = text

    # Apply each filter in order
    for filt, _name in chain:
        # Longest keys first → avoid substring overwrites
        for find, repl in sorted(filt.items(), key=lambda x: len(x[0]), reverse=True):
            pattern = re.compile(r'\b' + re.escape(find) + r'\b', re.IGNORECASE)
            current = pattern.sub(repl, current)

    return current + marker


if __name__ == '__main__':
    tree = filtered_dialogue('angler', 'pirate', 'general_1')
    print(tree)