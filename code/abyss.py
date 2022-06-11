from random import getstate
import pygame
from settings import *
from support import *
from game import *
from Monster import *
from level import *
from debug import *
from AbyssSpell import *
from soundManager import * 

class Abyss(Monster):
    def __init__(self, pos, MONSTER_SIZE, groups, obstacle_sprites):
        self.image = pygame.image.load('image/Monster/abyss/idleL.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, MONSTER_SIZE)

        super().__init__(pos, MONSTER_SIZE, groups, obstacle_sprites)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-220, -200)
        self.OffsetX = self.scale[0] / 4 #??
        self.look_direction = -1

        #사운드 로딩
        self.attackSound1 = soundManager.load_sound('abyss_attack1', 'sound/abyss/abyss_attack1.wav')
        self.attackSound1.set_volume(0.5)
        self.attackSound2 = soundManager.load_sound('abyss_attack2', 'sound/abyss/abyss_attack2.wav')
        self.attackSound2.set_volume(0.5)
        self.hitSound = soundManager.load_sound('abyss_hit', 'sound/abyss/abyss_hit.mp3')
        self.deathSound = soundManager.load_sound('abyss_death', 'sound/abyss/abyss_death.wav')
        self.castSound = soundManager.load_sound('abyss_cast', 'sound/abyss/abyss_spell.wav')

        # 공격
        self.targetPos = 200.0 # 맨 처음에 플레이어 위치를 타겟으로 설정하는 건가?
        self.attackBox = pygame.Rect(self.hitbox.topleft, (MONSTER_SIZE[0]-100, MONSTER_SIZE[1]-20))
        self.attackBox.topright = self.hitbox.topleft
        self.boundary = 150 # 플레이어와의 거리가 이 거리 이상일 경우 몬스터가 플레이어 방향으로 움직임

        self.spell = AbyssSpell((-500, -500), groups, self.obstacle_sprites)
        # spell 공격 상태 및 쿨타임 설정
        self.can_spell = True
        self.spell_time = None
        self.spell_duration_time = 3000 # 3초에 한 번씩 마법 공격 사용

        self.isAttack = False
        self.isDead = False

        # 체력바
        self.healthbar = pygame.Rect(self.rect[0] , self.rect[1], ABYSS_SIZE[0]/2, ABYSS_SIZE[1]/32)

        # attack1 상태 및 쿨타임 설정
        self.can_attack = True
        self.attack_time = None
        self.attack_duration_time = 3000 # 2초에 한 번씩 공격 하기

        self.can_hurt = True # default는 공격당할 수 있는 상태, 공격 당한 직후에는 쿨 타임 찰 동안 공격 못 받게 함
        self.hurt_time = None # 공격 당한 직후 해당 시간을 저장, 루프마다 coolsdown()에서 쿨타임 시간 지났는지 확인하기.
        self.hurt_cooltime = 500 # 무적 시간 == 공격 안 받을 수 있는 시간 - 0.5초

        self.AttackPower = ABYSS_POWER # 공격력
        self.hp = ABYSS_HP # 체력

        self.IdleTimeMax = 1.5
        self.IdleTime = 0.0

    def import_monster_assets(self):
        self.spr = {'idleL':[], 'idleR':[],
                    'runL':[], 'runR':[],
                    'attack1L':[], 'attack1R':[], # 어비스 이미지 이름은 attack1L, attack1R 로 되어있음. 이거 수정하면 됨
                    'attack2L':[], 'attack2R':[], # 스펠 공격 전 준비 모션
                    'deathL':[], 'deathR':[],
                    'hurtL':[], 'hurtR':[]}

        super(Abyss, self).import_monster_assets('image/Monster/abyss/', ABYSS_IMG_INFO, 'L')

    def animate(self, df):
        spr = self.spr[self.status]
        self.animation_end = False

        #피격 모션인 경우 애니메이션이 느리게 재생되도록 줄어든 델타타임을 인자로 넘김
        if 'hurt' in self.status:
            df /= 1.0
        
        elif 'death' in self.status:
            df /= 2.0

        self.animation_time += df / 1000.0

        if self.animation_time >= self.animation_time_max:
            self.animation_time = 0
            self.frame_index += 1

        if self.frame_index >= len(spr):  # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0  # 다시 처음 이미지로 돌아가기
            self.animation_end = True

        # 위의 프레임 인덱스에 따라 플레이어 이미지를 바꿔줌
        self.image = spr[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if 'hurt' in self.status or 'attack1' in self.status: # 피격, 공격 모션일 경우
            if self.frame_index == len(spr) - 1:
                self.status = 'idleL' if 'L' in self.status else 'idleR' # 이미지 재생이 끝나면 idle 상태로 바꾸기.

        if 'attack2' in self.status: # 마법 공격 상태일 경우
            if self.frame_index == len(spr) - 1:
                self.status = 'idleL' if 'L' in self.status else 'idleR' # 이미지 재생이 끝나면 idle 상태로 바꾸기.
                self.spell.ON(self.targetPos, self.attackBox.center)  # 사용자 위치에 마법 사용


        if 'death' in self.status and self.animation_end:
            #임시적 조치로 죽음 모션의 마지막 프레임일 경우 화면 밖으로 내보낸다.
            self.kill_monster()
            return

    def AI(self, df):
        if not self.isDead:
            # 플레이어 hitbox의 x 좌표 : self.targetPos
            # 플레이어와 몬스터의 x좌표 거리가 100이상일 경우, 플레이어 쪽으로 몬스터를 이동시킨다.
            distanceX = self.getHitBox().centerx - self.targetPos # 0보다 크면 플레이어가 왼쪽에 있음, 0보다 작으면 플레이어가 오른쪽에 있음

            # 방향 전환
            if distanceX > 0:  # 플레이어가 왼쪽에 있으면
                self.direction, self.look_direction = -1, -1  # 움직일 때 x값이 작아질 수 있게.
            else:  # 플레이어가 오른쪽에 있으면
                self.direction, self.look_direction = 1, 1  # 움직일 때 x값이 커질 수 있게.

            if ('hurt' in self.status) | ('death' in self.status) | ('attack1' in self.status) | ('attack2' in self.status)| ('idle' in self.status):
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

            if 'attack' not in self.status: # 공격중이지 않을 때
                if abs(distanceX) > self.boundary: # 거리가 멀면 움직이고
                    self.status = 'runL' if self.direction == -1 else 'runR'
                    self.can_attack = True # 거리가 멀어졌다가 다시 가까워졌을 때, 쿨타임 상관 없이 다시 기본공격 할 수 있도록 상태 바꿔줌

                else: # 가까우면 안 움직인다
                    self.status = 'idleL' if self.direction == -1 else 'idleR'
                    # 쿨 타임 주고 기본 공격 사용
                    if self.can_attack:  # 공격 가능 상태일 경우
                        self.attack_time = pygame.time.get_ticks()  # 쿨타임 계산을 위한 공격 시작 시간 저장
                        self.can_attack = False  # 쿨 타임 차기 전까지 공격 못 하도록 can_attack을 False로 변경
                        self.status = 'attack1L' if self.direction == -1 else 'attack1R'  # 방향에 맞게 attack1 상태로 변경
                        self.attackSound1.play()

            # 쿨 타임을 주고 spell 공격 사용
            if self.can_spell:  # 마법 공격 가능 상태일 경우
                self.spell_time = pygame.time.get_ticks()  # 마법 공격 수행 시간 체크
                self.status = 'attack2L' if 'L' in self.status else 'attack2R'  # 마법 공격 상태로 변경
                self.can_spell = False  # 마법 불가능 상태로 변경 -> coodsdown에서 시간 지나면 다시 마법 가능 상태로 변경해줌
                self.attackSound2.play()

    def move(self):
        if 'run' in self.status:
            self.hitbox.x += self.direction * self.speed

        if self.hitbox.x < 0:
            self.hitbox.x = 0

        self.collision('horizontal')

    def update(self, df):
        self.AI(df)
        self.animate(df)
        self.move()
        self.coodsdown()

         #체력바 위치 갱신
        self.healthbar.x = self.getHitBox()[0] - ABYSS_SIZE[1]/10;
        self.healthbar.y = self.hitbox.y - ABYSS_SIZE[1]/12;
        self.healthbar[2] = ABYSS_SIZE[0]/2 / ABYSS_HP * self.hp

        # 어택 박스 정보 갱신
        if self.direction == -1:
            self.attackBox.center = self.hitbox.topleft
        else:
            self.attackBox.center = self.hitbox.topright

        # attack animation notify
        # 애니메이션 프레임에 따라서, 스프라이트의 몇 번째 그림에 정확히 공격 이미지가 생성되고 사라지는지를
        # 공격시 어택박스 생성, isAttack 시그널로 사용하기.
        if 'attack1' in self.status:
            if (self.frame_index < 6 and self.frame_index > 2): # 어비스 공격 스프라이트의 4, 5, 6 에 공격 이미지 있음
                self.isAttack = True
            else:
                self.isAttack = False

        # # attack2를 준비 이미지라고 가정, 해당 스프라이트가 다 재생되면 마법을 사용함.

        self.spell.CameraOffset = self.CameraOffset
        self.spell.update(df)

        if 'death' in self.status and self.animation_end: # 죽음 모션의 마지막 프레임일 경우 죽음 상태로 변경
            self.isDead = True

        # 충돌
        # 플레이어 어택박스, 몬스터 히트박스 충돌 and 몬스터가 피격 가능 상태 and 플레이어가 공격 중일 경우
        if collision_check(self.playerAttackbox,self.getHitBox()) and self.can_hurt and self.playerisAttack and not 'death' in self.status:
            self.hp -= self.playerPower
            self.hurt_time = pygame.time.get_ticks() # 공격 감지 직후 시간 체크. 쿨다운에서 비교할 시간
            self.can_hurt = False # self.coolsdown() 에서 쿨타임 지나면 다시 True로 바꿔줌

            if not 'attack' in self.status: # 몬스터가 공격하고 있지 않을 때만 hurt 모션으로 바꿔줌
                self.frame_index = 0
                self.status = 'hurtR' if self.look_direction == 1 else 'hurtL'
                self.hitSound.play()
                # 플레이어 어택박스가 사라지지 않고 몬스터를 계속 공격하는 현상 발견.
                # 플레이어 어택박스 위치가 바뀌면 hurt상태를 벗어남. -> colission check 방식을 바꿔야하나?
                # 일단은 hurt로 상태 변경하자 마자 플레이어 어택박스 위치를 임의로 화변 밖으로 위치시켜서 해당 현상 해결
                self.playerAttackbox.x = -100

            if self.hp<=0: # hp<=0이하일경우 death상태로 변경
                self.frame_index = 0
                self.status = 'deathR' if self.look_direction == 1 else 'deathL'
                self.deathSound.play()

        #플레이어 주문1 히트박스, 몬스터 히트박스 충돌시
        if collision_check(self.hitbox,self.playerSpell1Attackbox) and self.playerspell1isAttack and self.can_hurt:
            self.playerspell1isAttack = False  #같은 스펠에 중복 데미지 안입도록
            self.hp -= self.playerSpell1Power
            self.hurt_time = pygame.time.get_ticks() # 공격 감지 직후 시간 체크. 쿨다운에서 비교할 시간
            self.can_hurt = False # self.coolsdown() 에서 쿨타임 지나면 다시 True로 바꿔줌

            if not 'attack' in self.status: # 몬스터가 공격하고 있지 않을 때만 hurt 모션으로 바꿔줌
                self.frame_index = 0
                self.status = 'hurtR' if self.look_direction == 1 else 'hurtL'
                self.hitSound.play()
                # 플레이어 어택박스가 사라지지 않고 몬스터를 계속 공격하는 현상 발견.
                # 플레이어 어택박스 위치가 바뀌면 hurt상태를 벗어남. -> colission check 방식을 바꿔야하나?
                # 일단은 hurt로 상태 변경하자 마자 플레이어 어택박스 위치를 임의로 화변 밖으로 위치시켜서 해당 현상 해결
                self.playerAttackbox.x = -100

            if self.hp <= 0: # 몬스터 피가 0이하가 되면 죽음 상태로 변경
                self.frame_index = 0
                self.status = 'deathR' if self.look_direction == 1 else 'deathL'
                self.deathSound.play()

        #플레이어 주문2 히트박스, 몬스터 히트박스 충돌시
        if collision_check(self.hitbox,self.playerSpell2Attackbox) and self.playerspell2isAttack and self.can_hurt:
            self.playerspell2isAttack = False  #같은 스펠에 중복 데미지 안입도록
            self.hp -= self.playerSpell2Power
            self.hurt_time = pygame.time.get_ticks() # 공격 감지 직후 시간 체크. 쿨다운에서 비교할 시간
            self.can_hurt = False # self.coolsdown() 에서 쿨타임 지나면 다시 True로 바꿔줌

            if not 'attack' in self.status: # 몬스터가 공격하고 있지 않을 때만 hurt 모션으로 바꿔줌
                self.frame_index = 0
                self.status = 'hurtR' if self.look_direction == 1 else 'hurtL'
                self.hitSound.play()
                # 플레이어 어택박스가 사라지지 않고 몬스터를 계속 공격하는 현상 발견.
                # 플레이어 어택박스 위치가 바뀌면 hurt상태를 벗어남. -> colission check 방식을 바꿔야하나?
                # 일단은 hurt로 상태 변경하자 마자 플레이어 어택박스 위치를 임의로 화변 밖으로 위치시켜서 해당 현상 해결
                self.playerAttackbox.x = -100

            if self.hp <= 0: # 몬스터 피가 0이하가 되면 죽음 상태로 변경
                self.frame_index = 0
                self.status = 'deathR' if self.look_direction == 1 else 'deathL'
                self.deathSound.play()

    def coodsdown(self):
        current_time = pygame.time.get_ticks()

        if not self.can_hurt: # 공격당해서 can_hurt가 False 됐을 경우, hurt_time과 현재 시간을 비교해서 쿨타임 지나면 다시 hurt 가능 상태로 만들어준다.
            if current_time - self.hurt_time >= self.hurt_cooltime:
                self.can_hurt = True # 다시 피격 가능상태로 바꿔준다.

        if not self.can_attack: # 공격 시작 후, can_attack이 False가 됐을 경우
            if current_time - self.attack_time >= self.attack_duration_time:
                self.can_attack = True # 다시 공격 가능 상태로 바꿔준다.

        if not self.can_spell: # 마법 공격 시작 후, cans_spell이 False가 됐을 경우
            if current_time - self.spell_time >= self.spell_duration_time:
                self.can_spell = True # 쿨타임 시간이 지나면 다시 마법 공격 가능 상태로 바꿔준다.

    # scene.py > level_update() 에서 player.hitbox의 center x좌표 값을 받아옴.
    # 플레이어를 따라다닐 때 사용할 것.
    def setTargetPos(self, posX):
        self.targetPos = posX

    def getHitBox(self):
        return self.hitbox

    def getAttackBox(self):
        return self.attackBox # self.attackbox 는 안 쓰는 건가보네

    def getSpellAttackBox(self):
        return self.spell.getHitBox()

    def kill_monster(self):
        self.kill()
        self.hitbox.x = 90000
        self.spell.kill()
