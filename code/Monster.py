# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *

class Monster(pygame.sprite.Sprite):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)

        #생성시 처음 이미지 지정 상속받는 각 몬스터 클래스에서 지정해줘야한다.
        # self.image = pygame.image.load('image/Monster/bringer/idleL.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, MONSTER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0)#이미지 사각형의 크기 줄여 HitBox로 사용 
        self.scale = MONSTER_SIZE
        self.display_surface = pygame.display.get_surface()

        #graphic setup
        self.import_monster_assets()
        self.status = 'idleL' # 시작은 왼쪽 방향을 보고 서있기
        self.prev_status = ''

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_time = 0.0
        self.animation_time_max = 0.1
        self.animation_end = False

        self.CameraOffset = [0,0]

        #충돌관련 받아올 변수들
        #받아올 플레이어 박스들
        self.playerHitbox = pygame.Rect(0,0,0,0)
        self.playerAttackbox = pygame.Rect(0,0,0,0)
        self.playerSpell1Attackbox = pygame.Rect(0,0,0,0)
        self.playerSpell2Attackbox = pygame.Rect(0,0,0,0)
        #플레이어가 공격중인가?
        self.playerisAttack = False
        #플레이어가 마법공격중인가?
        self.playerspell1isAttack = False
        self.playerspell2isAttack = False
        #플레이어의 공격력
        self.playerPower = 0
        self.playerSpell1Power = 0
        self.playerSpell2Power = 0

        self.direction = -1

        # movement
        self.speed = 4

        self.space_number = 0

        self.obstacle_sprites = obstacle_sprites

    def import_monster_assets(self, path, MonsterInfo, reverse_key):
        
        #자식 클래스에서 지정 해준 후 호출
        # self.spr = {'idleL':[], 'idleR':[],
        #             'walkL':[], 'walkR':[],
        #             'attackL':[], 'attackR':[],
        #             'deathL':[], 'deathR':[],
        #             'castL':[], 'castR':[],
        #             'hurtL':[], 'hurtR':[]}
        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])
            if reverse_key in spr_name: #오른쪽방향일 경우 이미지 순서 뒤집어서 정렬해주기
                self.spr[spr_name].reverse()

    def get_status(self):
        if self.direction == 0:
            if not 'idle' in self.status:
                # 이전 상태가 오른쪽 움직이였으면 'stand'로 상태 변경 or 왼쪽 움직임이었으면 'standL'로 상태 변경
                self.status = 'idleR' if not 'L' in self.status else 'idleL'

    def move(self):
        if 'walk' in self.status:
            self.hitbox.x += self.direction * self.speed

        if self.hitbox.x < 0:
            self.hitbox.x = 0
        # if self.hitbox.x + self.rect.width > WIDTH:
        #     self.hitbox.x = WIDTH - self.rect.width

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
        self.animation_end = False

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
            self.animation_end = True

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
        self.AI(df)
        self.animate(df)

 