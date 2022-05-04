# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, PLAYER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load('image/player2/idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0) # 아직 하는 일 없음. 충돌 검사 때 사용해야함

        #graphic setup
        self.import_player_assets()
        self.status = 'idle' # 시작은 오른쪽 방향을 보고 서있기
        self.status_num = 0  #0: idle, 1: run, 2: jump, 3: fall, 4: death, 5: hitted, 6: attack, 7: attack2

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.5

        # move(이동)함수, collision(충돌 검사)함수 등에 사용
        # 플레이어의 이동 방향
        self.direction = 0 # 가만히 서 있기 : 0 / 오른쪽 방향으로 이동시 : 1 / 왼쪽 방향으로 이동시 : -1

        # movement
        self.RUNNING_SPEED = 0.4  # 뛸 때 속도 상수
        self.JUMPMOVE_SPEED = 0.2
        self.speed = self.RUNNING_SPEED # 플레이어 생성시, 걷는 속도로 초기화

        # jumping implementation by event.type == KEYDOWN
        self.jumping = False
        self.Jump_power = -22
        self.jump_value = self.Jump_power
        self.ground_line = self.hitbox.y

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        # 플레이어를 생성할 때 스프라이트 이미지 세트들도 함께 저장한다.
        # 스프라이트 구현할 때 편하게 하기 위해 각 상태의 이름은 이미지 폴더에 실재하는 이름과 같게 바꿨음
        # 더 많은 상태를 추가하고 싶을 경우,
        #   예를들어 'run attack.png' 이미지를 불러오고 싶다면
        #          아래의 self.spr 딕셔너리에
        #               'run attack1':[] 으로 key:item을 추가해준다.
        #          settings.py 에 있는 PLAYER_IMG_INFO 에도
        #                'run attack1': {'idx': 프레임수, 'size': (적절한_사이즈, 적절한_사이즈)} 를 추가로 작성해준다.
        #   어떤 key input이 들어왔을 때 'run attack1' 상태로 만들고싶은지를 고려하여
        #   아래의 input함수에 key 검사를 추가해준다.
        self.spr = {'idle':[], 'idleL':[],
                    'run':[], 'runL':[],
                    'jump':[], 'jumpL':[],
                    'fall':[], 'fallL':[],
                    'death':[], 'deathL':[],
                    'hitted':[], 'hittedL':[],
                    'attack1':[], 'attack1L':[],
                    'attack2':[], 'attack2L':[]
                    }

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(spr_name +'.png',
                                                      PLAYER_IMG_INFO[spr_name]['idx'],
                                                      PLAYER_IMG_INFO[spr_name]['size'])
            if 'L' in spr_name: #왼쪽방향일 경우 이미지 순서 뒤집어서 정렬해주기 -> 애니메이션 구현할 때 편하게 하려고 뒤집어줌.
                self.spr[spr_name].reverse()

    def input(self):
        ## 현재 눌린 키들의 리스트.
        # 여기에 우리가 검사할 키가 들어있는지 확인하고, 있으면 상태를 변경해줌
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            quit_check(event)
            #정지상태
            if self.status_num==0:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    self.direction = 1
                    self.status = 'run'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    self.direction = -1
                    self.status = 'runL'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.status=='idle':
                    self.direction = 0
                    self.status = 'jump'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.status=='idleL':
                    self.direction = 0
                    self.status = 'jumpL'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
            if self.status_num==1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.status=='runL':
                    self.direction = 1
                    self.status = 'run'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.status=='run':
                    self.direction = -1
                    self.status = 'runL'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.status=='run':
                    self.direction = 1
                    self.status = 'jump'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.status=='runL':
                    self.direction = -1
                    self.status = 'jumpL'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
                if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT and self.status=='run':
                    self.direction = 0
                    self.status = 'idle'
                    self.status_num = 0
                    self.speed = self.RUNNING_SPEED
                if event.type == pygame.KEYUP and event.key == pygame.K_LEFT and self.status=='runL':
                    self.direction = 0
                    self.status = 'idleL'
                    self.status_num = 0
                    self.speed = self.RUNNING_SPEED
            if self.status_num==2:
                if keys[pygame.K_RIGHT]:
                    self.direction = 1
                    self.status = 'jump'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
                if keys[pygame.K_LEFT]:
                    self.direction = -1
                    self.status = 'jumpL'
                    self.status_num = 2
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
            if self.status_num==3:
                if keys[pygame.K_RIGHT]:
                    self.direction = 1
                    self.status = 'fall'
                    self.status_num = 3
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
                if keys[pygame.K_LEFT]:
                    self.direction = -1
                    self.status = 'fallL'
                    self.status_num = 3
                    self.jumping = True
                    self.speed = self.JUMPMOVE_SPEED
            """"
            if self.status_num==4:
                if keys[pygame.K_RIGHT]:
                    self.direction = 1
                    self.status = 'run'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
            if self.status_num==5:
                if keys[pygame.K_RIGHT]:
                    self.direction = 1
                    self.status = 'run'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
            if self.status_num==6:
                if keys[pygame.K_RIGHT]:
                    self.direction = 1
                    self.status = 'run'
                    self.status_num = 1
                    self.speed = self.RUNNING_SPEED
            """""
        #quit_check(event)

    def move(self,df):
        # 나중에 플레이어와 사물이 부딪힐 때를 대비해 player.rect 자체가 아니라 좀 더 작은 충돌 범위(hitbox)를 검사한다.
        self.hitbox.x += self.direction * self.speed * df

        # 카메라 하면서 바꿔야 하는 부분. 일단 임시로 화면 width 안 벗어나게 해두었음.
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x + self.rect.width > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width

        if self.jumping:
            self.jump(df)

        # 충돌 검사 (현재 : 왼쪽 오른쪽 벽에 대해서 대충 구현)
        self.collision('horizontal')

    def jump(self,df):
        # 점프할 때의 y값 변경
        self.hitbox.y += self.jump_value
        self.jump_value += 0.05*df
        if self.status == 'jump':
            if self.jump_value >= 0:
                self.status_num = 3
                self.status = 'fall'
        if self.status == 'jumpL':
            if self.jump_value >= 0:
                self.status_num = 3
                self.status = 'fallL'
        if self.jump_value > 15:
            self.jump_value = 15

        #점프에서 착지
        if self.hitbox.y >= self.ground_line:
            self.jumping = False
            self.hitbox.y = self.ground_line
            self.jump_value = self.Jump_power
            self.status_num=0
            self.speed = self.RUNNING_SPEED
            if self.direction == 0:
                if self.status == 'fall':
                    self.status = 'idle'
                if self.status == 'fallL':
                    self.status = 'idleL'
            else:
                if self.status == 'fall':
                    self.status = 'run'
                if self.status == 'fallL':
                    self.status = 'runL'

    def animate(self,df):
        # 플레이어 생성시 준비한 spr 딕셔너리에서
        # self.status에 맞는 스프라이트 세트를 가져온다.
        spr = self.spr[self.status]
        #0: idle, 1: run, 2: jump, 3: fall, 4: death, 5: hitted, 6: attack, 7: attack2
        # 기본적으로 0.33이나, 플레이어가 뛰어가는 동작을 하면 이미지를 더 빠르게 바꾸기 위해 speed를 높게 설정한다.
        if self.status_num==0:
            self.animation_speed = 0.01
        if self.status_num==1:
            self.animation_speed = 0.008
        if self.status_num==2:
            self.animation_speed = 0.02
        if self.status_num==3:
            self.animation_speed = 0.02
        if self.status_num==4:
            self.animation_speed = 0.01
        if self.status_num==5:
            self.animation_speed = 0.01
        if self.status_num==6:
            self.animation_speed = 0.01
        
        # loop over the frame index
        self.frame_index += self.animation_speed*df
        if self.frame_index >= len(spr) and (self.status != 'jump' and self.status != 'jumpL'): # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0 # 다시 처음 이미지로 돌아가기
            
        # once frame index
        if self.frame_index >= len(spr) and (self.status == 'jump' or self.status == 'jumpL'): # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = len(spr)-1 #  마지막 프레임에서 고정

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

    def update(self,df):
        self.input()
        self.move(df)
        self.animate(df)