#-*-coding:utf-8-*-
import pygame, os

#경로 편하게 만들어주기
DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'image')

#플레이어 스테이트


# 스프라이트 시트 클래스 
class SpriteSheet:
    def __init__(self, filename, width, height, max_row, max_col, max_index,size_x,size_y, isWhite = False):
        baseImage = pygame.image.load(os.path.join(DIR_IMAGE, filename)).convert()
        self.spr = []
        self.width = width
        self.height = height

        for i in range(max_index):      # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
            image = pygame.Surface((width, height))
            image.blit(baseImage, (0, 0), ((i % max_row) * width, (i // max_col) * height, width, height))
            image = pygame.transform.scale(image,(size_x,size_y))
            if isWhite:
                image.set_colorkey((0, 0, 0)) #뒤에 흰배경 없앰
            else:
                image.set_colorkey((255, 255, 255)) #뒤에 검은배경 없앰
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
def change_playerAction(frame,new_frame, action_var, new_var, frameSpd, new_frameSpd, aniMode, new_aniMode, loop, new_loop):
    if action_var != new_var:
        action_var = new_var
        frame = new_frame
        frameSpd = new_frameSpd
        aniMode = new_aniMode
        loop = new_loop

    return frame, action_var, frameSpd, aniMode, loop
    
    