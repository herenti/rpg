import random
import time
import json
import urllib.parse
import urllib.request
import re

rpg_players = dict()
f = open('rpg.txt', 'r')
print('Loading rpg...')
for line in f.readlines():
        try:
                if len(line) > 0:
                        user, _dict = json.loads(line.strip())
                        rpg_players[user] = json.dumps(_dict)        
        except Exception as e:
                print("Could not load rpg: %s" % e)
f.close()

clan_list = ['ethos','verity','regal','burathian','noctuo']

weapon_dict = {'unarmed': '0 5 1 1 no 1 mele',
               'short sword': '100 10 1 1 no 1 mele',
               'bow': '100 13 2.5 1 yes 10 ranged',
               'dildo': '200 18 1 3 no 1 mele',
               'flintlock pistol': '200 24 2.8 3 yes 10 ranged',
               'nuke': '1000000 1000000 10000 50 yes 1 ranged',
               'jizz': '0 1 0.1 1 yes 1 ranged',
               'orc penis': '500 38 1 6 no 1 mele',
               'fury bow': '500 45 2.5 6 yes 10 ranged'
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

max_health = {'1': 110, '2': 121, '3': 133, '4': 146, '5': 161, '6': 177, '7': 195, '8': 214, '9': 236, '10': 259, '11': 285, '12': 314, '13': 345, '14': 380, '15': 418, '16': 459, '17': 505, '18': 556, '19': 612, '20': 673, '21': 740, '22': 814, '23': 895, '24': 985,
              '25': 1083, '26': 1192, '27': 1311, '28': 1442, '29': 1586, '30': 1745, '31': 1919, '32': 2111, '33': 2323, '34': 2555, '35': 2810, '36': 3091, '37': 3400, '38': 3740, '39': 4114, '40': 4526, '41': 4979, '42': 5476, '43': 6024, '44': 6626, '45': 7289, '46': 8018, '47': 8820, '48': 9702, '49': 10672,
              '50': 11739, '51': 12913, '52': 14204, '53': 15625, '54': 17187, '55': 18906, '56': 20797, '57': 22876, '58': 25164, '59': 27680, '60': 30448, '61': 33493, '62': 36842, '63': 40527, '64': 44579, '65': 49037, '66': 53941, '67': 59335, '68': 65268, '69': 71795, '70': 78975, '71': 86872, '72': 95559, '73': 105115, '74': 115627,
              '75': 127190, '76': 139908, '77': 153899, '78': 169289, '79': 186218, '80': 204840, '81': 225324, '82': 247856, '83': 272642, '84': 299906, '85': 329897, '86': 362887, '87': 399175, '88': 439093, '89': 483002, '90': 531302, '91': 584432, '92': 642876, '93': 707163, '94': 777880, '95': 855668, '96': 941234, '97': 1035358, '98': 1138894, '99': 1252783, '100': 1378061
              }
    
def _register(x, user, uid, roomname, othervars):
    if user not in rpg_players:
        _status = dict(critchance=0.07, health=110, level=1, attack_timeout=time.time(), exp=0, accuracy=0.75, marriage={}, effects={})
        _inventory = dict(weapons={'unarmed':['equipped', 1]}, potions={}, items={}, money=150)
        skills = dict()
        _clan = random.choice(clan_list)
        _dict = dict(status=_status, inventory=_inventory, clan=_clan)
        rpg_players[user] = json.dumps(_dict)
        calc_level(user)
        return 'registered in clan ' + _clan
    else:
        return 'you are already registered'

def _item(arg, user, uid, roomname, othervars):
    try:
        try:
            _dict = json.loads(rpg_players[user])
        except:
            return 'you are not registered yet'
        try: title = _dict['title'] + ', '
        except: title = ''
        try: arg, item = arg.split(' ',1)
        except: arg, item = arg, ''
        if arg == 'list':
            i = ', '.join([i+': cost-'+item_dict[i].split()[-1] for i in item_dict])
            return i
        elif arg == 'mylist':
            if len([i for i in _dict['inventory']['items']]) > 0:
                i = title+'your items are: '+', '.join([i for i in _dict['inventory']['items']])
                return i
            else: return title+'you have no items'
        elif arg == 'info':
            _item = ' '.join(item_dict[item].split()[:-1])
            return item+': '+_item
    except: return 'invallid'

def _potion(arg, user, uid, roomname, othervars):
    try:
        _dict = json.loads(rpg_players[user])
    except:
        return 'you are not registered yet'
    try: title = _dict['title'] + ', '
    except: title = ''
    try: arg, item = arg.split(' ',1)
    except: pass
    if arg == 'drink':
        if _dict['inventory']['potions'][item] <= 0:
            return title+'you are out of that potion'
        else:
            _dict['inventory']['potions'][item] -= 1
            if _dict['inventory']['potions'][item] <= 0:
                del _dict['inventory']['potions'][item]
            info = potion_dict[item].split()
            effect = info[2]
            val = info [1]
            level = _dict['status']['level']
            if effect == 'health':
                amount = _dict['status']['health'] + int(val)
                _amount = max_health[str(level)]
                if amount > _amount:
                    _dict['status']['health'] = _amount
                else:
                    _dict['status']['health'] += int(val)
            else:
                _dict['status']['effects'][effect] = [time.time(), val]
            _dict['status']['exp'] += 5
            rpg_players[user] = json.dumps(_dict)
            calc_level(user)
            return title+'you drank: ['+item+' potion]'
    elif arg == 'list':
        return ', '.join([i+': cost - '+potion_dict[i].split()[0] for i in potion_dict])
    elif arg == 'mylist':
        try: return ', '.join([i+': supply - '+_dict['inventory']['potions'][i] for i in _dict['inventory']['potions']])
        except: return 'no potions'
        
def _weapon(arg, user, uid, roomname, othervars):
    try:  _dict = json.loads(rpg_players[user])
    except: return 'you are not registered yet'
    try: arg, item = arg.split(' ',1)
    except: pass
    if arg == 'list':
        return ', '.join([i+': cost-'+weapon_dict[i].split()[0] for i in weapon_dict])
    elif arg == 'mylist':
        derp = []
        for i in _dict['inventory']['weapons']:
            n = '['
            n+= i+' - '+_dict['inventory']['weapons'][i][0]
            if weapon_dict[i].split()[6] == 'ranged':
                n += ': ammo-'+str(_dict['inventory']['weapons'][i][1])
            n += ']'
            derp.append(n)
        return ', '.join(derp)
                    
def _attack(user, _user, uid, roomname, othervars):
    try: __dict = json.loads(rpg_players[_user])
    except: return 'you are not registered yet'
    try:  _dict = json.loads(rpg_players[user])
    except: return 'they are not registered yet'
    try: _title = __dict['title']+ ', '
    except: _title = ''
    try: title = _dict['title']
    except: title = user
    if __dict['status']['health'] < 1:
        return _title+'you are dead. you cannot attack'
    if _dict['status']['health'] < 1:
        return _title+tile+' is dead. you cannot attack'
    for i in __dict['inventory']['weapons']:
        _i = __dict['inventory']['weapons'][i]
        if _i[0] == 'equipped':
            weapon = i
            ammo = _i[1]
            break
    if ammo <= 0: return _title+'you are out of ammo'
    _stats = weapon_dict[weapon].split()
    base_damage = int(_stats[1])
    attack_rate = float(_stats[2])*5
    wtype = _stats[6]
    if attack_rate > 10000: attack_rate = 10000
    timeout = time.time() - __dict['status']['attack_timeout']
    if timeout < attack_rate:
        return _title+'you find yourself unable to attack fast enough [%s seconds]' % str(round(attack_rate -  timeout))
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
        _invisibility, val = _dict['status']['effects']['invisibility']
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
        part = round(i * 10000)
        _part = 10000 - part
        part = ['y' for i in range(int(part))]
        _part = ['n' for i in range(int(_part))]
        part = part + _part
        hit = random.choice(part)
        return hit
    if hit_chance(accuracy) == 'n':
        __dict['status']['attack_timeout'] = time.time()
        rpg_players[_user] = json.dumps(__dict)
        rpg_players[user] = json.dumps(_dict)
        calc_level(_user)
        return _title+'you missed!!!'
    if hit_chance(critchance) == 'y':
        crit = True
        max_damage *= 2
    if wtype == 'ranged':
        for i in __dict['inventory']['weapons']:
            _i = __dict['inventory']['weapons'][i]
            if _i[0] == 'equipped':
                _ammo = _i[1]
                ammo -= 1
                if ammo <= 0: ammo = 0
                _i.remove(_ammo)
                _i.append(ammo)        
    min_damage = max_damage * 0.6
    damage = random.randrange(round(min_damage), round(max_damage))
    _dict['status']['health'] -= damage
    level = _dict['status']['level']
    _level = __dict['status']['level']
    _kexp = round(max_health[str(level)]/random.choice([12,11,13]))
    _exp = round(max_health[str(_level)]/random.choice(range(30,35))) 
    if _dict['status']['health'] <= 0:
        _dict['status']['health'] = 0
        killed = True
        _exp += _kexp
        __dict['inventory']['money'] += _kexp*10
    __dict['inventory']['money'] += _exp*10
    __dict['status']['exp'] += _exp
    __dict['status']['attack_timeout'] = time.time()        
    rpg_players[user] = json.dumps(_dict)
    rpg_players[_user] = json.dumps(__dict)
    calc_level(_user)
    ret = _title+'you attacked ' + title + ' for ' + str(damage)+' damage. their health: '+ str(_dict['status']['health'])
    if crit == True: ret = ret + ': critical hit!!!'
    if killed == True: ret = ret + ': '+title+' was killed'
    return ret

def calc_level(user):
    _dict = json.loads(rpg_players[user])
    exp = _dict['status']['exp']
    _exp = max_health[str(_dict['status']['level'])]
    while True:
        if exp > _exp:
            _left = exp - _exp
            _dict = json.loads(rpg_players[user])
            _exp = max_health[str(_dict['status']['level'])]
            exp -= _exp
            _dict['status']['exp'] = _left
            if _dict['status']['level'] >= 100:
                _dict['status']['level'] = 100
            else:
                _dict['status']['level'] += 1
            level = _dict['status']['level']
            _health = max_health[str(level)]
            _dict['status']['health'] = _health
            if _dict['status']['accuracy'] >= 1:
                _dict['status']['accuracy'] = 1
            else: _dict['status']['accuracy'] += 0.0025
            rpg_players[user] = json.dumps(_dict)
        else: break
    dumprpg()

def _propose(arg, _user, uid, roomname, othervars):
    try:
        arg, user = arg.split()
        _dict = json.loads(rpg_players[user])
        __dict = json.loads(rpg_players[_user])
        try: _title = __dict['title']+ ', '
        except: _title = ''
        try: title = _dict['title']
        except: title = user
        if arg == 'to':
            proposed = []
            try:
                _ret = _dict['status']['marriage']['proposed']
                proposed += _ret
            except:
                pass
            try:
                ret = _dict['status']['marriage']['married']
                try: ret = rpg_players[ret]['title']
                except: ret = ret
                return  title+'is already married to ' + ret
            except:
                __dict['inventory']['items']['wedding rings']
                proposed.append(_user)
                _dict['status']['marriage']['proposed'] = list(set(proposed))
                try:
                    ret = __dict['status']['marriage']['proposing']
                    try: ret = rpg_players[ret]['title']
                    except: ret = ret
                    return _title+'you are already proposing to ' + ret
                except:
                    __dict['status']['marriage']['proposing'] = user
                    rpg_players[user] = json.dumps(_dict)
                    rpg_players[_user] = json.dumps(__dict)
                    calc_level(_user)
                    return _title+'you have proposed to ' + title
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
                _dict['status']['exp'] += 5000
                __dict['status']['exp'] += 5000
                rpg_players[user] = json.dumps(_dict)
                rpg_players[_user] = json.dumps(__dict)
                calc_level(_user)
                calc_level(user)
                return _title+'you are now married to ' + title
            else: return title+' has not proposed to you'
    except:
        return 'not vallid'

def _rpgstats(user, _user, uid, roomname, othervars):
    user = _user if user == '' else user.lower()
    try:
        rpg_players[user]
    except:
        return 'you/they are not registered yet'
    _dict = json.loads(rpg_players[user])
    rel = _dict['status']['marriage']
    try: _title_ = _dict['title']
    except: _title_ = user
    try:
        proposed_to = rel['proposed']
        _i = []
        for i in proposed_to:
            try: title = json.loads(rpg_players[i])['title']
            except: title = i
            _i.append(title)
        _rel = 'proposed to by: ' + ', '.join(_i)
    except:
        _rel = ''
    try:
        married_to = rel['married']
        try: _title = _dict['title']
        except: _title = married_to
        rel = 'married to: ' + _title
    except: rel = 'not married'
    level = str(_dict['status']['level'])
    exp = str(_dict['status']['exp'])
    health = str(_dict['status']['health'])
    clan = _dict['clan']
    money = _dict['inventory']['money']
    if _rel == '': derp = ['name: '+_title_, rel, 'exp: ' + exp, 'level: '+level, 'health: '+health, 'clan: '+clan, 'money: '+str(money)]
    else: derp = ['name: '+_title_, rel, _rel, 'exp: ' + exp, 'level: '+level, 'health: '+health, 'clan: '+clan, 'money: '+str(money)]
    return '<br/><br/><br/>' + '<br/>'.join(derp)
    

def _equip(weapon, user, uid, roomname, othervars):
    try:
        rpg_players[user]
    except:
        return 'you are not registered yet'
    _dict = json.loads(rpg_players[user])
    try: _title = _dict['title'] + ', '
    except: _title = ''
    try:
        for i in _dict['inventory']['weapons']:
            if _dict['inventory']['weapons'][i][0] == 'equipped':
                ammo = _dict['inventory']['weapons'][i][1]
                _dict['inventory']['weapons'][i] = ['unequipped', ammo]
        ammo = _dict['inventory']['weapons'][weapon][1]
        _dict['inventory']['weapons'][weapon] = ['equipped', ammo]
        _dict['status']['exp'] += 5
        rpg_players[user] = json.dumps(_dict)
        calc_level(user)
        return _title+'equipped ' + weapon
    except:
        return _title+'you do not have that weapon'

def _buy(arg, user, uid, roomname, othervars):
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
    try: _title = _dict['title'] + ', '
    except: _title = ''
    if arg == 'weapon':
        i = weapon_dict[_name].split()
        cost = int(i[0])
        need_ammo = i[4]
        ammo = int(i[5])
        if need_ammo == 'yes':
            ammo *= amount        
        _level = int(i[3])
        if _level > level:
            return _title+'your level is not high enough'
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return _title+'you do not have enough money'
        _dict['inventory']['weapons'][_name] = ['unequipped', ammo]
    if arg == 'item':
        i = item_dict[_name].split()
        cost = int(i[-1])
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return _title+'you do not have enough money'
        if _name == 'royal crest':
            _gender = gender(user)
            if _gender == 'him': title = 'lord '+user
            elif _gender == 'her': title = 'lady '+user
            elif _gender == 'them': title = 'your grace: '+user
            _dict['title'] = title
        _dict['inventory']['items'][_name] = 'purchased'
    if arg == 'potion':
        i = potion_dict[_name].split()
        cost = int(i[0])
        cost *= amount
        if money >= cost:
            money -= cost
        else:
            return _title+'you do not have enough money'
        try: _dict['inventory']['potions'][_name] += amount
        except: _dict['inventory']['potions'][_name] = amount
    _dict['inventory']['money'] = money    
    _dict['status']['exp'] += 5*level
    rpg_players[user] = json.dumps(_dict)
    calc_level(user)
    try: _title = _dict['title'] + ', '
    except: _title = ''
    return _title+'you bought ' + str(amount) + ' ' + _name

def dumprpg():
    f = open("rpg.txt", "w")
    for i in rpg_players:
           _dict = json.loads(rpg_players[i])
           f.write(json.dumps([i,_dict])+"\n")                                        
    f.close()
