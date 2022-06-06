# -*-coding:utf-8-*-
from random import getstate
import pygame
from settings import *
from support import *
from game import *
from Monster import * 
from level import * 
from debug import *
from BringerSpell import *
from soundManager import *

class Bringer(Monster):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        #초기 모션 지정 후에 부모 생성자 호출
        self.image = pygame.image.load('image/Monster/bringer/idleL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, MONSTER_SIZE)

        super(Bringer, self).__init__(pos, MONSTER_SIZE, groups, obstacle_sprites)

        self.attackSound = soundManager.load_sound('Bringer_attack1', 'sound/bringer/bringer_attack.wav')
        self.hitSound = soundManager.load_sound('Bringer_hit', 'sound/bringer/bringer_hit.wav')
        self.deathSound = soundManager.load_sound('Bringer_death', 'sound/bringer/bringer_death.wav')
        self.castSound = soundManager.load_sound('Bringer_cast', 'sound/bringer/bringer_cast.wav')

        self.IdleTimeMax = 1.5
        self.IdleTime = 0.0

        self.CastTime =0.0
        self.CastTimeMax = 5.0

        self.look_direction = -1

        self.targetPos = 200.0
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect[0] , self.rect[1], MONSTER_SIZE[0]/2, MONSTER_SIZE[1])
        self.OffsetX = MONSTER_SIZE[0]/4

        self.attackBox = pygame.Rect(self.rect[0] , self.rect[1], MONSTER_SIZE[0]/2, MONSTER_SIZE[1])
        self.spell = BringerSpell((-500,-500), BRINGER_SPELL_SIZE, groups, self.obstacle_sprites)
        self.isAttack = False
        self.isDead = False

        # 체력바
        self.healthbar = pygame.Rect(self.rect[0] , self.rect[1], BRINGER_SIZE[0]/2, BRINGER_SIZE[1]/32)

        #공격력
        self.AttackPower = 40
        #체력
        self.hp = BRINGER_HP
        #무적시간
        self.hittedTime = 0

    def spellON(self):
        TargetPos = self.targetPos
        self.spell.ON(TargetPos)

    def import_monster_assets(self):
        self.spr = {'idleL':[], 'idleR':[],
                    'walkL':[], 'walkR':[],
                    'attackL':[], 'attackR':[],
                    'deathL':[], 'deathR':[],
                    'castL':[], 'castR':[],
                    'hurtL':[], 'hurtR':[]}

        super(Bringer, self).import_monster_assets('image/Monster/bringer/', BRINGER_IMG_INFO, 'R')

    def animate(self, df):
        dt = df

        #피격 모션인 경우 애니메이션이 느리게 재생되도록 줄어든 델타타임을 인자로 넘김
        if 'hurt' in self.status:
            dt /= 2.0
        
        elif 'death' in self.status:
            dt /= 1.5

        super(Bringer, self).animate(dt)

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
                    self.status = 'attackL'
                    self.attackBox.x = self.hitbox.x - BRINGER_SIZE[0] / 4
                else:
                    self.status = 'attackR'
                    self.attackBox.x = self.hitbox.x + BRINGER_SIZE[0] / 4
                
                self.attackSound.stop()
                self.attackSound.play()
                self.direction = 0
        else:
            self.CastTime = 0.0
            if(distanceX) >= 0:
                self.status = 'castL'
            else:
                self.status = 'castR'
            
            self.castSound.play()
            

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

        #체력바 위치 갱신
        self.healthbar.x = self.getHitBox()[0] - BRINGER_SIZE[1]/5;
        self.healthbar.y = self.hitbox.y + BRINGER_SIZE[1]/3;

        self.healthbar[2] = BRINGER_SIZE[0]/2 / BRINGER_HP * self.hp

       #attack animation notify
        if 'attack' in self.status:
            if(self.frame_index < 7 and self.frame_index > 3):
                pygame.draw.rect(self.display_surface,(255, 255, 255), attack_hitbox, 3)
                self.isAttack = True
            else:
                self.isAttack = False

        elif 'cast' in self.status and self.animation_end:
            self.spellON()
           
        
        self.spell.CameraOffset = self.CameraOffset
        self.spell.update(df)

        #충돌
        #플레이어 어택박스, 몬스터 히트박스 충돌시
        if collision_check(self.playerAttackbox,self.getHitBox()) and self.playerisAttack and self.hittedTime < 0:
            self.hp -= self.playerPower
            self.hittedTime = 0.5

            if not 'attack' in self.status and not 'cast' in self.status:
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
        hitbox = self.hitbox.inflate(-BRINGER_SIZE[0]/4, -BRINGER_SIZE[1]/5*2)
        return  sub_Coordinate(hitbox, (0 - self.OffsetX, -BRINGER_SIZE[1]/5, 0, 0))

    def getAttackBox(self):
        return self.attackBox

    def getSpellAttackBox(self):
        return self.spell.getHitBox()                                             

 