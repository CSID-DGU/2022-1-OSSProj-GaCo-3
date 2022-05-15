# -*-coding:utf-8-*-

WIDTH   = 1280 #가로 크기
HEIGHT  = 720 #세로 크기
FPS     = 60

# player settings
PLAYER_SIZE = (300, 300)
PLAYER_COOR_ini = (100, 420) # 플레이어 초기 위치
PLAYER_IMG_INFO = {'idle': {'idx': 11, 'size': (300, 300)}, 'idleL': {'idx': 11, 'size': (300, 300)},
                     'run': {'idx': 8, 'size': (300, 300)}, 'runL': {'idx': 8, 'size': (300, 300)},
                     'jump': {'idx': 3, 'size': (300, 300)}, 'jumpL': {'idx': 3, 'size': (300, 300)},
                     'fall': {'idx': 3, 'size': (300, 300)}, 'fallL': {'idx': 3, 'size': (300, 300)},
                     'death': {'idx': 11, 'size': (300, 300)}, 'deathL': {'idx': 11, 'size': (300, 300)},
                     'hitted': {'idx': 4, 'size': (300, 300)}, 'hittedL': {'idx': 4, 'size': (300, 300)},
                     'attack1': {'idx': 7, 'size': (300, 300)}, 'attack1L': {'idx': 7, 'size': (300, 300)},
                     'attack2': {'idx': 7, 'size': (300, 300)}, 'attack2L': {'idx': 7, 'size': (300, 300)}
                     }
PLAYER_HP = 100

# monster2 settings
BRINGER_SIZE = (420, 279)
BRINGER_COOR_ini = (700, 335) # 몬스터2(BRINGER) 초기 위치
BRINGER_IMG_INFO = {'idleL': {'idx': 8, 'size': BRINGER_SIZE}, 'idleR': {'idx': 8, 'size': BRINGER_SIZE},
                     'walkL': {'idx': 8, 'size': BRINGER_SIZE}, 'walkR': {'idx': 8, 'size': BRINGER_SIZE},
                     'attackL': {'idx': 10, 'size': BRINGER_SIZE}, 'attackR': {'idx': 10, 'size': BRINGER_SIZE},
                     'deathL':{'idx': 10, 'size': BRINGER_SIZE}, 'deathR':{'idx': 10, 'size': BRINGER_SIZE}, 
                     'castL': {'idx': 9, 'size': BRINGER_SIZE}, 'castR': {'idx': 9, 'size': BRINGER_SIZE},
                     'hurtL': {'idx': 3, 'size': BRINGER_SIZE}, 'hurtR': {'idx': 3, 'size': BRINGER_SIZE}}
BRINGER_HP = 100

# 게임 장면 이름
GAME_STATES = ['intro', 'level1', 'level2', 'level3', 'ending']

# 장면 이미지 정보들
MAP_IMG_INFO = {'intro': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'},
                'level1': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'},
                'level2': {'background': 'image/map/castle.png', 'floor': 'image/map/floor.png'},
                'level3': {'background': 'image/map/boss_background.png', 'floor': 'image/map/boss_background.png'},
                'ending': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'}}

# monster2 spell settings
BRINGER_SPELL_SIZE = (560, 372)
BRINGER_SPELL_INFO = {'spell': {'idx': 16, 'size': BRINGER_SPELL_SIZE}}
