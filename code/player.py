# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, PLAYER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load('image/player/stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,0) # 아직 하는 일 없음. 충돌 검사 때 사용해야함

        #graphic setup
        self.import_player_assets()
        self.status = 'stand' # 시작은 오른쪽 방향을 보고 서있기

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.25

        # move(이동)함수, collision(충돌 검사)함수 등에 사용
        # 플레이어의 이동 방향
        self.direction = 0 # 가만히 서 있기 : 0 / 오른쪽 방향으로 이동시 : 1 / 왼쪽 방향으로 이동시 : -1

        # movement
        self.speed = 4
        # 가속도 상수는 setting.py로 빼도 될 것 같음.
        self.vspeed_walk = 1 # 걸을 때 가속도 상수
        self.vspeed_running = 1.8 # 뛸 때 가속도 상수
        self.vspeed = self.vspeed_walk  # 플레이어 가속도

        #플레이어 떨어질 때 중력? 그거 해야됨

        # jumping
        self.jumping = False
        self.jump_cooldown = 1000 # jump animation 보고 결정하기
        self.jumping_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        # 플레이어를 생성할 때 스프라이트 이미지 세트들도 함께 저장한다.
        # 스프라이트 구현할 때 편하게 하기 위해 각 상태의 이름은 이미지 폴더에 실재하는 이름과 같게 바꿨음
        # 더 많은 상태를 추가하고 싶을 경우,
        #   예를들어 'running attack.png' 이미지를 불러오고 싶다면
        #          아래의 self.spr 딕셔너리에
        #               'running attack':[] 으로 key:item을 추가해준다.
        #          settings.py 에 있는 PLAYER_IMG_INFO 에도
        #                'running attack': {'idx': 프레임수, 'size': (적절한_사이즈, 적절한_사이즈)} 를 추가로 작성해준다.
        #   어떤 key input이 들어왔을 때 'running attack' 상태로 만들고싶은지를 고려하여
        #   아래의 input함수에 key 검사를 추가해준다.
        self.spr = {'stand':[], 'standL':[], 'walking':[], 'walkingL':[],
                    'running':[], 'runningL':[], 'jump':[], 'jumpL':[]}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(spr_name +'.png',
                                                      PLAYER_IMG_INFO[spr_name]['idx'],
                                                      PLAYER_IMG_INFO[spr_name]['size'])
            if 'L' in spr_name: #왼쪽방향일 경우 이미지 순서 뒤집어서 정렬해주기 -> 애니메이션 구현할 때 편하게 하려고 뒤집어줌.
                self.spr[spr_name].reverse()

    def input(self):
        if not self.jumping: # jump 할 때는 입력 안 받기. jump 끝나야 입력 받을 수 있음
            ## 현재 눌린 키들의 리스트.
            # 여기에 우리가 검사할 키가 들어있는지 확인하고, 있으면 상태를 변경해줌
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_RIGHT]:
                self.direction = 1
                if keys[pygame.K_z]:
                    self.status = 'running'
                    self.vspeed = self.vspeed_running
                    #print('z pressed')
                else:
                    self.status = 'walking'
                    self.vspeed = self.vspeed_walk

                if keys[pygame.K_SPACE]:
                    self.jumping = True
                    self.jumping_time = pygame.time.get_ticks()
                    self.status = 'jump'

            elif keys[pygame.K_LEFT]:
                self.direction = -1
                if keys[pygame.K_z]:
                    self.status = 'runningL'
                    self.vspeed = self.vspeed_running
                else:
                    self.status = 'walkingL'
                    self.vspeed = self.vspeed_walk

                if keys[pygame.K_SPACE]:
                    self.jumping = True
                    self.jumping_time = pygame.time.get_ticks()
                    self.status = 'jumpL'

            else:
                # stand 일 때 jump는? -> 이미지를 어떻게 할까.
                if keys[pygame.K_SPACE]:
                    print('stand -> jump') #상태 표시만 일단...
                self.direction = 0

    def get_status(self):
        if self.direction == 0:
            if not 'stand' in self.status:
                # 이전 상태가 오른쪽 움직이였으면 'stand'로 상태 변경 or 왼쪽 움직임이었으면 'standL'로 상태 변경
                self.status = 'stand' if not 'L' in self.status else 'standL'

    def move(self, speed):
        # 나중에 플레이어와 사물이 부딪힐 때를 대비해 player.rect 자체가 아니라 좀 더 작은 충돌 범위(hitbox)를 검사한다.
        self.hitbox.x += self.direction * speed * self.vspeed

        # 카메라 하면서 바꿔야 하는 부분. 일단 임시로 화면 안 벗어나게 해두었음.
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x + self.rect.width > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width
        self.collision('horizontal')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # 점프할 때는 self.jump_cooldown 에서 정한 시간만큼은 self.status를 바꿀 수 없다.
        if self.jumping:
            if current_time - self.jumping_time >= self.jump_cooldown:
                self.jumping = False

    def animate(self):
        # 플레이어 생성시 준비한 spr 딕셔너리에서
        # self.status에 맞는 스프라이트 세트를 가져온다.
        spr = self.spr[self.status]

        # 기본적으로 0.33이나, 플레이어가 뛰어가는 동작을 하면 이미지를 더 빠르게 바꾸기 위해 speed를 높게 설정한다.
        self.animation_speed = 0.33 if not 'running' in self.status else 1.0

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(spr):
            self.frame_index = 0
            ## jump할 때 상태 못 바꾸도록 하려고
            ## 현재는 cooldowns 함수 사용했으나 또는 jump 애니메이션 끝날 때 상태 변경해주는 방법도 있음(아래 주석처리된 코드)
            # if self.jumping:
            #     self.jumping = False

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

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)