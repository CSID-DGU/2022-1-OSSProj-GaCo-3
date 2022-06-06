# -*-coding:utf-8-*-

import pygame
from settings import *
from support import *
from game import *
from soundManager import *

class Devil_Firebomb(pygame.sprite.Sprite):
    def __init__(self, pos, SIZE, groups, obstacle_sprites):
        pygame.sprite.Sprite.__init__(self, groups)
        #������ ó�� �̹��� ���� ��ӹ޴� �� ���� Ŭ�������� ����������Ѵ�.
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('image/Monster/Devil/firebomb.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-SIZE[0]/4, 0)#�̹��� �簢���� ũ�� �ٿ� HitBox�� ���
        self.scale = SIZE
        self.CameraOffset = [0,0]
        self.isAttack = False

        #graphic setup
        self.import_assets('image/Monster/Devil/', DEVIL_FIREBOMB_INFO)
        self.status = 'firebomb'
        
        #self.thunderSound = soundManager.load_sound('Bringer_thunder', 'sound/bringer/bringer_thunder.wav')
        #self.thunderSound.set_volume(0.4)

        # animation �ٲ� �� ���
        self.frame_index = 0
        self.animation_speed = 0.25
        self.animation_time = 0.0
        self.animation_time_max = 0.1
        self.animation_end = False

        self.SkillON = True

        # movement
        self.speed = 4

        self.space_number = 0

        self.obstacle_sprites = obstacle_sprites

    def import_assets(self, path, MonsterInfo):
        self.spr = {'firebomb':[]}

        for spr_name in self.spr.keys():
            self.spr[spr_name] = import_sprites_image(path, spr_name +'.png',
                                                      MonsterInfo[spr_name]['idx'],
                                                      MonsterInfo[spr_name]['size'])

    def ON(self, posX):
        self.SkillON = True
        self.hitbox.x = posX - self.scale[0]/4
        self.hitbox.y = 300
        #self.thunderSound.play()

    def animate(self, df):
        spr = self.spr[self.status]
        # loop over the frame index
        #self.frame_index += self.animation_speed
        # DeltaTime�̿��ؼ� �ִϸ��̼� ������ ó�� 
        #=============================================================

        if self.SkillON == True:
            self.animation_time += df /1000.0

            if self.animation_time >= self.animation_time_max:
                self.animation_time = 0
                self.frame_index += 1
        
        else:
            self.frame_index = 0
        #===============================================================

        if self.frame_index >= len(spr): # ��������Ʈ ������ �̹������� ������ ��
            self.frame_index = 0 # �ٽ� ó�� �̹����� ���ư���
            self.SkillON = False
            self.hitbox.x = -500
            self.hitbox.y = -500

        self.image = spr[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: #collision occurs while moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right


    def update(self, df):
        self.animate(df)
        #���� �ڽ� ���� ����
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0]/16, -self.scale[1]/3)
        attack_hitbox = sub_Coordinate(attackBox, (self.CameraOffset[0], self.CameraOffset[1], 0, 0))
        
        if(self.frame_index < 12 and self.frame_index > 8):
            pygame.draw.rect(self.display_surface,(255, 255, 255), attack_hitbox, 3)
            self.isAttack = True
        else:
            self.isAttack = False

    def getHitBox(self):
        attackBox = pygame.Rect(self.hitbox)
        attackBox = attackBox.inflate(-self.scale[0]/16, -self.scale[1]/3)
        return attackBox


