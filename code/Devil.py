# -*-coding:utf-8-*-
import random
from random import getstate
import pygame
from settings import *
from support import *
from game import *
from Monster import * 
from level import * 
from debug import *
from Devil_Darkbolt import *
from Devil_Firebomb import *
from soundManager import *

class Devil(Monster):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        #초기 모션 지정 후에 부모 생성자 호출
        self.image = pygame.image.load('image/Monster/Devil/idleL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, MONSTER_SIZE)

        super(Devil, self).__init__(pos, MONSTER_SIZE, groups, obstacle_sprites)
        self.speed = 6

        self.attackSound = soundManager.load_sound('Devil_attack1', 'sound/devil/attack_1.wav')
        self.hitSound = soundManager.load_sound('Devil_hit', 'sound/devil/hurt.wav')
        self.deathSound = soundManager.load_sound('Devil_death', 'sound/devil/death.wav')
        self.attack2Sound = soundManager.load_sound('Devil_attack2', 'sound/devil/attack_2.wav')
        self.castSound = soundManager.load_sound('Devil_cast', 'sound/devil/cast.wav')
        self.castSound.set_volume(1.5)
        self.dazzleSound = soundManager.load_sound('Devil_dazzle', 'sound/devil/dazzle.wav')
        self.dazzleSound.set_volume(3.0)

        self.IdleTimeMax = 1.5
        self.IdleTime = 0.0

        self.CastTime =0.0
        self.CastTimeMax = 5.0

        self.look_direction = -1

        self.targetPos = 200.0
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-MONSTER_SIZE[0]/10*8, - MONSTER_SIZE[1]/10*8)

        self.attackBox = pygame.Rect(self.hitbox[0] , self.hitbox[1] - MONSTER_SIZE[0]/10, MONSTER_SIZE[0]/5*2, MONSTER_SIZE[1]/5*2)
        self.temp = Devil_Darkbolt((-500,-500), DEVIL_DARKBOLT_SIZE, groups, self.obstacle_sprites)
        self.spell = Devil_Darkbolt((-500,-500), DEVIL_DARKBOLT_SIZE, groups, self.obstacle_sprites)
        self.spell2 = Devil_Firebomb((-500,-500), DEVIL_DARKBOLT_SIZE, groups, self.obstacle_sprites)
        self.isAttack = False
        self.isDead = False

        # 체력바
        self.healthbar = pygame.Rect(self.rect[0] , self.rect[1], DEVIL_SIZE[0]/2, DEVIL_SIZE[1]/32)

        #공격력
        self.AttackPower = DEVIL_POWER
        #체력
        self.hp = DEVIL_HP
        #무적시간
        self.hittedTime = 0


    def spellON(self):  #darkbolt
        if self.spell.status == 'firebomb':
            self.temp = self.spell
            self.spell = self.spell2
            self.spell2 = self.temp #swap

        TargetPos = self.targetPos
        self.spell.ON(TargetPos)
        
    def spell2ON(self):   #firebomb
        if self.spell.status == 'darkbolt':
            self.temp = self.spell
            self.spell = self.spell2
            self.spell2 = self.temp #swap

        TargetPos = self.targetPos
        self.spell.ON(TargetPos)

        

    def import_monster_assets(self):
        self.spr = {'idleL':[], 'idleR':[],
                    'walkL':[], 'walkR':[],
                    'attack1L':[], 'attack1R':[],
                    'cast_explosionL':[], 'cast_explosionR':[],
                    'cast_dazzleL':[], 'cast_dazzleR':[],
                    'cast_thunderL':[], 'cast_thunderR':[],
                    'deathL':[], 'deathR':[],
                    'hurtL':[], 'hurtR':[]}

        super(Devil, self).import_monster_assets('image/Monster/Devil/', DEVIL_IMG_INFO, 'L')

        #왼쪽 이미지들만 컬러키 다르게 먹여야해서 일단 이렇게 해둠
        leftList = ['idleL', 'walkL','attack1L','cast_explosionL','cast_dazzleL','cast_thunderL'
                    ,'cast_dazzleR','cast_thunderR','deathL','hurtL']

        for LeftName in leftList:
            spr = self.spr[LeftName]

            for image in spr:
                image.set_colorkey((255,255,255))
            

    def animate(self, df):
        dt = df

        #피격 모션인 경우 애니메이션이 느리게 재생되도록 줄어든 델타타임을 인자로 넘김
        if 'hurt' in self.status:
            dt /= 1.0
        
        elif 'death' in self.status:
            dt /= 4.0

        super(Devil, self).animate(dt)

        spr = self.spr[self.status]
        if 'death' in self.status and self.animation_end:
            #임시적 조치로 죽음 모션의 마지막 프레임일 경우 화면 밖으로 내보낸다.
            self.isDead = True
            self.kill()
            self.hitbox.x = 90000
            return

    def AI(self, df):
        #구체적인 AI구현
        self.prev_status = self.status

        origindir = self.look_direction
        spr = self.spr[self.status]
        if 'death' in self.status and self.animation_end:
            return

        #마법 공격 쿨타임
        self.CastTime += df/ 1000.0

        posX = self.targetPos
        #중앙값으로 거리 계산 하기 위해 사이즈의 일정 비율을 더해준다.
        monsterPosX = self.getHitBox()[0] + self.scale[0]/8
        distanceX = monsterPosX - posX
       
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

        if self.CastTime < self.CastTimeMax:
            if abs(distanceX) > 200:
                if(distanceX)>=0:
                    self.status = 'walkL'
                    self.direction = -1
                else:
                    self.status = 'walkR'
                    self.direction = 1
            else:
                if(distanceX) >= 0:
                    self.status = 'attack1L'
                    self.attackBox.x = self.hitbox.x - DEVIL_SIZE[0] / 4
                else:
                    self.status = 'attack1R'
                    self.attackBox.x = self.hitbox.x + DEVIL_SIZE[0] / 8
                
                self.attack2Sound.stop()
                self.attack2Sound.play()
                self.direction = 0
        else:
            self.CastTime = 0.0
            attacktype = random.randint(0,2)
            if attacktype == 0:
                if(distanceX) >= 0:
                    self.status = 'cast_explosionL'
                else:
                    self.status = 'cast_explosionR'
            if attacktype == 1:
                if(distanceX) >= 0:
                    self.status = 'cast_dazzleL'
                else:
                    self.status = 'cast_dazzleR'
                self.dazzleSound.play()
            if attacktype == 2:
                if(distanceX) >= 0:
                    self.status = 'cast_thunderL'
                else:
                    self.status = 'cast_thunderR'

            self.attack2Sound.play()
            self.castSound.play()

        if 'R' in self.status:
            self.look_direction = 1
        else:
            self.look_direction = -1

        # if self.look_direction != origindir:
        #     if self.look_direction == 1:
        #         self.hitbox.x += self.scale[0] /2.0
        #         self.OffsetX = -BRINGER_SIZE[0]/4

        #     elif self.look_direction == -1:
        #         self.hitbox.x -= self.scale[0] /2.0
        #         self.OffsetX = BRINGER_SIZE[0]/4

        if(self.prev_status != self.status):
            self.frame_index = 0 

        super(Devil, self).AI(df)

    def update(self, df):
        super(Devil, self).update(df)

        #어택 박스 정보 갱신
        attack_hitbox = sub_Coordinate(self.attackBox, (self.CameraOffset[0], self.CameraOffset[1], 0, 0))               

        #체력바 위치 갱신
        self.healthbar.x = self.getHitBox()[0] - DEVIL_SIZE[0]/ 16
        self.healthbar.y = self.hitbox.y

        self.healthbar[2] = DEVIL_SIZE[0]*1/3 / DEVIL_HP * self.hp

       #attack animation notify
        if 'attack1' in self.status:
            if(self.frame_index < 7 and self.frame_index > 3):
                self.isAttack = True
            else:
                self.isAttack = False

        elif 'cast_thunder' in self.status and self.animation_end:
            self.spellON()
        elif 'cast_explosion' in self.status and self.animation_end:
            self.spell2ON()
           
        
        self.spell.CameraOffset = self.CameraOffset
        self.spell.update(df)

        #충돌
        #플레이어 어택박스, 몬스터 히트박스 충돌시
        if collision_check(self.playerAttackbox,self.getHitBox()) and self.playerisAttack and self.hittedTime < 0:
            self.hp -= self.playerPower
            self.hittedTime = 0.5

            if not 'attack' in self.status and not 'cast' in self.status:
                self.frame_index = 0
                if self.look_direction == 1:
                    self.status = 'hurtR'
                else:
                    self.status = 'hurtL'
                self.hitSound.play()
            
            if self.hp <= 0:
                if self.look_direction == 1:
                    self.status = 'deathR'
                else:
                    self.status = 'deathL'
                self.deathSound.play()

        #플레이어 주문1 히트박스, 몬스터 히트박스 충돌시
        if collision_check(self.playerSpell1Attackbox,self.getHitBox()) and self.playerspell1isAttack and self.hittedTime < 0:
            self.playerspell1isAttack = False  #같은 스펠에 중복 데미지 안입도록
            self.hp -= self.playerSpell1Power
            self.hittedTime = 0.5

            if not 'attack' in self.status and not 'cast' in self.status:
                self.frame_index = 0
                if self.look_direction == 1:
                    self.status = 'hurtR'
                else:
                    self.status = 'hurtL'
                self.hitSound.play()
            
            if self.hp <= 0:
                if self.look_direction == 1:
                    self.status = 'deathR'
                else:
                    self.status = 'deathL'
                self.deathSound.play()

        #플레이어 주문2 히트박스, 몬스터 히트박스 충돌시
        if collision_check(self.playerSpell2Attackbox,self.getHitBox()) and self.playerspell2isAttack and self.hittedTime < 0:
            self.playerspell2isAttack = False  #같은 스펠에 중복 데미지 안입도록
            self.hp -= self.playerSpell2Power
            self.hittedTime = 0.5

            if not 'attack' in self.status and not 'cast' in self.status:
                self.frame_index = 0
                if self.look_direction == 1:
                    self.status = 'hurtR'
                else:
                    self.status = 'hurtL'
                self.hitSound.play()
            
            if self.hp <= 0:
                if self.look_direction == 1:
                    self.status = 'deathR'
                else:
                    self.status = 'deathL'
                self.deathSound.play()
        
        #데미지 사이 시간
        self.hittedTime -= df/ 1000.0

    def setTargetPos(self, posX):
        self.targetPos = posX
    
    def getHitBox(self):
        return  sub_Coordinate(self.hitbox, (0 , -DEVIL_SIZE[1]/20, 0, 0))
        #return self.hitbox

    def getAttackBox(self):
        return self.attackBox

    def getSpellAttackBox(self):
        return self.spell.getHitBox()                                             

 