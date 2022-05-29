# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *

class player_missile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        # ������ ó�� �̹��� ���� ��ӹ޴� �� ���� Ŭ�������� ����������Ѵ�.
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('image/Monster/AbyssSpell/spell.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ABYSS_SPELL_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-50, -30)  # �̹��� �簢���� ũ�� �ٿ� hitbox�� ���

        self.scale = ABYSS_SPELL_SIZE
        self.CameraOffset = [0, 0]
        self.isAttack = False

        # graphic setup
        self.import_assets('image/Monster/AbyssSpell/', ABYSS_SPELL_INFO)
        self.status = 'spell'

        # animation �ٲ� �� ���
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

        self.target_pos = 0 # �÷��̾��� ��ġ ����

    def import_assets(self, path, MonsterInfo):
        self.spr = {'spell': []}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])

    def ON(self, target_pos, initial_pos):
        # �÷��̾ ���ʿ� ������ ���� ȭ�� �ٱ�����, �����ʿ� ������ ������ ȭ�� �ٱ����� ����
        distance = initial_pos[0] - target_pos
        self.target_pos = -100 if distance >= 0 else 2800
        self.isAttack = True
        self.SkillON = True
        self.hitbox.centerx = initial_pos[0] - 70 if distance >= 0 else initial_pos[0] + 70
        self.hitbox.y = 460

    def animate(self, df):
        spr = self.spr[self.status]

        if self.SkillON == True:
            self.animation_time += df / 1000.0

            if self.animation_time >= self.animation_time_max:
                self.animation_time = 0
                self.frame_index += 1
        else:
            self.frame_index = 0

        if self.frame_index >= len(spr):  # ��������Ʈ ������ �̹������� ������ ��
            self.frame_index = 0  # �ٽ� ó�� �̹����� ���ư���

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
        # ���� �ڽ� ���� ����
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(40, -30)
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
        # abyss attack2 ���� ���� �����Ͽ� �÷��̾� �������� ��� ������
        # �������� : �÷��̾� ��ġ������ �������� ���� ȭ�� ������ ��� �̵�
        distance = self.target_pos - self.hitbox.x
        if self.SkillON: # ���ݻ����� ��� ������
            if abs(distance) > self.boundary: # ��������Ʈ�� �÷��̾��� �Ÿ��� self.boundary ���� �ָ� ����
                if distance < 0: # ���� ���⿡ �÷��̾ ����
                    self.hitbox.x -= self.speed
                else: # ������ ���⿡ �÷��̾ ����
                    self.hitbox.x += self.speed
            else:
                self.SkillON = False
                self.hitbox.x = -500
                self.hitbox.y = -500