# -*-coding:utf-8-*-
import pygame
from settings import *
from support import *
from game import *
from Monster import * 
from level import * 
from debug import *
from BringerSpell import *

class Bringer(Monster):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        #초기 모션 지정 후에 부모 생성자 호출
        self.image = pygame.image.load('image/Monster/bringer/idleL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, MONSTER_SIZE)

        super(Bringer, self).__init__(pos, MONSTER_SIZE, groups, obstacle_sprites)

        self.IdleTimeMax = 1.5
        self.IdleTime = 0.0

        self.CastTime =0.0
        self.CastTimeMax = 5.0

        self.look_direction = -1

        self.targetPos = 200.0
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect[0] , self.rect[1],BRINGER_SIZE[0]/2,BRINGER_SIZE[1])
        self.OffsetX = BRINGER_SIZE[0]/4

        self.attackBox = pygame.Rect(self.rect[0] , self.rect[1],BRINGER_SIZE[0]/2,BRINGER_SIZE[1])
        self.spell = BringerSpell((-500,-500), BRINGER_SPELL_SIZE, groups, self.obstacle_sprites)

    def spellON(self):
        TargetPos = self.targetPos
        self.spell.ON(TargetPos)

    def attack(self):
        self.attackbox = pygame.Rect(self.rect[0] , self.rect[1],BRINGER_SIZE[0]/2,BRINGER_SIZE[1])

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
        #구체적인 AI구현
        self.prev_status = self.status

        origindir = self.look_direction

        #마법 공격 쿨타임
        self.CastTime += df/ 1000.0
       
        if ('hurt' in self.status) | ('death' in self.status) | ('attack' in self.status) | ('cast' in self.status)| ('idle' in self.status):
            if not self.animation_end:
                return
            else:
                if self.look_direction == 1:
                    self.status = 'idleR'
                else:
                    self.status = 'idleL'

        if 'idle' in self.status:
            if self.IdleTime < self.IdleTimeMax:
                self.IdleTime += df
                return
            else:
                self.IdleTime = 0.0

        posX = self.targetPos
        monsterPosX = self.hitbox.topleft[0] - self.OffsetX
        distanceX = monsterPosX - posX

        if self.CastTime < self.CastTimeMax:
            if abs(distanceX) > 80:
                if(distanceX)>=0:
                    self.status = 'walkL'
                    self.direction = -1
                else:
                    self.status = 'walkR'
                    self.direction = 1
            else:
                if(distanceX) >= 0:
                    self.status = 'attackL'
                    self.attackBox.x = self.hitbox.x - BRINGER_SIZE[0] / 4
                else:
                    self.status = 'attackR'
                    self.attackBox.x = self.hitbox.x + BRINGER_SIZE[0] / 4
                self.direction = 0
        else:
            self.CastTime = 0.0
            if(distanceX) >= 0:
                self.status = 'castL'
            else:
                self.status = 'castR'
            

        if 'R' in self.status:
            self.look_direction = 1
        else:
            self.look_direction = -1

        if self.look_direction != origindir:
            if self.look_direction == 1:
                self.hitbox.x += self.scale[0] /2.0
                self.OffsetX = -BRINGER_SIZE[0]/4

            elif self.look_direction == -1:
                self.hitbox.x -= self.scale[0] /2.0
                self.OffsetX = BRINGER_SIZE[0]/4

        if(self.prev_status != self.status):
            self.frame_index = 0 

        super(Bringer, self).AI(df)

    def update(self, df):
        super(Bringer, self).update(df)

        #어택 박스 정보 갱신
        attack_hitbox = sub_Coordinate(self.attackBox, (self.CameraOffset[0], self.CameraOffset[1], 0, 0))               

       #attack animation notify
        if 'attack' in self.status:
            if(self.frame_index < 7 and self.frame_index > 3):
                pygame.draw.rect(self.display_surface,(255, 255, 255), attack_hitbox, 3)
                

        elif 'cast' in self.status and self.animation_end:
            self.spellON()
           
        
        self.spell.CameraOffset = self.CameraOffset
        self.spell.update(df)  

    def setTargetPos(self, posX):
        self.targetPos = posX

 