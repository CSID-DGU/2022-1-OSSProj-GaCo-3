# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *

def import_image(path, filename, idx, (size_x, size_y)):
    surface_list = []
    max_col = max_index = max_row = idx
    baseImage = pygame.image.load(path+filename).convert()
    width = baseImage.get_width() / max_col
    height = baseImage.get_height()

    for i in range(max_index):  # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
        image = pygame.Surface((width, height))
        image.blit(baseImage, (0, 0), ((i % max_row) * width, (i // max_col) * height, width, height))
        image = pygame.transform.scale(image, (size_x, size_y))
        image.set_colorkey((0, 0, 0))  # 뒤에 흰배경 없앰
        surface_list.append(image)
    return surface_list

class BringerSpell(pygame.sprite.Sprite):
    def __init__(self, pos, SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        #생성시 처음 이미지 지정 상속받는 각 몬스터 클래스에서 지정해줘야한다.
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('image/Monster/bringer/spell.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-SIZE[0]/4*3, 0)#이미지 사각형의 크기 줄여 HitBox로 사용 
        self.scale = SIZE
        self.CameraOffset = [0,0]
        self.isAttack = False

        #graphic setup
        self.import_assets('image/Monster/bringer/', BRINGER_SPELL_INFO)
        self.status = 'spell'

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_time = 0.0
        self.animation_time_max = 0.1
        self.animation_end = False

        self.SkillON = True

        # movement
        self.speed = 4

        self.space_number = 0

        self.obstacle_sprites = obstacle_sprites

    def import_assets(self, path, MonsterInfo):
        self.spr = {'spell':[]}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])

    def ON(self, posX):
        self.SkillON = True
        self.hitbox.x = posX - self.scale[0]/16
        self.hitbox.y = 250

    def animate(self, df):
        spr = self.spr[self.status]
        # loop over the frame index
        #self.frame_index += self.animation_speed
        # DeltaTime이용해서 애니메이션 프레임 처리 
        #=============================================================

        if self.SkillON == True:
            self.animation_time += df /1000.0

            if self.animation_time >= self.animation_time_max:
                self.animation_time = 0
                self.frame_index += 1
        
        else:
            self.frame_index = 0
        #===============================================================

        if self.frame_index >= len(spr): # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0 # 다시 처음 이미지로 돌아가기
            self.SkillON = False
            self.hitbox.x = -500
            self.hitbox.y = -500

        self.image = spr[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #collision occurs while moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right


    def update(self, df):
        self.animate(df)
        #어택 박스 정보 갱신
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0]/16, -self.scale[1]/3)
        attack_hitbox = sub_Coordinate(attackBox, (self.CameraOffset[0], self.CameraOffset[1]-self.scale[1]/4, 0, 0))
        
        if(self.frame_index < 11 and self.frame_index > 6):
            pygame.draw.rect(self.display_surface,(255, 255, 255), attack_hitbox, 3)
            self.isAttack = True
        else:
            self.isAttack = False

    def getHitBox(self):
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0]/16, -self.scale[1]/3)
        return attackBox


