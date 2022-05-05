# -*-coding:utf-8-*-
import pygame
from settings import *
from support import *
from game import *
from Monster import * 

class Bringer(Monster):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        #초기 모션 지정 후에 부모 생성자 호출
        self.image = pygame.image.load('image/Monster/bringer/idleL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, MONSTER_SIZE)

        super(Bringer, self).__init__(pos, MONSTER_SIZE, groups, obstacle_sprites)

    def import_monster_assets(self):
        self.spr = {'idleL':[], 'idleR':[],
                    'walkL':[], 'walkR':[],
                    'attackL':[], 'attackR':[],
                    'deathL':[], 'deathR':[],
                    'castL':[], 'castR':[],
                    'hurtL':[], 'hurtR':[]}

        super(Bringer, self).import_monster_assets('image/Monster/bringer/', BRINGER_IMG_INFO)

    def input(self):
        keys = pygame.key.get_pressed()

        #기존 상태 저장
        self.prev_status = self.status
        origindir = self.direction
        #movement input
        if keys[pygame.K_RIGHT]:
            self.direction = 1
            self.status = 'walkR'

        elif keys[pygame.K_LEFT]:
            self.direction = -1
            self.status = 'walkL'

        elif keys[pygame.K_r]:
            if(self.direction == 1):
                self.status = 'attackR'
            else:
                self.status = 'attackL'

        elif keys[pygame.K_q]:
            if(self.direction == 1):
                self.status = 'castR'
            else:
                self.status = 'castL'

        elif keys[pygame.K_w]:
            if(self.direction == 1):
                self.status = 'hurtR'
            else:
                self.status = 'hurtL'
                
        elif keys[pygame.K_e]:
            if(self.direction == 1):
                self.status = 'deathR'
            else:
                self.status = 'deathL'        

        if self.direction != origindir:
            if self.direction == 1:
                self.hitbox.x += self.scale[0] /2.0

            else:
                self.hitbox.x -= self.scale[0] /2.0

        super(Bringer, self).input()

    def get_status(self):
        super(Bringer, self).get_status()

    def move(self):
       super(Bringer, self).move()

    def jump(self):
       super(Bringer, self).jump()

    def animate(self, df):
       super(Bringer, self).animate(df)

    def collision(self, direction):
        super(Bringer, self).collision(direction)

    def AI(self, df):
        super(Bringer, self).AI(df)

    def update(self, df):
       super(Bringer, self).update(df)

 