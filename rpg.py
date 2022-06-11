import random
import time
import json
from text import rpg_players

'''
    for i in weapon_list:
        i[0] price
        i[1] damage
        i[2] rate
        i[3] level
        i[4] needs ammo
        i[5] starting ammo
'''

clan_list = ['derp']
weapon_dict = {'short sword': '100 10 1 1 no 1',
               'bow': '100 13 1.5 1 yes 10',
               'dildo': '200 18 1 3 no 1',
               'flintlock pistol': '200 22 1.8 3 yes 10',
               'nuke': '1000000 1000000 10000 50 yes 1',
               'jizz': '0 1 0.1 1 yes 1',
               'orc penis': '500 38 1 6 no 1',
               'fury bow': '500 45 1.6 6 yes 10'
               }

def register(user):
    if user not in rpg_players:
        _status = dict(critmult=1, health=100, level=1, exp=0)
        _inventory = dict(weapons={}, potions={}, items={}, money=150)
        _clan = random.choice(clan_list)
        _dict = dict(status=_status, inventory=_inventory, clan=_clan)
        rpg_players[user] = json.dumps(_dict)
        dumprpg()
        return 'registered in clan ' + _clan
    else:
        return 'you are already registered'

def buy(arg, user):
    try:
        rpg_players[user]
    except:
        return 'you are not registered yet'
    arg, item = arg.split(' ',1)
    _item = item.split()
    try:
        amount = int(_item[-1]) 
        _item.remove(_item[-1])
    except: amount = 1
    _name = ' '.join(_item)
    _dict = json.loads(rpg_players[user])
    money = _dict['inventory']['money']
    level = _dict['status']['level']
    if arg == 'weapon':
        i = weapon_dict[_name]
        i = i.split()
        cost = int(i[0])
        need_ammo = i[4]
        ammo = i[5]
        _level = int(i[3])
        if _level > level:
            return 'your level is not high enough'
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return 'you do not have enough money'
        _dict['inventory']['weapons'][_name] = ammo
        _dict['inventory']['money'] = money
        exp =_dict['status']['exp']
        exp += 5
        _dict['status']['exp'] = exp
        rpg_players[user] = json.dumps(_dict)
    dumprpg()
    return 'you bought ' + str(amount) + ' ' + item.replace(' '+str(amount),'')

def dumprpg():
    f = open("rpg.txt", "w")
    for i in rpg_players:
           _dict = json.loads(rpg_players[i])
           f.write(json.dumps([i,_dict])+"\n")                                        
    f.close()
