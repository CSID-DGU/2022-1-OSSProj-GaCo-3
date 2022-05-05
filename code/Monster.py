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

        # move(이동)함수, collision(충돌 검사)함수 등에 사용
        # 플레이어의 이동 방향
        self.direction = -1 # 가만히 서 있기 : 0 / 오른쪽 방향으로 이동시 : 1 / 왼쪽 방향으로 이동시 : -1

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
        # 나중에 플레이어와 사물이 부딪힐 때를 대비해 player.rect 자체가 아니라 좀 더 작은 충돌 범위(hitbox)를 검사한다.
        
        #self.hitbox.x += self.direction * self.speed

        # 카메라 하면서 바꿔야 하는 부분. 일단 임시로 화면 width 안 벗어나게 해두었음.
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x + self.rect.width > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width

        # if self.jumping:
        #     self.jump()

        # 충돌 검사 (현재 : 왼쪽 오른쪽 벽에 대해서 대충 구현)
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
        # 플레이어 생성시 준비한 spr 딕셔너리에서
        # self.status에 맞는 스프라이트 세트를 가져온다.
        spr = self.spr[self.status]

        # 기본적으로 0.33이나, 플레이어가 뛰어가는 동작을 하면 이미지를 더 빠르게 바꾸기 위해 speed를 높게 설정한다.
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
        # 파이게임은 충돌시에 아래 위 어느 방향에서 충돌했는지 알려주지 않음
        # 따라서 direction값으로 어느 방향으로 충돌검사 할 것인지를 인자로 받고
        # 만약 horizontal이면,
        #   self.direction이 0보다 클 때는 오른쪽으로 움직이다 충돌한 것이므로
        #       self.hitbox의 오른쪽과 방해물의 왼쪽 충돌검사를 한다.
        #   self.direction이 0보다 작을 때는, 왼쪽으로 움직이다 충돌한 것이므로
        #       self.hitbox의 왼쪽과 방해물의 왼쪽 충돌검사를 한다.
        # 충돌할 경우, 방해물을 통과하여 지나가지 못하도록 self.hitbox의 위치를 조정한다.
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #collision occurs while moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

    def weve_value(self):
        # 7시간 강의에서 나왔던 함수
        # 이미지의 투명도를 시간에 따라 조절하여 이미지가 깜빡거리도록 할 수 있음
        # 플레이어가 공격받거나 약해지거나 죽을 때 사용할 수 있을 듯함.
        # 현재 코드에서는 사용하고 있지 않음
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

 