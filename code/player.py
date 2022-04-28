# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, PLAYER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load('image/player/jumpL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        #self.rect = pygame.Rect(pos[0], pos[1], PLAYER_SIZE[0], PLAYER_SIZE[1])  # 플레이어 히트박스 #차례대로 좌상x, 좌상y, 넓이, 높이
        self.hitbox = self.rect.inflate(0,0) # 아직 변화 없음

        self.frame_index = 0 #entity
        self.animation_speed = 0.15 #entity
        self.direction = 1 #entity # 1-> right side, -1 -> left side, 0 -> stand

        #graphic setup
        self.import_player_assets()
        self.status = 'stand'

        # movement
        self.movement = [0, 0] #direction ? #x
        self.speed = 4
        self.vspeed_walk = 1
        self.vspeed_running = 2.5
        self.vspeed = self.vspeed_walk  # 플레이어 y가속도

        # jumping
        self.jumping = False
        self.jump_cooldown = 1000 # jump animation 보고 결정하기
        self.jumping_time = None

        self.flytime = 0  # 공중에 뜬 시간
        self.state = ['stand', 'walking', 'running', 'jump', 'stand_attack', 'walking_attack', 'running_attack', 'jump_attack']
        self.action = self.state[0]  # 플레이어 현재 행동 #x

        self.obstacle_sprites = obstacle_sprites

        # 플레이어 컨트롤 변수
        self.keyLeft = False
        self.keyRight = False
        self.keyLeft_Run = False
        self.keyRight_Run = False

    def import_player_assets(self):
        #character_path = 'image/player/'
        self.spr = {'stand':[], 'standL':[], 'walking':[], 'walkingL':[],
                    'running':[], 'runningL':[], 'jump':[], 'jumpL':[]}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(spr_name +'.png',
                                                      PLAYER_IMG_INFO[spr_name]['idx'],
                                                      PLAYER_IMG_INFO[spr_name]['size'])

    def input(self):
        if not self.jumping: # jump 할 때는 입력 안 받기. jump 끝나야 입력 받을 수 이씀
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_RIGHT]:
                self.direction = 1
                if keys[pygame.K_z]:
                    self.status = 'running'
                    self.vspeed = self.vspeed_running
                else:
                    self.status = 'walking'
                    self.vspeed = self.vspeed_walk

                if keys[pygame.K_SPACE] and not self.jumping:
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

                if keys[pygame.K_SPACE] and not self.jumping:
                    self.jumping = True
                    self.jumping_time = pygame.time.get_ticks()
                    self.status = 'jumpL'

            else:
                self.direction = 0

        # stand 일 때 jump는?
        # if keys[pygame.K_SPACE]:
        #     self.jumpping = True
        #     self.jumpping_time = pygame.time.get_ticks()
        #     self.status = 'jump' if not 'L' in self.status else 'jumpL'

    def get_status(self):
        if self.direction == 0:
            if not 'stand' in self.status:
                # 이전 상태가 오른쪽 움직이였으면 'stand'로 상태 변경 or 왼쪽 움직임이었으면 'standL'로 상태 변경
                self.status = 'stand' if not 'L' in self.status else 'standL'

    def move(self, speed):
        self.hitbox.x += self.direction * speed * self.vspeed
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x > WIDTH:
            self.hitbox.x = WIDTH - self.rect.width
        self.collision('horizontal')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

    def animate(self):
        # sprite animation
        spr = self.spr[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(spr):
            if self.jumping:
                self.jumping = False
            self.frame_index = 0

        # set the image
        self.image = spr[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

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