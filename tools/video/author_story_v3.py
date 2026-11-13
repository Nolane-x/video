#!/usr/bin/env python3
"""Cinematic Agincourt shot author v3: dynamic opening, clear staging, reduced foreground occlusion."""
import argparse, json
from pathlib import Path


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def has(text, *terms):
    return any(term in text for term in terms)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    args = ap.parse_args()
    root = Path(args.project)
    story_path = root / 'story' / 'shots.json'
    data = read(story_path)
    shots = data.get('shots', [])
    if not shots:
        raise SystemExit('No draft shots found')
    duration = float(data.get('duration', 0))
    previous_tpl = []
    chapter_last = None

    for i, shot in enumerate(shots):
        line = shot.get('line', '')
        t = line.casefold()
        start = float(shot.get('start', 0))
        end = float(shot.get('end', start + 2))
        phase = start / max(duration, 1)

        if start < 24: chapter = 'cold-open'
        elif has(t, 'harfleur', 'siege', 'port', 'normandy', 'landing', 'fortified wall'): chapter = 'siege'
        elif has(t, 'sommes', 'calais', 'river', 'march north', 'road north', 'crossing', 'food', 'hungry', 'march'): chapter = 'march'
        elif has(t, 'longbow', 'archer', 'archers', 'stake', 'arrow', 'bow'): chapter = 'archery'
        elif has(t, 'armour', 'armor', 'plate', 'joint', 'helmet', 'gauntlet', 'weight', 'mobile', 'mobility'): chapter = 'armour'
        elif has(t, 'estimate', 'chronicle', 'shakespeare', 'records', 'account', 'legend', 'curry'): chapter = 'history'
        elif phase > .91: chapter = 'epilogue'
        elif phase > .28: chapter = 'battle'
        else: chapter = 'campaign'
        chapter_changed = chapter != chapter_last
        chapter_last = chapter

        english = has(t, 'english archer', 'longbow', 'archer', 'english line', 'english soldier', 'henry', 'english force')
        hero = 'englishArcher' if has(t, 'longbow', 'archer', 'bow', 'stake', 'arrow') else ('henry' if 'henry' in t else ('knight15' if english else 'frenchKnight'))
        side = '#a93f37' if english else '#315b8c'
        face = 'determined'
        if has(t, 'sink', 'mud', 'no room', 'crowd', 'crush', 'fall', 'trapped', 'pressure', 'cannot', 'barely', 'exhausted'): face = 'scared'
        elif has(t, 'sick', 'hungry', 'tired', 'exhausting', 'feet hurt', 'disease', 'weak'): face = 'tired'
        elif has(t, 'myth', 'misconception', 'wrong', 'not magic'): face = 'confused'
        elif has(t, 'victory', 'proud', 'courage', 'king'): face = 'determined'
        pose = 'stand'
        if has(t, 'march', 'stepping ashore', 'move forward', 'advance', 'follow the road', 'approach'): pose = 'march'
        elif has(t, 'fall', 'stumble', 'sink', 'knees bend'): pose = 'fall'
        elif has(t, 'press', 'push', 'shoulder', 'hold the line'): pose = 'push'
        elif has(t, 'fight', 'swing', 'combat', 'melee', 'attack', 'charge', 'closes with'): pose = 'lunge'
        elif has(t, 'aim', 'shoot', 'draw the bow', 'arrow'): pose = 'draw' if hero == 'englishArcher' else 'guard'
        elif has(t, 'wait', 'pause', 'think', 'understand'): pose = 'think'

        geography = has(t, 'harfleur', 'normandy', 'sommes', 'calais', 'agincourt', 'river', 'route', 'north')
        numbers = has(t, 'twelve thousand', 'eight thousand', 'five to one', 'estimates', 'twenty to twenty-five', 'kilograms', 'weight', 'five-sixths', 'six thousand')
        records = has(t, 'account', 'shakespeare', 'legend', 'chronicle', 'records', 'written by', 'historian')
        armour = has(t, 'armour', 'armor', 'plate', 'joint', 'helmet', 'gauntlet', 'weight', 'mobile', 'mobility', 'bend', 'kneel')
        formation = has(t, 'formation', 'ranks', 'narrow', 'crowd', 'corridor', 'flanks', 'compressed', 'space begins', 'same corridor', 'rear ranks', 'deployment', 'pressing')
        equipment = has(t, 'bow', 'arrow', 'stake', 'helmet', 'sword', 'shield', 'armour', 'armor', 'plate', 'boots', 'weapon', 'spear', 'horseshoe')
        cavalry = has(t, 'horse', 'cavalry', 'mounted', 'charge', 'rider')
        armies = has(t, 'army', 'archers', 'men-at-arms', 'french force', 'english force', 'troops', 'vanguard')
        personal = has(t, 'you are', 'your boots', 'your sword', 'your armour', 'your horse', 'you breathe', 'you understand', 'you have')

        if numbers:
            tpl = 'board'
        elif records:
            tpl = 'board' if i % 2 == 0 else 'split'
        elif geography:
            tpl = 'map' if i % 3 != 1 else 'scene'
        elif armour and i % 3 != 1:
            tpl = 'xray' if i % 2 == 0 else 'close'
        elif formation:
            tpl = 'top' if i % 2 == 0 else 'plan'
        elif equipment and i % 3 != 2:
            tpl = 'item' if has(t, 'weapon', 'bow', 'arrow', 'stake', 'helmet', 'sword', 'shield') else 'close'
        elif cavalry:
            tpl = 'scene' if i % 2 == 0 else 'army'
        elif armies:
            tpl = 'army'
        elif personal:
            tpl = 'close' if i % 3 == 0 else 'scene'
        else:
            tpl = ['scene', 'close', 'army', 'scene', 'frame'][i % 5]

        if len(previous_tpl) >= 2 and previous_tpl[-1] == tpl and previous_tpl[-2] == tpl:
            alternatives = {
                'scene': ['army', 'close'], 'close': ['scene', 'item'], 'army': ['top', 'scene'],
                'item': ['close', 'scene'], 'map': ['frame', 'scene'], 'board': ['frame', 'split'],
                'frame': ['close', 'scene'], 'top': ['plan', 'army'], 'plan': ['top', 'scene'],
                'xray': ['close', 'item'], 'split': ['board', 'scene']
            }
            tpl = alternatives[tpl][i % len(alternatives[tpl])]

        seed = 31 + i * 17
        if chapter in ('cold-open', 'battle'):
            bg, light = 'mud', 'storm' if chapter == 'cold-open' else ('storm' if phase < .68 else 'dusk')
        elif chapter == 'siege':
            bg, light = ('castle' if i % 2 == 0 else 'field'), 'day'
        elif chapter == 'march':
            bg, light = ('field' if i % 3 else 'mud'), ('golden' if i % 2 else 'dawn')
        elif chapter == 'archery':
            bg, light = 'field', 'golden'
        elif chapter == 'armour':
            bg, light = ('workshop' if i % 2 == 0 else 'castle'), ('dusk' if i % 2 == 0 else 'day')
        elif chapter == 'history':
            bg, light = 'wood', 'dusk'
        else:
            bg, light = 'field', 'dawn'

        bg_opts = {'seed': seed, 'clouds': 2 + (i % 3)}
        if chapter == 'siege':
            bg_opts.update({'castle': True, 'castleX': .74, 'tents': 4, 'flags': [{'color': side, 'charge': 'lion'}]})
        elif chapter == 'march':
            bg_opts.update({'trees': 7 + (i % 4), 'bushes': 5, 'path': True, 'tents': 2 if i % 4 == 0 else 0})
        elif chapter in ('cold-open', 'battle'):
            bg_opts.update({'mud': True, 'wet': True, 'trees': 5 + (i % 3), 'flags': [{'color': side, 'charge': 'lion'}]})
        elif chapter == 'archery':
            bg_opts.update({'trees': 3, 'bushes': 7, 'flags': [{'color': '#a93f37', 'charge': 'cross'}]})
        elif chapter == 'armour':
            bg_opts.update({'window': True, 'torch': True, 'floorY': .83})
        elif chapter == 'epilogue':
            bg_opts.update({'trees': 4, 'bushes': 6, 'sun': True})

        x = [.30, .68, .42, .74, .26][i % 5]
        h = [.48, .54, .44, .58][i % 4]
        camera_moves = ['in', 'left', 'right', 'out', 'up', 'down']
        move = camera_moves[i % len(camera_moves)]
        move_amt = [.060, .075, .050, .080][i % 4]
        bg_common = {'bg': bg, 'time': light, 'bgOpts': bg_opts, 'seed': seed, 'move': move, 'moveAmt': move_amt}

        if tpl == 'map':
            args2 = {
                'view': [-1.0, 48.7, 3.6, 51.5],
                'places': [
                    {'text': 'Harfleur', 'lon': .20, 'lat': 49.50, 'at': 'Harfleur'},
                    {'text': 'Somme', 'lon': 1.95, 'lat': 49.90, 'at': 'Somme'},
                    {'text': 'Calais', 'lon': 1.85, 'lat': 50.95, 'at': 'Calais'},
                    {'text': 'Agincourt', 'lon': 2.14, 'lat': 50.46, 'at': 'Agincourt'}],
                'routes': [{'pts': [[.20,49.50],[1.0,49.7],[1.95,49.90],[1.85,50.95]], 'at': 'march', 'dur': 2.2}],
                'troops': [{'lon': .20, 'lat':49.50, 'side':'blue', 'at':0.3, 'n':18}, {'lon':2.14, 'lat':50.46, 'side':'red', 'at':1.2, 'n':12}]
            }
        elif tpl == 'board':
            vals = [{'label':'ENGLISH','v':.62,'top':'8.5–9k'}, {'label':'FRENCH','v':1.0,'top':'~12k'}]
            if has(t, 'weight', 'kilograms', 'twenty to twenty-five'):
                vals = [{'label':'FIELD HARNESS','v':.82,'top':'20–25 kg'}, {'label':'CARRY LOAD','v':1.0,'top':'varies'}]
            args2 = {'title':'AGINCOURT — ESTIMATES', 'bars':vals, 'mult':{'text':'ESTIMATES DISPUTED','x':.5,'y':.76,'at':.6}, 'curve':[[.13,.68],[.38,.50],[.66,.57],[.86,.36]], 'curveAt':.2}
        elif tpl == 'top':
            args2 = {'ground':{'color':'#7d6042','grass':True},
                     'blocks':[{'x':.13,'y':.51,'w':.24,'h':.48,'rows':9,'cols':9,'side':'red','cell':.021,'seed':seed},
                               {'x':.62,'y':.48,'w':.27,'h':.43,'rows':7,'cols':13 if has(t,'crowd','pressure','compressed','rear ranks') else 9,'side':'blue','cell':.021,'seed':seed+7,'path':[[0,.78,.5],[1.2,.66,.5],[2.5,.57,.5]]}],
                     'arrows':[{'from':[.78,.48],'to':[.46,.48],'at':.3,'w':8,'color':'#c9473a'}, {'from':[.90,.72],'to':[.66,.53],'at':1.0,'w':6,'color':'#315b8c'}],
                     'dust':[{'x':.55,'y':.50,'s':.12,'at':.7},{'x':.48,'y':.58,'s':.08,'at':1.4}], 'fog':[.40,.61]}
        elif tpl == 'plan':
            args2 = {'paper':'parchment', 'blocks':[{'x':.16,'y':.30,'w':.20,'h':.44,'side':'red','cols':7,'rows':11},
                                                   {'x':.64,'y':.28,'w':.20,'h':.46,'side':'blue','cols':7,'rows':12}],
                     'zones':[{'x':.50,'y':.52,'w':.18,'h':.55,'color':'#8b6a49','lw':10,'at':.35,'dur':1.4,'fill':'#8b6a49','fa':.22}],
                     'arrows':[{'from':[.78,.51],'to':[.53,.51],'at':.2,'w':8,'color':'#c9473a'}]}
        elif tpl == 'split':
            args2 = {
                'left': {
                    'bg': 'wood', 'time': 'dusk',
                    'people': [{'preset': 'peasant', 'x': .36, 'y': .93, 'h': .48, 'face': 'worried', 'pose': 'stand'},
                               {'preset': 'lady', 'x': .68, 'y': .93, 'h': .50, 'face': 'sad', 'pose': 'stand'}],
                    'props': [{'kind': 'scroll', 'x': .50, 'y': .72, 's': .22, 'at': .2}]
                },
                'right': {
                    'bg': 'mud' if chapter in ('battle','cold-open') else 'castle',
                    'time': 'storm' if chapter in ('battle','cold-open') else 'day',
                    'people': [{'preset': hero, 'x': .52, 'y': .94, 'h': .64, 'face': face, 'pose': pose,
                                'weapon': 'sword' if hero != 'englishArcher' else 'bow'}],
                    'props': [{'kind': 'flag', 'x': .82, 'y': .78, 's': .32, 'color': side, 'at': .4}]
                },
                'slant': .075
            }
        elif tpl == 'xray':
            args2 = {'subject':'body', 'hit':{'dx':-.22 if i % 2 else .22,'dy':.23,'ang':-.5 if i % 2 else .4,'at':.9}, 'label':'ARTICULATED PLATE — BUILT TO MOVE'}
        elif tpl == 'frame':
            args2 = {'bg':'wood' if i % 2 == 0 else 'castle', 'window':False if i % 2 == 0 else True,
                     'people':[{'preset':'henry' if has(t,'henry','king') else hero,'x':.60 if i % 2 == 0 else .40,'y':.90,'h':.52,'face':face,'pose':'present','weapon':None}],
                     'props':[{'kind':'scroll','x':.25,'y':.70,'s':.32,'at':.25,'anim':'pop'}, {'kind':'torch','x':.83,'y':.70,'s':.23,'at':.5}]}
        elif tpl == 'item':
            thing = 'bow' if has(t,'bow','archer') else ('arrow' if 'arrow' in t else ('stake' if 'stake' in t else ('helmet' if has(t,'helmet','armour','armor','plate','visor') else ('shield' if 'shield' in t else ('spear' if 'spear' in t else 'sword')))))
            args2 = {'bg':bg, 'time':light, 'bgOpts':bg_opts, 'blur':9,
                     'thing':{'kind':thing,'s':.50,'x':.49,'y':.50,'anim':'pop','ang':-0.6 + (i%4)*.28},
                     'props':[{'kind':'arrow','x':.78,'y':.56,'s':.20,'at':.8,'anim':'float'}] if thing in ('bow','stake') else [],
                     'people':[{'preset':hero,'x':.18 if i%2==0 else .82,'y':.92,'h':.36,'face':face,'pose':'present','at':.3}] if i%3==0 else []}
        elif tpl == 'close':
            others=[]
            if chapter in ('battle','cold-open'):
                others=[{'preset':'frenchKnight' if english else 'englishArcher','x':.18 if x>.5 else .82,'y':.50,'R':.13,'face':'scared' if not english else 'determined','visor':'down'}]
            args2 = {**bg_common, 'preset':hero, 'face':face, 'pose':pose, 'x':x, 'y':.48,'R':.22 if i%2 else .26,
                     'look':-.45 if i%2 else .4,'others':others,'fx':[{'kind':'rain','at':0}] if light=='storm' else []}
        elif tpl == 'army':
            args2 = {**bg_common, 'preset':'englishArcher' if chapter=='archery' or english else 'frenchKnight',
                     'enemy':'frenchKnight' if chapter=='archery' or english else 'englishArcher',
                     'rows':5 if i%2==0 else 4,'cols':12 + (i%5),'march':.55,'face':face,
                     'mid':[{'presets':['englishArcher','crossbowman'] if chapter=='archery' or english else ['frenchKnight','frenchKnight2','knight14'],'rows':4,'cols':13,'x0':.04,'x1':.96,'yFront':.98,'yBack':.70,'hFront':.36,'hBack':.12,'seed':seed,'advance':.008 if chapter in ('march','battle') else .003,'march':.65,'flags':[{'col':.16,'row':.72,'kind':'vexillum','color':side}],'flip':bool(i%2)}],
                     'back':[{'presets':['frenchKnight','frenchKnight2','knight14'] if chapter=='archery' or english else ['englishArcher','crossbowman'],'rows':3,'cols':20,'x0':.02,'x1':.98,'yFront':.72,'yBack':.60,'hFront':.10,'hBack':.06,'seed':seed+11,'spread':.72,'advance':.002}]}
        else:
            people=[]
            main={'preset':hero,'x':x,'y':.92,'h':h,'face':face,'pose':pose,'flip':bool(i%2),
                  'visor':'down' if hero=='frenchKnight' and chapter in ('battle','cold-open') else 'none',
                  'weapon':'bow' if hero=='englishArcher' else ('sword' if hero=='frenchKnight' else None),
                  'at':.1,'seed':seed}
            if cavalry:
                main.update({'pose':'ride','horse':{'color':'#85898b','gait':'gallop','h':.84,'riderH':.72,'travel':True},'moveAt':.2,'speed':.85,'dir':-1 if i%2 else 1})
            elif pose in ('march','fall','push','lunge','draw'):
                main.update({'walk':'front' if pose=='march' else False,'to':.40 if x>.5 else .60,'moveAt':.35,'dur':max(1.2,end-start-.35)})
            people.append(main)
            if chapter in ('battle','cold-open') or has(t,'beside', 'behind', 'next to', 'ranks behind'):
                second_preset='frenchKnight' if english else 'englishArcher'
                people.append({'preset':second_preset,'x':.78 if x<.5 else .22,'y':.93,'h':.43,'face':'scared' if chapter=='battle' else 'worried',
                               'pose':'brace' if chapter=='battle' else 'guard','flip':bool(i%2),'at':.45,'seed':seed+3,
                               'weapon':'spear' if chapter=='battle' else 'bow'})
            back_preset='frenchKnight' if english else 'englishArcher'
            back=[{'preset':back_preset,'rows':3 + (i%2),'cols':16 + (i%4),'x0':.01,'x1':.99,'yFront':.78,'yBack':.61,
                   'hFront':.18,'hBack':.07,'seed':seed+5,'spread':.80,'advance':.0025 if chapter=='battle' else .001}] 
            mid=[]
            if chapter in ('battle','cold-open','archery'):
                mid=[{'preset':'englishArcher' if chapter=='archery' else 'frenchKnight','rows':2,'cols':10,'x0':.04,'x1':.96,
                      'yFront':.91,'yBack':.77,'hFront':.28,'hBack':.14,'seed':seed+9,'advance':.004,'march':.35,'flip':bool(i%2)}]
            props=[]
            if has(t,'stake','stakes') or chapter=='archery':
                props += [{'kind':'stake','x':.84,'y':.90,'s':.34,'rot':.22,'at':.2}, {'kind':'stake','x':.66,'y':.95,'s':.28,'rot':.18,'at':.5}]
            if chapter=='siege':
                props += [{'kind':'flag','x':.80,'y':.78,'s':.44,'color':side,'charge':'lion','at':.2}, {'kind':'cart','x':.18,'y':.87,'s':.36,'at':.5}]
            if chapter=='march':
                props += [{'kind':'sack','x':.16,'y':.87,'s':.24,'at':.2}, {'kind':'barrel','x':.82,'y':.88,'s':.24,'at':.5}]
            fx=[]
            if light=='storm': fx.append({'kind':'rain','at':0})
            if chapter in ('battle','cold-open') and cavalry: fx += [{'kind':'dust','x':.72,'y':.83,'s':.18,'at':.35},{'kind':'flash','at':1.2,'color':'#f8e7cc'}]
            if chapter=='archery' and has(t,'arrow','volley','shoot','archer'): fx += [{'kind':'volley','at':.6,'n':24,'x0':.25,'x1':.88,'y0':.28,'y1':.78}]
            args2 = {**bg_common,'people':people,'back':back,'mid':mid,'props':props,'fx':fx,
                     'blur':3.5,'vignette':.18,'shake':.12 if chapter=='battle' and has(t,'impact','collide','crash','falls') else 0}

        # Rebuild the first 30–35 seconds as a deliberate visual sequence:
        # establishing battlefield -> trapped face -> advancing mass -> weapon insert ->
        # opposing line -> armour detail -> overhead compression -> personal stakes -> map.
        if i == 0:
            tpl = 'scene'
            args2 = {
                'bg': 'mud', 'time': 'storm', 'bgOpts': {'seed': 81, 'mud': True, 'wet': True, 'trees': 7, 'clouds': 4,
                    'flags': [{'color': '#315b8c', 'charge': 'fleur'}]},
                'back': [{'presets': ['frenchKnight','frenchKnight2','knight14'], 'rows': 4, 'cols': 18, 'x0': .02, 'x1': .98,
                          'yFront': .78, 'yBack': .58, 'hFront': .23, 'hBack': .065, 'seed': 91, 'spread': .82, 'advance': .003}],
                'mid': [{'presets': ['englishArcher','crossbowman'], 'rows': 2, 'cols': 13, 'x0': .04, 'x1': .96,
                         'yFront': .90, 'yBack': .79, 'hFront': .26, 'hBack': .15, 'seed': 92, 'advance': .004,
                         'flags': [{'col': .15, 'row': .68, 'color': '#a93f37'}]}],
                'people': [{'preset': 'frenchKnight', 'x': .42, 'y': .94, 'h': .68, 'face': 'worried', 'pose': 'march',
                            'walk': 'front', 'weapon': 'sword', 'to': .55, 'from': .34, 'moveAt': .25, 'dur': 2.1, 'seed': 93},
                           {'preset': 'frenchKnight2', 'x': .76, 'y': .96, 'h': .42, 'face': 'scared', 'pose': 'brace', 'seed': 94}],
                'props': [{'kind': 'stake', 'x': .12, 'y': .95, 's': .34, 'rot': .18, 'at': .35},
                          {'kind': 'sword', 'x': .88, 'y': .96, 's': .24, 'rot': -.1, 'at': .7}],
                'fx': [{'kind': 'rain', 'at': 0}, {'kind': 'dust', 'x': .48, 'y': .83, 's': .16, 'at': .9}],
                'move': 'in', 'moveAmt': .075, 'blur': 3, 'vignette': .18
            }
        elif i == 1:
            tpl = 'close'
            args2 = {'bg': 'mud', 'time': 'storm', 'bgOpts': {'seed': 108, 'wet': True, 'trees': 5},
                     'preset': 'frenchKnight', 'face': 'scared', 'pose': 'brace', 'x': .55, 'y': .47, 'R': .27,
                     'look': -.34, 'others': [{'preset': 'frenchKnight2', 'x': .17, 'y': .54, 'R': .13, 'face': 'worried', 'visor': 'down'}],
                     'fx': [{'kind': 'rain', 'at': 0}], 'move': 'in', 'moveAmt': .065}
        elif i == 2:
            tpl = 'army'
            args2 = {'bg': 'mud', 'time': 'storm', 'bgOpts': {'seed': 121, 'mud': True, 'wet': True, 'trees': 4},
                     'preset': 'frenchKnight', 'enemy': 'englishArcher', 'rows': 6, 'cols': 19, 'march': .8, 'face': 'scared',
                     'mid': [{'presets': ['frenchKnight','frenchKnight2','knight14'], 'rows': 5, 'cols': 16, 'x0': .01, 'x1': .99,
                              'yFront': .98, 'yBack': .70, 'hFront': .34, 'hBack': .12, 'seed': 122, 'advance': .011, 'march': .8,
                              'flags': [{'col': .2, 'row': .7, 'color': '#315b8c'}]}],
                     'back': [{'presets': ['englishArcher','crossbowman'], 'rows': 3, 'cols': 22, 'x0': .01, 'x1': .99,
                               'yFront': .71, 'yBack': .60, 'hFront': .12, 'hBack': .06, 'seed': 123, 'spread': .75, 'advance': .003}],
                     'fx': [{'kind': 'rain', 'at': 0}, {'kind': 'dust', 'x': .58, 'y': .82, 's': .18, 'at': .7}],
                     'move': 'left', 'moveAmt': .07}
        elif i == 3:
            tpl = 'item'
            args2 = {'bg': 'mud', 'time': 'storm', 'bgOpts': {'seed': 134, 'wet': True}, 'blur': 8,
                     'thing': {'kind': 'sword', 's': .58, 'x': .49, 'y': .50, 'anim': 'pop', 'ang': -.35},
                     'props': [{'kind': 'shield', 'x': .78, 'y': .72, 's': .28, 'at': .65, 'anim': 'pop'},
                               {'kind': 'helmet', 'x': .20, 'y': .72, 's': .25, 'at': .9, 'anim': 'pop'}],
                     'move': 'right', 'moveAmt': .06}
        elif i == 4:
            tpl = 'scene'
            args2 = {'bg': 'field', 'time': 'dawn', 'bgOpts': {'seed': 147, 'trees': 5, 'bushes': 7, 'clouds': 3,
                     'flags': [{'color': '#a93f37', 'charge': 'cross'}]},
                     'back': [{'presets': ['frenchKnight','frenchKnight2'], 'rows': 3, 'cols': 20, 'x0': .01, 'x1': .99,
                               'yFront': .73, 'yBack': .60, 'hFront': .12, 'hBack': .06, 'seed': 148, 'spread': .78}],
                     'mid': [{'presets': ['englishArcher','crossbowman'], 'rows': 4, 'cols': 15, 'x0': .03, 'x1': .97,
                              'yFront': .99, 'yBack': .72, 'hFront': .31, 'hBack': .13, 'seed': 149, 'advance': .001,
                              'flags': [{'col': .18, 'row': .70, 'color': '#a93f37'}]}],
                     'people': [{'preset': 'englishArcher', 'x': .24, 'y': .95, 'h': .54, 'face': 'determined', 'pose': 'draw', 'seed': 150},
                                {'preset': 'englishArcher', 'x': .78, 'y': .96, 'h': .45, 'face': 'determined', 'pose': 'guard', 'seed': 151}],
                     'props': [{'kind': 'flag', 'x': .86, 'y': .79, 's': .42, 'color': '#a93f37', 'charge': 'cross', 'at': .2}],
                     'move': 'out', 'moveAmt': .065, 'vignette': .15}
        elif i == 5:
            tpl = 'xray'
            args2 = {'subject': 'body', 'hit': {'dx': .28, 'dy': .22, 'ang': -.3, 'at': .75},
                     'label': 'PLATE ARMOUR — ARTICULATED JOINTS'}
        elif i == 6:
            tpl = 'top'
            args2 = {'ground': {'color': '#756345', 'grass': False, 'rocks': True, 'seed': 161},
                     'blocks': [{'x': .20, 'y': .50, 'w': .25, 'h': .55, 'rows': 10, 'cols': 8, 'side': 'red', 'cell': .024, 'seed': 162},
                                {'x': .76, 'y': .50, 'w': .34, 'h': .70, 'rows': 12, 'cols': 15, 'side': 'blue', 'cell': .022, 'seed': 163,
                                 'path': [[0, .70, .50], [.8, .62, .50], [1.8, .55, .50]]}],
                     'arrows': [{'from': [.82, .47], 'to': [.49, .47], 'at': .25, 'w': 10, 'color': '#d14c42'}],
                     'dust': [{'x': .55, 'y': .50, 's': .18, 'at': .7}, {'x': .47, 'y': .62, 's': .12, 'at': 1.2}],
                     'fog': [.40, .64], 'move': 'in', 'moveAmt': .055}
        elif i == 7:
            tpl = 'split'
            args2 = {'left': {'bg': 'wood', 'time': 'dusk',
                              'people': [{'preset': 'peasant', 'x': .35, 'y': .93, 'h': .46, 'face': 'worried'},
                                         {'preset': 'lady', 'x': .67, 'y': .93, 'h': .48, 'face': 'sad'}],
                              'props': [{'kind': 'scroll', 'x': .50, 'y': .76, 's': .24, 'at': .35}]},
                     'right': {'bg': 'field', 'time': 'dawn',
                               'people': [{'preset': 'englishArcher', 'x': .54, 'y': .94, 'h': .62, 'face': 'determined', 'pose': 'guard'}],
                               'props': [{'kind': 'flag', 'x': .82, 'y': .80, 's': .30, 'color': '#a93f37'}]},
                     'slant': .085}
        elif i == 8:
            tpl = 'item'
            args2 = {'bg': 'castle', 'time': 'day', 'bgOpts': {'seed': 174, 'window': True, 'torch': True}, 'blur': 10,
                     'thing': {'kind': 'helmet', 's': .52, 'x': .50, 'y': .48, 'anim': 'pop', 'ang': .2},
                     'props': [{'kind': 'shield', 'x': .80, 'y': .74, 's': .28, 'at': .6, 'anim': 'pop'},
                               {'kind': 'sword', 'x': .20, 'y': .75, 's': .28, 'at': .9, 'anim': 'pop'}],
                     'move': 'in', 'moveAmt': .065}
        elif i == 9:
            tpl = 'army'
            args2 = {'bg': 'field', 'time': 'golden', 'bgOpts': {'seed': 187, 'trees': 4, 'bushes': 8},
                     'preset': 'frenchKnight', 'enemy': 'englishArcher', 'rows': 5, 'cols': 20, 'march': .4,
                     'mid': [{'presets': ['frenchKnight','frenchKnight2','knight14'], 'rows': 5, 'cols': 19, 'x0': .02, 'x1': .98,
                              'yFront': .97, 'yBack': .70, 'hFront': .32, 'hBack': .12, 'seed': 188, 'advance': .004, 'march': .45}],
                     'back': [{'presets': ['englishArcher','crossbowman'], 'rows': 3, 'cols': 22, 'x0': .01, 'x1': .99,
                               'yFront': .72, 'yBack': .59, 'hFront': .11, 'hBack': .06, 'seed': 189, 'spread': .80}],
                     'move': 'right', 'moveAmt': .075}
        elif i == 10:
            tpl = 'scene'
            args2 = {'bg': 'field', 'time': 'golden', 'bgOpts': {'seed': 200, 'trees': 9, 'bushes': 10, 'tents': 3, 'path': True, 'clouds': 4},
                     'back': [{'presets': ['peasant','englishArcher','frenchKnight'], 'rows': 2, 'cols': 14, 'x0': .05, 'x1': .95,
                               'yFront': .73, 'yBack': .62, 'hFront': .11, 'hBack': .06, 'seed': 201, 'spread': .84}],
                     'people': [{'preset': 'frenchKnight', 'x': .50, 'y': .95, 'h': .59, 'face': 'worried', 'pose': 'stand'}],
                     'props': [{'kind': 'cart', 'x': .18, 'y': .90, 's': .34, 'at': .2}, {'kind': 'tent', 'x': .82, 'y': .86, 's': .38, 'at': .3}],
                     'move': 'left', 'moveAmt': .07, 'vignette': .14}
        elif i == 11:
            tpl = 'map'
            args2 = {'view': [-1.0, 48.7, 3.6, 51.5],
                     'places': [{'text': 'Harfleur', 'lon': .20, 'lat': 49.50, 'at': 'Harfleur'},
                                {'text': 'Somme', 'lon': 1.95, 'lat': 49.90, 'at': 'Somme'},
                                {'text': 'Calais', 'lon': 1.85, 'lat': 50.95, 'at': 'Calais'},
                                {'text': 'Agincourt', 'lon': 2.14, 'lat': 50.46, 'at': 'Agincourt'}],
                     'routes': [{'pts': [[.20,49.50],[1.0,49.7],[1.95,49.90],[1.85,50.95]], 'at': 'march', 'dur': 2.2}],
                     'troops': [{'lon': .20, 'lat':49.50, 'side':'blue', 'at':0.3, 'n':18},
                                {'lon':2.14, 'lat':50.46, 'side':'red', 'at':1.2, 'n':12}]}
        shot['tpl'] = tpl
        shot['args'] = args2
        shot['in'] = {'type':'fade' if i==0 or chapter_changed or i%17==0 else 'cut'}
        shot['notes'] = 'DROP' if i == len(shots)-1 else ''
        cues=[]
        if has(t,'arrow','longbow','archer','volley'): cues.append({'name':'arrow_volley','at':.35,'gain':-6})
        if has(t,'sword','fight','combat','men-at-arms','melee'): cues.append({'name':'sword_clash','at':.6,'gain':-7})
        if has(t,'mud','boots','march','sink','ground'): cues.append({'name':'mud_step','at':.25,'gain':-8})
        shot['sfx'] = cues[:2]
        previous_tpl.append(tpl)
        previous_tpl=previous_tpl[-3:]

    data['title']='Agincourt 1415 — The Army That Ran Out of Room'
    data['music']=[
        {'start':0,'end':round(duration*.08,3),'bed':'suspense','gainDb':0},
        {'start':round(duration*.08,3),'end':round(duration*.28,3),'bed':'medieval','gainDb':0},
        {'start':round(duration*.28,3),'end':round(duration*.43,3),'bed':'suspense','gainDb':0},
        {'start':round(duration*.43,3),'end':round(duration*.73,3),'bed':'war','gainDb':0},
        {'start':round(duration*.73,3),'end':round(duration*.95,3),'bed':'somber','gainDb':0},
        {'start':round(duration*.95,3),'end':duration,'bed':'victory','gainDb':0}]
    write(story_path,data)
    config_path=root/'config.json'
    config=read(config_path)
    config.update({'captions':False,'pack':'squire','aspect':'16:9','resolution':'1080p','fps':24,'loudness':-14})
    config['music']={'enabled':True,'gainDb':-10}
    config['sfx']={'enabled':True,'gainDb':-4}
    write(config_path,config)
    from collections import Counter
    counts=Counter(s['tpl'] for s in shots)
    print('SQUIRE V3:',len(shots),'shots;',round(duration,2),'seconds;',dict(counts))

if __name__=='__main__':
    main()
