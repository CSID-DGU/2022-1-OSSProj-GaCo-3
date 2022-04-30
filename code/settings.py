# -*-coding:utf-8-*-

WIDTH   = 1280 #가로 크기
HEIGHT  = 720 #세로 크기
FPS     = 60

# player settings
PLAYER_SIZE = (200, 200)
PLAYER_IMG_INFO = {'stand': {'idx': 5, 'size': (200, 200)}, 'standL': {'idx': 5, 'size': (200, 200)},
                     'walking': {'idx': 8, 'size': (200, 200)}, 'walkingL': {'idx': 8, 'size': (200, 200)},
                     'running': {'idx': 10, 'size': (190, 190)}, 'runningL': {'idx': 10, 'size': (190, 190)},
                     'stand_jump':{'idx': 5, 'size': (200, 200)}, 'standL_jump':{'idx': 5, 'size': (200, 200)}, #stand와 동일한 이미지
                     'jump': {'idx': 12, 'size': (200, 200)}, 'jumpL': {'idx': 12, 'size': (200, 200)}}