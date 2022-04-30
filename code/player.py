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
        self.WALK_SPEED = 4  # 걸을 때 속도 상수
        self.RUNNING_SPEED = 10  # 뛸 때 속도 상수
        self.speed = self.WALK_SPEED # 플레이어 생성시, 걷는 속도로 초기화

        # jumping implementation by event.type == KEYDOWN
        self.jumping = False
        self.jump_status_max = 2
        self.jump_value = -15.0
        self.space_number = 0
        self.jump_start_y = self.hitbox.y

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
        self.spr = {'stand':[], 'standL':[],
                    'walking':[], 'walkingL':[],
                    'running':[], 'runningL':[],
                    'stand_jump':[], 'standL_jump':[],
                    'jump':[], 'jumpL':[]}

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

        #movement input
        if not self.jumping: # jump 하고 있을 때는 다른(왼쪽, 오른쪽, 가속)키 입력은 받지 않는다.
            if keys[pygame.K_RIGHT]:
                self.direction = 1
                if keys[pygame.K_z]:
                    self.status = 'running'
                    self.speed = self.RUNNING_SPEED
                    print('z')
                else:
                    self.status = 'walking'
                    self.speed = self.WALK_SPEED

            elif keys[pygame.K_LEFT]:
                self.direction = -1
                if keys[pygame.K_z]:
                    self.status = 'runningL'
                    self.speed = self.RUNNING_SPEED
                else:
                    self.status = 'walkingL'
                    self.speed = self.WALK_SPEED

            else:
                self.direction = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.space_number += 1 # 스페이스바 누르면 횟수를 증가시킴

                # 스페이스바 수가 우리가 설정한 점프 max 횟수(여기선 2)보다 적을 때만 점프 동작 상태로 변경
                if self.space_number <= self.jump_status_max:
                    # 처음 뛰었을 때 - 1단 점프 / 점프 중이지 않은 상태에서 스페이스바 입력이 들어와야 최초의 점프라고 인식
                    if self.space_number == 1 and not self.jumping:
                        self.jumping = True
                        self.status = 'jump' if not 'L' in self.status else 'jumpL'
                        self.jump_value = -10.0
                        self.frame_index = 3 # 점프할 때 고개 숙이는 부분 제외

                    # 두 번 뛰었을 때 - 2단 점프
                    if self.space_number == 2:
                        self.status = 'jump' if not 'L' in self.status else 'jumpL'
                        self.jump_value = -8.0
                        self.frame_index = 3 # 점프할 때 고개 숙이는 부분 제외

            # 종료 버튼 누를 때 인식 잘 못하는 경우를 위해
            # event 루프 확인할 때는 (for event in pygame.event.get(): 사용시)
            # 종료 버튼 눌렸을 때 종료하라고 중복되지만 써주기
            # support.py 에 종료 조건 확인되면 종료하는 아래 함수 있음.
            quit_check(event)

    def get_status(self):
        if self.direction == 0:
            if not 'stand' in self.status:
                # 이전 상태가 오른쪽 움직이였으면 'stand'로 상태 변경 or 왼쪽 움직임이었으면 'standL'로 상태 변경
                self.status = 'stand' if not 'L' in self.status else 'standL'

    def move(self):
        # 나중에 플레이어와 사물이 부딪힐 때를 대비해 player.rect 자체가 아니라 좀 더 작은 충돌 범위(hitbox)를 검사한다.
        self.hitbox.x += self.direction * self.speed

        # 카메라 하면서 바꿔야 하는 부분. 일단 임시로 화면 width 안 벗어나게 해두었음.
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x + self.rect.width > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width

        if self.jumping:
            self.jump()

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

    def animate(self):
        # 플레이어 생성시 준비한 spr 딕셔너리에서
        # self.status에 맞는 스프라이트 세트를 가져온다.
        spr = self.spr[self.status]

        # 기본적으로 0.33이나, 플레이어가 뛰어가는 동작을 하면 이미지를 더 빠르게 바꾸기 위해 speed를 높게 설정한다.
        self.animation_speed = 0.33 if not 'running' in self.status else 1.0

        # loop over the frame index
        self.frame_index += self.animation_speed
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

    def update(self):
        self.input()
        self.get_status()
        self.move()
        self.animate()