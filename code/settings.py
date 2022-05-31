# -*-coding:utf-8-*-
import pygame
pygame.init()

WIDTH   = 1280 #가로 크기
HEIGHT  = 720 #세로 크기
FPS     = 60

# 게임 장면 이름
GAME_STATES = ['level1', 'level2', 'level3']
# GAME_STATES = ['intro', 'level1', 'level2', 'level3', 'ending']

# font setup
LARGE_FONT = pygame.font.Font('image/font/Thorn Font.ttf', 60)
MENU_FONT = pygame.font.Font('image/font/Thorn Font.ttf', 40)
CONTENT_FONT = pygame.font.Font('image/font/Thorn Font.ttf', 20)

# colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)

# characters hp info
PLAYER_HP   = 100
PLAYER_MP   = 100
ABYSS_HP    = 100
BRINGER_HP  = 150

#Size
PLAYER_SIZE     = (300, 300)
ABYSS_SIZE      = (300, 300)
BRINGER_SIZE     = (420, 279)

# player settings
PLAYER_SPELL1_YCHANGE = 30
PLAYER_SPELL1_MP = 10
PLAYER_SPELL2_MP = 20
PLAYER_SPELL1_CASTTIME = 3.0
PLAYER_SPELL2_CASTTIME = 5.0
PLAYER_COOR_ini = (100, 420) # 플레이어 초기 위치
PLAYER_IMG_INFO = {'idle': {'idx': 11, 'size': PLAYER_SIZE}, 'idleL': {'idx': 11, 'size': PLAYER_SIZE},
                     'run': {'idx': 8, 'size': PLAYER_SIZE}, 'runL': {'idx': 8, 'size': PLAYER_SIZE},
                     'jump': {'idx': 3, 'size': PLAYER_SIZE}, 'jumpL': {'idx': 3, 'size': PLAYER_SIZE},
                     'fall': {'idx': 3, 'size': PLAYER_SIZE}, 'fallL': {'idx': 3, 'size': PLAYER_SIZE},
                     'death': {'idx': 11, 'size': PLAYER_SIZE}, 'deathL': {'idx': 11, 'size': PLAYER_SIZE},
                     'hitted': {'idx': 4, 'size': PLAYER_SIZE}, 'hittedL': {'idx': 4, 'size': PLAYER_SIZE},
                     'attack1': {'idx': 7, 'size': PLAYER_SIZE}, 'attack1L': {'idx': 7, 'size': PLAYER_SIZE},
                     'attack2': {'idx': 7, 'size': PLAYER_SIZE}, 'attack2L': {'idx': 7, 'size': PLAYER_SIZE},
                     'cast1': {'idx': 8, 'size': ABYSS_SIZE}, 'cast1L':{'idx':8, 'size': ABYSS_SIZE},
                     'cast2': {'idx': 9, 'size': BRINGER_SIZE}, 'cast2L': {'idx': 9, 'size': BRINGER_SIZE}
                     }

# monster1 settings - abyss
ABYSS_COOR_ini  = (700, 395)
ABYSS_IMG_INFO  = {'idleL':{'idx':6, 'size': ABYSS_SIZE}, 'idleR':{'idx':6, 'size': ABYSS_SIZE},
                  'runL': {'idx': 8, 'size': ABYSS_SIZE}, 'runR': {'idx': 8, 'size': ABYSS_SIZE},
                  'attack1L': {'idx': 8, 'size': ABYSS_SIZE}, 'attack1R': {'idx': 8, 'size': ABYSS_SIZE},
                  'attack2L': {'idx': 8, 'size': ABYSS_SIZE}, 'attack2R':{'idx':8, 'size': ABYSS_SIZE},
                  'deathL':{'idx': 7, 'size': ABYSS_SIZE}, 'deathR':{'idx': 7, 'size': ABYSS_SIZE},
                  'hurtL': {'idx': 4, 'size': ABYSS_SIZE}, 'hurtR': {'idx': 4, 'size': ABYSS_SIZE} }

# monster2 settings
BRINGER_COOR_ini = (700, 335) # 몬스터2(BRINGER) 초기 위치
BRINGER_IMG_INFO = {'idleL': {'idx': 8, 'size': BRINGER_SIZE}, 'idleR': {'idx': 8, 'size': BRINGER_SIZE},
                     'walkL': {'idx': 8, 'size': BRINGER_SIZE}, 'walkR': {'idx': 8, 'size': BRINGER_SIZE},
                     'attackL': {'idx': 10, 'size': BRINGER_SIZE}, 'attackR': {'idx': 10, 'size': BRINGER_SIZE},
                     'deathL':{'idx': 10, 'size': BRINGER_SIZE}, 'deathR':{'idx': 10, 'size': BRINGER_SIZE}, 
                     'castL': {'idx': 9, 'size': BRINGER_SIZE}, 'castR': {'idx': 9, 'size': BRINGER_SIZE},
                     'hurtL': {'idx': 3, 'size': BRINGER_SIZE}, 'hurtR': {'idx': 3, 'size': BRINGER_SIZE}}

# monster3 settings - Devil
DEVIL_SIZE     = (750, 750)
DEVIL_COOR_ini = (1000, 125) # 몬스터3(Devil) 초기 위치
DEVIL_IMG_INFO = {'idleL': {'idx': 8, 'size': DEVIL_SIZE}, 'idleR': {'idx': 8, 'size': DEVIL_SIZE},
                    'walkL': {'idx': 8, 'size': DEVIL_SIZE}, 'walkR': {'idx': 8, 'size': DEVIL_SIZE},
                    'attack1L': {'idx': 8, 'size': DEVIL_SIZE}, 'attack1R': {'idx': 8, 'size': DEVIL_SIZE},
                    'attack2L':{'idx': 8, 'size': DEVIL_SIZE}, 'attack2R':{'idx': 8, 'size': DEVIL_SIZE}, 
                    'deathL': {'idx': 7, 'size': DEVIL_SIZE}, 'deathR': {'idx': 7, 'size': DEVIL_SIZE},
                    'hurtL': {'idx': 3, 'size': DEVIL_SIZE}, 'hurtR': {'idx': 3, 'size': DEVIL_SIZE}}

# 장면 이미지 정보들
MAP_IMG_INFO = {'intro': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'},
                'level1': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'},
                'level2': {'background': 'image/map/castle.png', 'floor': 'image/map/floor.png'},
                'level3': {'background': 'image/map/boss_background.png', 'floor': 'image/map/boss_background.png'},
                'ending': {'background': 'image/map/background.png', 'floor': 'image/map/new_floor.png'}}

#BGM 정보
BGM_INFO = {'intro':'sound/BGM/Title.ogg' ,
            'level1': 'sound/BGM/Stage1.wav',
            'level2': 'sound/BGM/Stage2.wav',
            'level3':  'sound/BGM/Stage3.mp3',
            'ending': 'sound/BGM/'}
BGM_DEFAULT_VOLUME = 0.5

# monster1 spell settings
ABYSS_SPELL_SIZE = (150, 150)
ABYSS_SPELL_INFO = {'spell': {'idx': 30, 'size': ABYSS_SPELL_SIZE}}

# monster2 spell settings
BRINGER_SPELL_SIZE = (560, 372)
BRINGER_SPELL_INFO = {'spell': {'idx': 16, 'size': BRINGER_SPELL_SIZE}}
