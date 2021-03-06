# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *
from level import *
from debug import *
from AbyssSpell import *
from BringerSpell import *
from soundManager import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, PLAYER_SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        self.image = pygame.image.load('image/player2/idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect[0]+7*PLAYER_SIZE[0]/16,self.rect[1]+7*PLAYER_SIZE[1]/16,PLAYER_SIZE[0]/8,PLAYER_SIZE[1]/5) #히트박스
        self.healthbar = pygame.Rect(self.rect[0],self.rect[1]+7*PLAYER_SIZE[1]/16,PLAYER_SIZE[0]/3,PLAYER_SIZE[1]/32) # 체력바
        self.manabar = pygame.Rect(self.rect[0],self.rect[1]+7*PLAYER_SIZE[1]/16 + PLAYER_SIZE[1]/32,PLAYER_SIZE[0]/3,PLAYER_SIZE[1]/32) # 마나바

        self.attackBox = pygame.Rect(self.rect[0] , self.rect[1]+PLAYER_SIZE[0]/4,PLAYER_SIZE[0]/3,PLAYER_SIZE[1]/3)  #플레이어 어택박스
        self.isAttack = False
        self.isDead = False

        #scene_num
        self.scene_num = 0

        #spell
        self.spell1 = AbyssSpell((-500, -500), groups, obstacle_sprites)
        self.spell2 = BringerSpell((-500,-500), BRINGER_SPELL_SIZE, groups, obstacle_sprites)

        #몬스터 위치
        self.targetPos = 200.0

        self.attackSound1 = soundManager.load_sound('player_attack1', 'sound/player/player_attack1.wav')
        self.attackSound2 = soundManager.load_sound('player_attack2', 'sound/player/player_attack2.ogg')
        self.hitSound = soundManager.load_sound('player_hit', 'sound/player/player_hit.wav')
        self.deathSound = soundManager.load_sound('player_death', 'sound/player/player_death.mp3')
        self.jumpSound = soundManager.load_sound('player_jump', 'sound/player/player_jump.wav')
        self.landSound = soundManager.load_sound('player_land', 'sound/player/player_landing.wav')
        self.potionSound = soundManager.load_sound('player_potion', 'sound/player/player_potion.wav')
        self.castSound = soundManager.load_sound('player_spell', 'sound/abyss/abyss_attack2.wav')
        self.castSound.set_volume(0.5)
        self.cast2Sound = soundManager.load_sound('player_spell2', 'sound/bringer/bringer_cast.wav')
        self.jumpSound.set_volume(1.0)
        self.landSound.set_volume(0.3)

        #검 공격력
        self.AttackPower = 10
        #마법1 공격력
        self.Spell1AttackPower = 20
        #마법2 공격력
        self.Spell2AttackPower = 30
        #체력
        self.hp = PLAYER_HP
        #마나
        self.mp = PLAYER_MP
        #무적시간
        self.hittedTime = 0

        #현혹걸림(마왕에 의해서)
        self.isdazzle = False

        #쿨타임
        self.missile_CastTime = PLAYER_SPELL1_CASTTIME
        self.missile_CastTimeMax = PLAYER_SPELL1_CASTTIME
        self.thunder_CastTime = PLAYER_SPELL2_CASTTIME
        self.thunder_CastTimeMax = PLAYER_SPELL2_CASTTIME
        self.dazzleTime = 0
        self.dazzleTimeMax = DEVIL_DAZZLE_TIME

        #포션
        self.hp_potion = 1
        self.mp_potion = 1

        #충돌관련 받아올 변수들
        #받아올 몬스터 박스들
        self.monsterHitbox = [0,0,0,0]
        self.monsterAttackbox = [0,0,0,0]
        self.monsterSpellAttackbox = pygame.Rect(0,0,0,0)
        #몬스터가 공격중인가?
        self.monsterisAttack = False
        #몬스터 마법이 공격중인가?
        self.monsterspellisAttack = False
        #몬스터의 공격력
        self.monsterPower = 0

        #낙뢰마법

        #graphic setup
        self.import_player_assets()
        self.status = 'idle' # 시작은 오른쪽 방향을 보고 서있기
        self.status_num = 0  #0: idle, 1: run, 2: jump, 3: fall, 4: attack, 5: attack2, 6: hitted, 7: death, 8:missile, 9:thunder

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.5

        # move(이동)함수, collision(충돌 검사)함수 등에 사용
        # 플레이어의 이동 방향
        self.direction = 0 # 가만히 서 있기 : 0 / 오른쪽 방향으로 이동시 : 1 / 왼쪽 방향으로 이동시 : -1

        # movement
        self.RUNNING_SPEED = 0.4  # 뛸 때 속도 상수
        self.JUMPMOVE_SPEED = 0.3
        self.RUNNINGATTACK_SPEED = 0.2
        self.DASHATTACK_SPEED = 0.8
        self.speed = self.RUNNING_SPEED # 플레이어 생성시, 걷는 속도로 초기화

        # jumping implementation by event.type == KEYDOWN
        self.jumping = False
        self.Jump_power = -1.4
        self.jump_value = self.Jump_power
        self.ground_line = self.hitbox.y

        self.obstacle_sprites = obstacle_sprites

        #카메라받기
        self.CameraOffset = [0,0]
        self.display_surface = pygame.display.get_surface()

    def spell1ON_R(self):
        TargetPos = self.targetPos
        self.spell1.ON_P_R(TargetPos, self.hitbox.center)

    def spell1ON_L(self):
        TargetPos = self.targetPos
        self.spell1.ON_P_L(TargetPos, self.hitbox.center)

    def spell2ON(self):
        TargetPos = self.targetPos
        self.spell2.ON(TargetPos)

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
                    'attack1':[], 'attack1L':[],
                    'attack2':[], 'attack2L':[],
                    'death':[], 'deathL':[],
                    'hitted':[], 'hittedL':[],
                    'cast1':[], 'cast1L':[],
                    'cast2':[], 'cast2L':[]
                    }

        for spr_name in self.spr.keys():
            path = 'image/player2/'
            self.spr[spr_name] = import_sprites_image(path, spr_name +'.png',
                                                      PLAYER_IMG_INFO[spr_name]['idx'],
                                                      PLAYER_IMG_INFO[spr_name]['size'])
            if 'L' in spr_name: #왼쪽방향일 경우 이미지 순서 뒤집어서 정렬해주기 -> 애니메이션 구현할 때 편하게 하려고 뒤집어줌.
                self.spr[spr_name].reverse()

    #플레이어 키이벤트
    def input(self):
        for event in pygame.event.get():
            #아이템사용
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z and self.hp_potion >=1:
                self.hp_potion-=1
                self.hp = PLAYER_HP
                self.potionSound.play()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x and self.mp_potion >=1:
                self.mp_potion-=1
                self.mp = PLAYER_MP
                self.potionSound.play()
        keys = pygame.key.get_pressed()

        #정지상태
        if self.status_num==0:
            if keys[pygame.K_RIGHT]:
                self.control(1,'run',0,1,False,self.RUNNING_SPEED)
            if keys[pygame.K_LEFT]:
                self.control(-1,'runL',0,1,False,self.RUNNING_SPEED)
            if keys[pygame.K_SPACE] and self.status=='idle':
                self.control(0,'jump',0,2,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_SPACE] and self.status=='idleL':
                self.control(0,'jumpL',0,2,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_a] and self.status=='idle':
                self.control(0,'attack1',0,4,False,self.RUNNING_SPEED)
            if keys[pygame.K_a] and self.status=='idleL':
                self.control(0,'attack1L',0,4,False,self.RUNNING_SPEED)
            if keys[pygame.K_s] and self.status=='idle':
                self.control(0,'attack2',0,5,False,self.RUNNING_SPEED)
            if keys[pygame.K_s] and self.status=='idleL':
                self.control(0,'attack2L',0,5,False,self.RUNNING_SPEED)
            #spell1
            if self.scene_num != 0 and keys[pygame.K_q] and self.status=='idle' and self.mp >=PLAYER_SPELL1_MP and self.missile_CastTime >= self.missile_CastTimeMax:
                self.control(0,'cast1',0,8,False,self.RUNNING_SPEED)
                self.spell1ON_R()
                self.mp -= PLAYER_SPELL1_MP
                self.castSound.play()
                self.missile_CastTime = 0.0
            if self.scene_num != 0 and keys[pygame.K_q] and self.status=='idleL' and self.mp >=PLAYER_SPELL1_MP and self.missile_CastTime >= self.missile_CastTimeMax:
                self.control(0,'cast1L',0,8,False,self.RUNNING_SPEED)
                self.spell1ON_L()
                self.mp -= PLAYER_SPELL1_MP
                self.castSound.play()
                self.missile_CastTime = 0.0
            #spell2
            if self.scene_num == 2 and keys[pygame.K_w] and self.status=='idle' and self.mp >=PLAYER_SPELL2_MP and self.thunder_CastTime >= self.thunder_CastTimeMax:
                self.control(0,'cast2',0,9,False,self.RUNNING_SPEED)
                self.spell2ON()
                self.mp -= PLAYER_SPELL2_MP
                self.cast2Sound.play()
                self.thunder_CastTime = 0.0
            if self.scene_num == 2 and keys[pygame.K_w] and self.status=='idleL' and self.mp >=PLAYER_SPELL2_MP and self.thunder_CastTime >= self.thunder_CastTimeMax:
                self.control(0,'cast2L',0,9,False,self.RUNNING_SPEED)
                self.spell2ON()
                self.mp -= PLAYER_SPELL2_MP
                self.cast2Sound.play()
                self.thunder_CastTime = 0.0
        #달리기상태
        if self.status_num==1:
            if keys[pygame.K_RIGHT] and self.status=='runL':
                self.control(1,'run',0,1,False,self.RUNNING_SPEED)
            if keys[pygame.K_LEFT] and self.status=='run':
                self.control(-1,'runL',0,1,False,self.RUNNING_SPEED)
            if keys[pygame.K_SPACE] and self.status=='run':
                self.control(1,'jump',0,2,True,self.JUMPMOVE_SPEED)
                self.jumpSound.play()
            if keys[pygame.K_SPACE] and self.status=='runL':
                self.control(-1,'jumpL',0,2,True,self.JUMPMOVE_SPEED)
                self.jumpSound.play()
            if keys[pygame.K_a] and self.status=='run':
                self.control(0,'attack1',0,4,False,self.RUNNING_SPEED)
            if keys[pygame.K_a] and self.status=='runL':
                self.control(0,'attack1L',0,4,False,self.RUNNING_SPEED)
            if keys[pygame.K_s] and self.status=='run':
                self.control(1,'attack2',0,5,False,self.RUNNINGATTACK_SPEED)
            if keys[pygame.K_s] and self.status=='runL':
                self.control(-1,'attack2L',0,5,False,self.RUNNINGATTACK_SPEED)
            if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and self.status=='run':
                self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
            if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and self.status=='runL':
                self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
        #점프상태
        if self.status_num==2:
            if keys[pygame.K_RIGHT]:
                self.control(1,'jump',0,2,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_LEFT]:
                self.control(-1,'jumpL',0,2,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_s] and self.status=='jump':
                self.control(1,'attack2',0,5,True,self.DASHATTACK_SPEED)
            if keys[pygame.K_s] and self.status=='jumpL':
                self.control(-1,'attack2L',0,5,True,self.DASHATTACK_SPEED)
        #떨어지는상태
        if self.status_num==3:
            if keys[pygame.K_RIGHT]:
                self.control(1,'fall',0,3,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_LEFT]:
                self.control(-1,'fallL',0,3,True,self.JUMPMOVE_SPEED)
            if keys[pygame.K_s] and self.status=='fall':
                self.control(1,'attack2',0,5,True,self.DASHATTACK_SPEED)
            if keys[pygame.K_s] and self.status=='fallL':
                self.control(-1,'attack2L',0,5,True,self.DASHATTACK_SPEED)
        

        #공격1상태, 공격2상태(각각 프레임이 일정수치에 가면 다음 상태로 넘어가도록 해줌)
        self.attack()
        #마법1상태, 마법2상태(각각 프레임이 일정수치에 가면 다음 상태로 넘어가도록 해줌)
        self.spell()
        #피격상태
        self.hitted()
        #사망
        self.dead()
        
    #각종 상태 컨트롤해주는 함수
    def control(self, direction, status, index, num, isjumping, speed):
        self.direction = direction
        self.status = status
        self.frame_index = index
        self.status_num = num
        self.jumping = isjumping
        self.speed = speed

    def move(self,df):
        # 나중에 플레이어와 사물이 부딪힐 때를 대비해 player.rect 자체가 아니라 좀 더 작은 충돌 범위(hitbox)를 검사한다.
        self.hitbox.x += self.direction * self.speed * df

        # # 플레이어가 지정된 화면 밖으로 벗어나지 못하게 함.
        # # 카메라 구현 과정에서 이대로 둘 것인지 obstacle 그룹을 만들어서 경계를 관리할 것인지 결정할 필요가 있음
        if self.hitbox.x < 0:
            self.hitbox.x = 0
        if self.hitbox.x > 2450: # 바닥 이미지 크기 설정할 때 함께 바꿔주던가 해야함
            self.hitbox.x = 2450

        if self.jumping:
            self.jump(df)

        # 충돌 검사 (현재 : 왼쪽 오른쪽 벽에 대해서 대충 구현)
        self.collision('horizontal')
    
    #공격상태, 공격상태에서 어택박스 크기 조절까지, 프레임끝나면 행동 변경
    def attack(self):
        if self.status_num == 4:
            if self.status == 'attack1':
                self.attackBox.x = self.hitbox.x
                self.attackBox.width = PLAYER_SIZE[0]/3
                self.attackBox.height = PLAYER_SIZE[1]/2
                if self.frame_index == 6:
                    self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
            if self.status == 'attack1L':
                self.attackBox.x = self.hitbox.x - PLAYER_SIZE[0] / 5
                self.attackBox.width = PLAYER_SIZE[0]/3
                self.attackBox.height = PLAYER_SIZE[1]/2
                if self.frame_index == 6:
                    self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
            self.attackSound1.play()

        elif self.status_num == 5:
            if self.status == 'attack2':
                self.attackBox.x = self.hitbox.x
                self.attackBox.width = PLAYER_SIZE[0]*3/5
                self.attackBox.height = PLAYER_SIZE[1]/2
                if self.frame_index == 6:
                    self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
            if self.status == 'attack2L':
                self.attackBox.x = self.hitbox.x - PLAYER_SIZE[0] / 2
                self.attackBox.width = PLAYER_SIZE[0]*3/5
                self.attackBox.height = PLAYER_SIZE[1]/2
                if self.frame_index == 6:
                    self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
            if self.frame_index >=2 and self.frame_index <3:
                self.attackSound2.play()
    
    def spell(self):
        if self.status_num == 8:
            if self.status == 'cast1' and self.frame_index >= 7:
                self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
            if self.status == 'cast1L' and self.frame_index >= 7:
                self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)

        elif self.status_num == 9:
            if self.status == 'cast2' and self.frame_index >= 8:
                self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
            if self.status == 'cast2L' and self.frame_index >= 8:
                self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)

    def hitted(self):
        if self.status_num == 6:
            if self.frame_index==3:
                if self.jumping == False:
                    if not 'L' in self.status:
                        self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
                    else:
                        self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
                else:
                    if not 'L' in self.status:
                        self.control(0,'fall',0,3,True,self.RUNNING_SPEED)
                    else:
                        self.control(0,'fallL',0,3,True,self.RUNNING_SPEED)
            elif self.frame_index <1:
                self.hitSound.play()
    
    def dead(self):
        if self.status_num == 7:
            if self.frame_index==10:
                self.isDead = True
                self.hp = 0
                self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
                self.hitbox.x = 231
                self.hitbox.y = 551
            elif self.frame_index <1:
                self.deathSound.play()

    def jump(self,df):
        # 점프할 때의 y값 변경
        self.hitbox.y += self.jump_value*df
        self.jump_value += 0.004*df
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
        keys = pygame.key.get_pressed()
        if self.hitbox.y >= self.ground_line:
            self.jumping = False
            self.hitbox.y = self.ground_line
            self.jump_value = self.Jump_power
            self.speed = self.RUNNING_SPEED
            if self.direction == 0:
                if self.status == 'fall':
                    self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
                elif self.status == 'fallL':
                    self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
            else:
                if self.status == 'fall' and keys[pygame.K_RIGHT]:
                    self.control(1,'run',0,1,False,self.RUNNING_SPEED)
                elif self.status == 'fall' and not keys[pygame.K_RIGHT]:
                    self.control(0,'idle',0,0,False,self.RUNNING_SPEED)
                elif self.status == 'fallL' and keys[pygame.K_LEFT]:
                    self.control(-1,'runL',0,1,False,self.RUNNING_SPEED)
                elif self.status == 'fallL' and not keys[pygame.K_LEFT]:
                    self.control(0,'idleL',0,0,False,self.RUNNING_SPEED)
            self.landSound.play()

    def animate(self,df):
        # 플레이어 생성시 준비한 spr 딕셔너리에서
        # self.status에 맞는 스프라이트 세트를 가져온다.
        spr = self.spr[self.status]
        #0: idle, 1: run, 2: jump, 3: fall, 4: attack, 5: attack2, 6: hitted, 7: death
        # 기본적으로 0.33이나, 플레이어가 뛰어가는 동작을 하면 이미지를 더 빠르게 바꾸기 위해 speed를 높게 설정한다.
        if self.status_num==0:
            self.animation_speed = 0.01
        if self.status_num==1:
            self.animation_speed = 0.008
        if self.status_num==2:
            self.animation_speed = 0.01
        if self.status_num==3:
            self.animation_speed = 0.01
        if self.status_num==4:
            self.animation_speed = 0.015
        if self.status_num==5:
            self.animation_speed = 0.007
        if self.status_num==6:
            self.animation_speed = 0.007
        if self.status_num==7:
            self.animation_speed = 0.007
        
        # loop over the frame index
        self.frame_index += self.animation_speed*df
        if self.frame_index >= len(spr) and (self.status != 'jump' and self.status != 'jumpL'): # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0 # 다시 처음 이미지로 돌아가기
            
        # once frame index
        if self.frame_index >= len(spr)-1 and (self.status == 'jump' or self.status == 'jumpL' or self.status == 'attack1' or self.status == 'attack1L'
                                              or self.status == 'attack2' or self.status == 'attack2L' or self.status == 'hitted' or self.status == 'hittedL'
                                              or self.status == 'death' or self.status == 'deathL'): # 스프라이트 마지막 이미지까지 보여준 뒤
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

    def set_pos(self, pos): # 장면 바뀔 때 위치 초기화하는 함수
        self.rect.topleft = pos
        self.hitbox = pygame.Rect(self.rect[0]+7*PLAYER_SIZE[0]/16,self.rect[1]+7*PLAYER_SIZE[1]/16,PLAYER_SIZE[0]/8,PLAYER_SIZE[1]/5)

    def set_state_ini(self):
        self.status = 'idle'  # 시작은 오른쪽 방향을 보고 서있기
        self.status_num = 0  # 0: idle, 1: run, 2: jump, 3: fall, 4: attack, 5: attack2, 6: hitted, 7: death
        self.set_pos(PLAYER_COOR_ini)

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

    def update(self, df):
        self.input()
        self.move(df)
        self.animate(df)

        #마법 공격 쿨타임
        self.thunder_CastTime += df/ 1000.0
        self.missile_CastTime += df/ 1000.0

        #현혹걸리면
        if self.isdazzle == True:
            self.dazzleTime += df/ 1000.0
            self.RUNNING_SPEED = 0.0  # 뛸 때 속도 상수
            self.JUMPMOVE_SPEED = 0.0
            self.RUNNINGATTACK_SPEED = 0.0
            self.DASHATTACK_SPEED = 0.0
            self.speed = self.RUNNING_SPEED # 플레이어 생성시, 걷는 속도로 초기화

        #현혹걸렸다가 풀림
        if self.isdazzle == True and self.dazzleTime > DEVIL_DAZZLE_TIME:
            self.isdazzle = False
            self.dazzleTime = 0
            self.RUNNING_SPEED = 0.4  # 뛸 때 속도 상수
            self.JUMPMOVE_SPEED = 0.3
            self.RUNNINGATTACK_SPEED = 0.2
            self.DASHATTACK_SPEED = 0.8
            self.speed = self.RUNNING_SPEED # 플레이어 생성시, 걷는 속도로 초기화


        #spell
        self.spell1.CameraOffset = self.CameraOffset
        self.spell1.update(df)

        self.spell2.CameraOffset = self.CameraOffset
        self.spell2.update(df)

        #어택 박스 정보 갱신
        attack_playerhitbox = sub_Coordinate(self.attackBox, (self.CameraOffset[0], self.CameraOffset[1], 0, 0))
        #어택 박스 높이 조절
        attack_playerhitbox[1] = self.hitbox.y - PLAYER_SIZE[1]/4

        self.healthbar.x = self.hitbox.x - PLAYER_SIZE[1]/12;
        self.healthbar.y = self.hitbox.y - PLAYER_SIZE[1]/6;
        self.healthbar[2] = PLAYER_SIZE[0]/3 / PLAYER_HP * self.hp;
        self.manabar.x = self.hitbox.x - PLAYER_SIZE[1]/12;
        self.manabar.y = self.hitbox.y + PLAYER_SIZE[1]/32 - PLAYER_SIZE[1]/6;
        self.manabar[2] = PLAYER_SIZE[0]/3 / PLAYER_MP * self.mp;

        #attack animation notify
        if 'attack' in self.status:
            if(self.frame_index < 6 and self.frame_index > 2):
                self.isAttack = True
            else:
                self.isAttack = False
        #충돌구현
        #몬스터 어택박스, 플레이어 히트박스 충돌시
        if collision_check(self.hitbox,self.monsterAttackbox) and self.monsterisAttack and self.hittedTime < 0 and self.status_num!=8 and self.status_num!=9:
            self.monsterisAttack = False  #같은 공격에 중복 데미지 안입도록
            self.hp -= self.monsterPower
            self.hittedTime = 0.5
            #피격상태
            if self.jumping == True:
                if not 'L' in self.status:
                    self.control(0,'hitted',0,6,True,self.RUNNING_SPEED)
                    self.isAttack = False
                else:
                    self.control(0,'hittedL',0,6,True,self.RUNNING_SPEED)
                    self.isAttack = False
            else:
                if not 'L' in self.status:
                    self.control(0,'hitted',0,6,False,self.RUNNING_SPEED)
                    self.isAttack = False
                else:
                    self.control(0,'hittedL',0,6,False,self.RUNNING_SPEED)
                    self.isAttack = False
        #몬스터 주문 히트박스, 플레이어 히트박스 충돌시
        if collision_check(self.hitbox,self.monsterSpellAttackbox) and self.monsterspellisAttack and self.hittedTime < 0 and self.status_num!=8 and self.status_num!=9:
            self.monsterspellisAttack = False  #같은 스펠에 중복 데미지 안입도록
            self.hp -= self.monsterPower
            self.hittedTime = 0.5
            #피격상태
            if self.jumping == True:
                if not 'L' in self.status:
                    self.control(0,'hitted',0,6,True,self.RUNNING_SPEED)
                    self.isAttack = False
                else:
                    self.control(0,'hittedL',0,6,True,self.RUNNING_SPEED)
                    self.isAttack = False
            else:
                if not 'L' in self.status:
                    self.control(0,'hitted',0,6,False,self.RUNNING_SPEED)
                    self.isAttack = False
                else:
                    self.control(0,'hittedL',0,6,False,self.RUNNING_SPEED)
                    self.isAttack = False
        
        #데미지 사이 시간
        self.hittedTime -= df/ 1000.0

        #사망
        if self.hp <= 0:
            self.hp = PLAYER_HP
            self.hittedTime = 10 #사망시 10초간 무적
            if self.jumping == True:
                if not 'L' in self.status:
                    self.control(0,'death',0,7,True,self.RUNNING_SPEED)
                else:
                    self.control(0,'deathL',0,7,True,self.RUNNING_SPEED)
            else:
                if not 'L' in self.status:
                    self.control(0,'death',0,7,False,self.RUNNING_SPEED)
                else:
                    self.control(0,'deathL',0,7,False,self.RUNNING_SPEED)

    #플레이어 위치 중간값x반환
    def getPlayerMiddle(self):
        return self.hitbox.x+ self.hitbox.width/2

    #몬스터 위치
    def setTargetPos(self, posX):
        self.targetPos = posX

    def getSpell1AttackBox(self):
        return self.spell1.getHitBox() 

    def getSpell2AttackBox(self):
        return self.spell2.getHitBox() 