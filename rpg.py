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

clan_list = ['ethos','verity','regal','burathian','noctuo']

weapon_dict = {'short sword': '100 10 1 1 no 1',
               'bow': '100 13 1.5 1 yes 10',
               'dildo': '200 18 1 3 no 1',
               'flintlock pistol': '200 22 1.8 3 yes 10',
               'nuke': '1000000 1000000 10000 50 yes 1',
               'jizz': '0 1 0.1 1 yes 1',
               'orc penis': '500 38 1 6 no 1',
               'fury bow': '500 45 1.6 6 yes 10'
               }

potion_dict = {'health potion s': '20 25',
               'health potion m': '40 50',
               'health potion l': '80 100',
               'health potion xl': '160 200',
               'elixer': '400 500',
               'godsgrow extract': '1000 1000',
               'peerless health potion': '2500 3000',
               'accuracy potion': '100 0.1',
               'peerless accuracy potion': '500 0.2',
               'critmult potion': '100 0.2'
               }

item_dict = {'condom':'it might be used 100',
             'body pillow':'why is it stiff? 250',
             'stuffed animal':'for cuddles 100',
             'gold necklace':'fine craftmanship 1000',
             'pet cat':'this kitty chonk 500',
             'pet tiger':'it might eat you 10000',
             'pet dog':'a loyal companion!!! 500',
             'diamond earring':'sparkles like nothing else 3000',
             'wedding rings':'for the one you love [for marrying] 10000',
             'ethirium pendant':'very rare material of a mysterious nature 100000',
             'royal crest':'those with this crest will now have a royal title 1000000'
             }
             
             

def _register(user):
    if user not in rpg_players:
        _status = dict(critmult=1, health=100, level=1, exp=0, accuracy=0.75, marriage={})
        _inventory = dict(weapons={'unarmed':[1, 'equipped']}, potions={}, items={}, money=150)
        _clan = random.choice(clan_list)
        _dict = dict(status=_status, inventory=_inventory, clan=_clan)
        rpg_players[user] = json.dumps(_dict)
        dumprpg()
        return 'registered in clan ' + _clan
    else:
        return 'you are already registered'

def _attack(user):
    return

def _propose(arg, _user):
    try:
        arg, user = arg.split()
        _dict = json.loads(rpg_players[user])
        __dict = json.loads(rpg_players[_user])
        if arg == 'to':
            proposed = []
            try:
                _ret = _dict['status']['marriage']['proposed']
                proposed += _ret
            except:
                pass
            try:
                ret = _dict['status']['marriage']['married']
                return 'that user is already married to ' + ret
            except:
                __dict['inventory']['items']['wedding rings']
                proposed.append(_user)
                _dict['status']['marriage']['proposed'] = list(set(proposed))
                try:
                    ret = __dict['status']['marriage']['proposing']
                    return 'you are already proposing to ' + ret
                except:
                    __dict['status']['marriage']['proposing'] = user
                    rpg_players[user] = json.dumps(_dict)
                    rpg_players[_user] = json.dumps(__dict)
                    dumprpg()
                    return 'you have proposed to ' + user
        if arg == 'accept':
            ret = __dict['status']['marriage']['proposed']
            if user in ret:
                __dict['inventory']['items']['wedding rings'] = 'given'
                try: del __dict['status']['marriage']['proposed']           
                except: pass
                try: del _dict['status']['marriage']['proposed']
                except: pass
                try: del __dict['status']['marriage']['proposing']
                except: pass
                try: del _dict['status']['marriage']['proposing']
                except: pass
                for i in rpg_players:
                    derp = json.loads(rpg_players[i])
                    try:
                       if user in derp['status']['marriage']['proposed']:
                           derp['status']['marriage']['proposed'].remove(user)
                    except:
                        pass
                    try:
                        if _user in derp['status']['marriage']['proposed']:
                           derp['status']['marriage']['proposed'].remove(_user)
                    except:
                        pass
                    try:
                        if derp['status']['marriage']['proposing'] == user or _user:
                           del derp['status']['marriage']['proposing']
                    except:
                        pass
                    rpg_players[i] = json.dumps(derp)
                _dict['status']['marriage']['married'] =  _user
                __dict['status']['marriage']['married'] = user
                rpg_players[user] = json.dumps(_dict)
                rpg_players[_user] = json.dumps(__dict)
                dumprpg()
                return 'you are now married to ' + user
            else: return 'they have not proposed to you'
    except:
        return 'not vallid'

def rpgstatus(user, _user):
    user = _user if user == '' else user.lower()
    _dict = json.loads(rpg_players[user])
    rel = _dict['status']['marriage']
    try:
        proposed_to = rel['proposed']
        _rel = 'proposed to by: ' + ', '.join(rel['proposed'])
    except:
        _rel = ''
    try:
        married_to = rel['married']
        rel = 'married to: ' + married_to
    except: rel = 'not married'
    level = str(_dict['status']['level'])
    exp = str(_dict['status']['exp'])
    health = str(_dict['status']['health'])
    if _rel == '': derp = ['name: '+user, rel, 'exp: ' + exp, 'level: '+level, 'health: '+health]
    else: derp = ['name: '+user, rel, _rel, 'exp: ' + exp, 'level: '+level, 'health: '+health]
    return '<br/><br/>' + '<br/>'.join(derp)
    

def _equip(weapon, user):
    _dict = json.loads(rpg_players[user])
    try:
        for i in _dict['inventory']['weapons']:
            if _dict['inventory']['weapons'][i][1] == 'equipped':
                _dict['inventory']['weapons'][i].remove('equipped')
                _dict['inventory']['weapons'][i].append('unequipped')
        _dict['inventory']['weapons'][weapon].remove('unequipped')
        _dict['inventory']['weapons'][weapon].append('equipped')
        rpg_players[user] = json.dumps(_dict)
        dumprpg()
        return 'equipped ' + weapon
    except:
        return 'you do not have that weapon'

def _buy(arg, user):
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
        i = weapon_dict[_name].split()
        cost = int(i[0])
        need_ammo = i[4]
        ammo = int(i[5])
        if need_ammo == 'yes':
            ammo *= amount        
        _level = int(i[3])
        if _level > level:
            return 'your level is not high enough'
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return 'you do not have enough money'
        _dict['inventory']['weapons'][_name] = [ammo, 'unequipped']
    if arg == 'item':
        i = item_dict[_name].split()
        cost = int(i[-1])
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return 'you do not have enough money'
        _dict['inventory']['items'][_name] = 'purchased'              
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
