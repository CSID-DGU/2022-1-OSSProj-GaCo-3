# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *

class AbyssSpell(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        # 생성시 처음 이미지 지정 상속받는 각 몬스터 클래스에서 지정해줘야한다.
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('image/Monster/AbyssSpell/spell.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ABYSS_SPELL_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-50, -30)  # 이미지 사각형의 크기 줄여 hitbox로 사용

        self.scale = ABYSS_SPELL_SIZE
        self.CameraOffset = [0, 0]
        self.isAttack = False

        # graphic setup
        self.import_assets('image/Monster/AbyssSpell/', ABYSS_SPELL_INFO)
        self.status = 'spell'

        # animation 바꿀 때 사용
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_time = 0.0
        self.animation_time_max = 0.1
        self.animation_end = False

        self.SkillON = True

        # movement
        self.speed = 20
        self.boundary = 10
        self.obstacle_sprites = obstacle_sprites

        self.target_pos = 0 # 플레이어의 위치 정보

    def import_assets(self, path, MonsterInfo):
        self.spr = {'spell': []}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])

    def ON(self, target_pos, initial_pos):
        # 플레이어가 왼쪽에 있으면 왼쪽 화면 바깥까지, 오른쪽에 있으면 오른쪽 화면 바깥까지 공격
        self.target_pos = -100 if initial_pos[0] - target_pos >= 0 else 2800
        self.isAttack = True
        self.SkillON = True
        self.hitbox.center = initial_pos
        self.hitbox.y = 500

    def animate(self, df):
        spr = self.spr[self.status]

        if self.SkillON == True:
            self.animation_time += df / 1000.0

            if self.animation_time >= self.animation_time_max:
                self.animation_time = 0
                self.frame_index += 1
        else:
            self.frame_index = 0

        if self.frame_index >= len(spr):  # 스프라이트 마지막 이미지까지 보여준 뒤
            self.frame_index = 0  # 다시 처음 이미지로 돌아가기

        self.image = spr[int(self.frame_index)]
        position = (self.hitbox.center[0] - 10, self.hitbox.center[1] + 20)
        self.rect = self.image.get_rect(center=position)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # collision occurs while moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

    def update(self, df):
        self.animate(df)
        # 어택 박스 정보 갱신
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0] / 16, -self.scale[1] / 3)
        attack_hitbox = sub_Coordinate(attackBox,
                                       (self.CameraOffset[0], self.CameraOffset[1] - self.scale[1] / 4, 0, 0))

        if abs(self.hitbox.centerx - self.target_pos) == 0:
            self.SkillON = False
            self.isAttack = False
            self.hitbox.x = -500
            self.hitbox.y = -500
        pygame.draw.rect(self.display_surface, (255, 0, 0), attack_hitbox, 3)
        self.move()

    def getHitBox(self):
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0] / 16, -self.scale[1] / 3)
        return attackBox

    def move(self):
        # abyss attack2 공격 직후 생성하여 플레이어 방향으로 계속 움직임
        # 수정사항 : 플레이어 위치까지만 움직이지 말고 화면 밖으로 계속 이동
        distance = self.target_pos - self.hitbox.x
        if self.SkillON: # 공격상태일 경우 움직임
            # if distance < 0:  # 왼쪽 방향에 플레이어가 있음
            #     self.hitbox.x -= self.speed
            # else:  # 오른쪽 방향에 플레이어가 있음
            #     self.hitbox.x += self.speed
            #
            # # 공격이 화면을 벗어나면 공격 중지
            # if self.hitbox.x > WIDTH or self.hitbox.x < 0 :
            #     self.SkillON = False
            #     self.hitbox.x = -500
            #     self.hitbox.y = -500

            if abs(distance) > self.boundary: # 스프라이트와 플레이어의 거리가 self.boundary 보다 멀면 동작
                if distance < 0: # 왼쪽 방향에 플레이어가 있음
                    self.hitbox.x -= self.speed
                else: # 오른쪽 방향에 플레이어가 있음
                    self.hitbox.x += self.speed
            else:
                self.SkillON = False
                self.hitbox.x = -500
                self.hitbox.y = -500