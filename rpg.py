import random
import time

'''
    for i in weapon_list:
        i[0] name
        i[1] price
        i[2] damage
        i[3] rate
        i[4] level
        i[5] needs ammo
'''

rpg_players = dict()
clan_list = ['derp']
weapon_list = ['short-sword 100 10 1 1 no',
               'bow 100 13 1.5 1 yes',
               'dildo 200 18 1 3 no',
               'flintlock-pistol 200 22 1.8 3 yes',
               'nuke 1000000 1000000 10000 50 yes',
               'jizz 0 1 0.1 1 yes',
               'orc-penis 500 38 1 6 no',
               'fury-bow 500 45 1.6 6 yes'
               ]

def register(user):
    _status = []
    _status.append('critmult-1')
    _status.append('health-100')
    weapons = []
    potions = []
    items = []
    _dict = dict(status=_status, inventory=[weapons, potions, items],clan=random.choice(clan_list))
    rpg_players[user] = _dict
    return 'registered'
    

