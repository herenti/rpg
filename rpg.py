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
    if user not in rpg_players:
        _status = []
        _status.append('critmult-1')
        _status.append('health-100')
        weapons = []
        potions = []
        items = []
        _clan = random.choice(clan_list)
        money = 100
        _dict = dict(status=_status, inventory=[weapons, potions, items, money], clan=_clan)
        rpg_players[user] = _dict
        return 'registered in clan ' + _clan
    else:
        return 'you are already registered'

def buy(arg):
    arg, item = arg.split(' ',1)
    item = item.split()
    try:
        amount = int(item[-1])
        item.remove(item[-1])
    except: amount = 1
    _name = '-'.join(item)
    _inv, potions, items, money = rpg_players['herenti']['inventory']
    if arg == 'weapon':
        for i in weapon_list:
            i = i.split()
            if i[0] == _name:
                cost = int(i[1])
                ammo = i[5]
                if i[5] == 'yes':
                    ammo = '10'
                break
        cost *= amount
        if money >= cost:
            money -= cost
            _inv.append(_name+ ' ' +ammo)
        else:
            return 'not enough money'
        rpg_players['herenti']['inventory'] = _inv, potions, items, money

register('herenti')
    
    

