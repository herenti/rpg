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

weapon_dict = {'unarmed': '0 5 1 1 no 1',
               'short sword': '100 10 1 1 no 1',
               'bow': '100 13 1.5 1 yes 10',
               'dildo': '200 18 1 3 no 1',
               'flintlock pistol': '200 22 1.8 3 yes 10',
               'nuke': '1000000 1000000 10000 50 yes 1',
               'jizz': '0 1 0.1 1 yes 1',
               'orc penis': '500 38 1 6 no 1',
               'fury bow': '500 45 1.6 6 yes 10'
               }

potion_dict = {'health s': '20 25 health',
               'health m': '40 50 health',
               'health l': '80 100 health',
               'health xl': '160 200 health',
               'elixer': '400 500 health',
               'godsgrow': '1000 1000 health',
               'peerless health': '2500 3000 health',
               'accuracy': '100 0.1 accuracy',
               'peerless accuracy': '500 0.2 accuracy',
               'crit': '2000 0.2 critchance'
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
        _status = dict(critchance=0.07, health=100, level=1, attack_timeout=time.time(), exp=0, accuracy=0.75, marriage={}, effects={})
        _inventory = dict(weapons={'unarmed':[1, 'equipped']}, potions={}, items={}, money=150)
        skills = dict()
        _clan = random.choice(clan_list)
        _dict = dict(status=_status, inventory=_inventory, clan=_clan)
        rpg_players[user] = json.dumps(_dict)
        dumprpg()
        return 'registered in clan ' + _clan
    else:
        return 'you are already registered'

def _item(arg, user):
    try:
        try:
            _dict = json.loads(rpg_players[user])
        except:
            return 'you are not registered yet'
        try: arg, item = arg.split(' ',1)
        except: arg, item = arg, ''
        if arg == 'list':
            i = 'your items are: '+', '.join([i for i in _dict['inventory']['items']])
            return i
        if arg == 'info':
            _item = ' '.join(item_dict[item].split()[:-1])
            return item+': '+_item
    except: return 'invallid'

def _potion(arg, user):
    try:
        _dict = json.loads(rpg_players[user])
    except:
        return 'you are not registered yet'
    arg, item = arg.split(' ',1)
    if arg == 'drink':
        if _dict['inventory']['potions'][item] <= 0:
            return 'you are out of that potion'
        else:
            _dict['inventory']['potions'][item] -= 1
            if _dict['inventory']['potions'][item] <= 0:
                del _dict['inventory']['potions'][item]
            info = potion_dict[item].split()
            effect = info[2]
            val = info [1]
            if effect =='health': _dict['status']['health'] += int(val)
            else: _dict['status']['effects'][effect] = [time.time(), val]
            _dict['status']['exp'] += 5
            rpg_players[user] = json.dumps(_dict)
            dumprpg()
            return 'drank '+item+' potion'
                    
def _attack(user, _user):
    _dict = json.loads(rpg_players[user])
    __dict = json.loads(rpg_players[_user])
    if __dict['status']['health'] < 1:
        return 'you are dead. you cannot attack'
    if _dict['status']['health'] < 1:
        return 'your opponent is dead. you cannot attack'
    for i in __dict['inventory']['weapons']:
        _i = __dict['inventory']['weapons'][i]
        if _i[1] == 'equipped':
            weapon = i
            ammo = _i[0]
    _stats = weapon_dict[weapon].split()
    base_damage = int(_stats[1])
    attack_rate = int(_stats[2])*5
    if attack_rate > 10000: attack_rate = 10000
    timeout = time.time() - __dict['status']['attack_timeout']
    if timeout < attack_rate:
        return 'you find yourself unable to attack fast enough [%s seconds]' % str(round(attack_rate -  timeout))
    needs_ammo = _stats[4]
    max_damage = base_damage * 3.5
    accuracy = __dict['status']['accuracy']
    critchance = __dict['status']['critchance']
    try:
        _critchance = __dict['status']['effects']['critchance']
        _timeout = _critchance[0]
        _timeout = time.time() - _timeout
        if _timeout > 600:
            del __dict['status']['effects']['critchance']
        else:
            critchance += round(float(_critchance[1]), 1)
    except: pass
    try:
        _accuracy = __dict['status']['effects']['accuracy']
        print('accuracy')
        _timeout = _accuracy[0]
        _timeout = time.time() - _timeout
        if _timeout > 600:
            del __dict['status']['effects']['accuracy']
        else:
            accuracy += round(float(_accuracy[1]), 1)
    except: pass
    try:
        _invisibility = _dict['status']['effects']['invisibility']
        _timeout = _invisibility
        _timeout = time.time() - _timeout
        if _timeout > 600:
            del __dict['status']['effects']['invisibility']
        else:
            accuracy -= 0.35
    except: pass
    crit = False
    killed = False
    def hit_chance(i):
        part = i * 100
        _part = 100 - part
        part = ['y' for i in range(int(part))]
        _part = ['n' for i in range(int(_part))]
        part = part + _part
        hit = random.choice(part)
        return hit
    if hit_chance(accuracy) == 'n':
        __dict['status']['attack_timeout'] = time.time()
        rpg_players[_user] = json.dumps(__dict)
        rpg_players[user] = json.dumps(_dict)
        dumprpg()
        return 'you missed!!!'
    if hit_chance(critchance) == 'y':
        crit = True
        max_damage *= 2   
    min_damage = max_damage * 0.6
    damage = random.randrange(round(min_damage), round(max_damage))
    _dict['status']['health'] -= damage
    _exp = 5
    level = _dict['status']['level']*2
    _exp += level
    if _dict['status']['health'] <= 0:
        _dict['status']['health'] = 0
        killed = True
        level = level*5
        _exp += level
    __dict['status']['exp'] += _exp
    __dict['status']['attack_timeout'] = time.time()        
    rpg_players[user] = json.dumps(_dict)
    rpg_players[_user] = json.dumps(__dict)
    dumprpg()
    ret = 'attacked ' + user + ' for ' + str(damage)
    if crit == True: ret = ret + ': critical hit!!!'
    if killed == True: ret = ret + ': they were killed'
    return ret

def calc_level(i):
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

def _rpgstats(user, _user):
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
    clan = _dict['clan']
    if _rel == '': derp = ['name: '+user, rel, 'exp: ' + exp, 'level: '+level, 'health: '+health, 'clan: '+clan]
    else: derp = ['name: '+user, rel, _rel, 'exp: ' + exp, 'level: '+level, 'health: '+health, 'clan: '+clan]
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
    if arg == 'potion':
        i = potion_dict[_name].split()
        cost = int(i[0])
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return 'you do not have enough money'
        try: _dict['inventory']['potions'][_name] += amount
        except: _dict['inventory']['potions'][_name] = amount
    _dict['inventory']['money'] = money    
    _dict['status']['exp'] += 5
    rpg_players[user] = json.dumps(_dict)
    dumprpg()
    return 'you bought ' + str(amount) + ' ' + item.replace(' '+str(amount),'')

def dumprpg():
    f = open("rpg.txt", "w")
    for i in rpg_players:
           _dict = json.loads(rpg_players[i])
           f.write(json.dumps([i,_dict])+"\n")                                        
    f.close()
