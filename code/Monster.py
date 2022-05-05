# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *

def import_monster_image(path, filename, idx, (size_x, size_y)):
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


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)

        #생성시 처음 이미지 지정 상속받는 각 몬스터 클래스에서 지정해줘야한다.
        # self.image = pygame.image.load('image/Monster/bringer/idleL.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, MONSTER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)#이미지 사각형의 크기 줄여 HitBox로 사용 
        self.scale = MONSTER_SIZE

        #graphic setup
        self.import_monster_assets()
        self.status = 'idleL' # 시작은 왼쪽 방향을 보고 서있기
        self.prev_status = ''

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_time = 0.0
        self.animation_time_max = 0.1

        self.direction = -1

        # movement
        self.speed = 4

        self.space_number = 0

        self.obstacle_sprites = obstacle_sprites

    def import_monster_assets(self, path, MonsterInfo):
        
        #자식 클래스에서 지정 해준 후 호출
        # self.spr = {'idleL':[], 'idleR':[],
        #             'walkL':[], 'walkR':[],
        #             'attackL':[], 'attackR':[],
        #             'deathL':[], 'deathR':[],
        #             'castL':[], 'castR':[],
        #             'hurtL':[], 'hurtR':[]}
        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_monster_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])
            if 'R' in spr_name: #오른쪽방향일 경우 이미지 순서 뒤집어서 정렬해주기
                self.spr[spr_name].reverse()

    def input(self):
        ## 몬스터 디버그 용
        #상태가 이전과 달라졌을 경우 프레임 인덱스 초기화
        if(self.prev_status != self.status):
            self.frame_index = 0        

    def get_status(self):
        if self.direction == 0:
            if not 'idle' in self.status:
                # 이전 상태가 오른쪽 움직이였으면 'stand'로 상태 변경 or 왼쪽 움직임이었으면 'standL'로 상태 변경
                self.status = 'idleR' if not 'L' in self.status else 'idleL'

    def move(self):
        #self.hitbox.x += self.direction * self.speed

        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x + self.rect.width > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width

        self.collision('horizontal')

    def jump(self):
        # 점프할 때의 y값 변경
        self.hitbox.y += self.jump_value
        self.jump_value += 1
        if self.jump_value > 10:
            self.jump_value = 10

        if self.hitbox.y >= self.jump_start_y:
            self.jumping = False
            self.hitbox.y = self.jump_start_y
            self.jump_value = 0
            self.space_number = 0

    def animate(self, df):
        spr = self.spr[self.status]
        self.animation_speed = 0.33 if not 'running' in self.status else 1.0

        # loop over the frame index
        #self.frame_index += self.animation_speed

        # DeltaTime이용해서 애니메이션 프레임 처리 
        #=============================================================
        self.animation_time += df /1000.0

        if self.animation_time >= self.animation_time_max:
            self.animation_time = 0
            self.frame_index += 1
        #===============================================================

        if self.frame_index >= len(spr): # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0 # 다시 처음 이미지로 돌아가기

        # 위의 프레임 인덱스에 따라 플레이어 이미지를 바꿔줌
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

    def weve_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def AI(self, df):
        self.move()

    def update(self, df):
        self.input()
        self.AI(df)
        self.animate(df)

 