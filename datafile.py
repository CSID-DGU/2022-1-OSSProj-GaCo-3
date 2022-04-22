 #-*-coding:utf-8-*-

import pygame, os, random

# 파일들 경로 정해줌
DIR_PATH = os.path.dirname(__file__)    # 파일 위치
DIR_IMAGE = os.path.join(DIR_PATH, 'image')
DIR_SOUND = os.path.join(DIR_PATH, 'sound')
DIR_FONT = os.path.join(DIR_PATH, 'font')

#윈도우 사이즈 정해줌
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
#배경 색깔 정해줌
BACKGROUND_COLOR = (100,100,100)

objects = [] #오브젝트 리스트
enemys = [] #적 오브젝트 리스트

# 스프라이트 시트 클래스 
class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index,size_x,size_y):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):      # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
            image = pygame.Surface((width, height))
            pygame.transform.scale(image,(size_x,size_y))
            image.blit(baseImage, (0, 0), 
                       ((i % max_row) * width, (i // max_col) * height, width, height))
            image.set_colorkey((0, 0, 0))
            self.spr.append(image)

# 스프라이트 세트 생성 함수 
def createSpriteSet(spriteSheet, index_list, index_max = None):
    spr = []

    if index_max == None:
        for index in index_list:
            spr.append(spriteSheet.spr[index])
    else:
        for index in range(index_list, index_max + 1):
            spr.append(spriteSheet.spr[index])

    return spr

# 애니메이션 행동 변경 함수
def change_playerAction(frame, action_var, new_var, frameSpd, new_frameSpd, aniMode, new_aniMode):
    if action_var != new_var:
        action_var = new_var
        frame = 0
        frameSpd = new_frameSpd
        aniMode = new_aniMode

    return frame, action_var, frameSpd, aniMode

# 텍스트 드로우 함수
def draw_text(screen, text, size, color, x, y):
    gameFont = pygame.font.Font(os.path.join(DIR_FONT, DEFAULT_FONT_NAME), size)
    text_surface = gameFont.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (round(x), round(y))
    screen.blit(text_surface, text_rect)
    

    
