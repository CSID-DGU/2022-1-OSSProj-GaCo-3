#-*-coding:utf-8-*-

import random
import time

import pygame
from settings import *
from support import *
from player import *
from Bringer import *
from random import choice
from debug import *

pygame.init()
font = pygame.font.Font(None, 30)

class Scene:
    def __init__(self, player, monster, scene_num, game_state, visible_sprites):
        self.display_surface = pygame.display.get_surface()
        self.game_state = game_state
        self.scene_num = scene_num

        # player, monster 객체 전달받기
        self.player = player
        self.monster = monster

        # player 초기화
        self.player.set_state_ini()

        # background setting
        self.visibile_sprites= visible_sprites
        self.visibile_sprites.background_setting(self.game_state)

        # for fade in/out
        self.fade_surf = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surf.fill((0, 0, 0)) # surface 검은 색으로 채움
        self.alpha = 255 # 장면 생성 처음엔 까만 화면
        self.fade_surf.set_alpha(self.alpha)

    def update(self, df):
        if self.game_state == 'intro':
            self.intro_update()
            return

        if self.game_state == 'ending':
            self.ending_update()
            return

        self.level_update(df)

    def level_update(self, df):
        self.visibile_sprites.custom_draw(self.player, self.game_state, self.monster)
        self.player.update(df)

        self.monster.setTargetPos(self.player.hitbox.x) # 플레이어 hitbox x 값 monster targetpos 로 넘겨주기.
        self.monster.update(df)

        # 디버그 코드
        debug("monster_Attackbox : " + str(self.monster.getAttackBox()), 10, 0)
        debug("spell_Attackbox : " + str(self.monster.getSpellAttackBox()), 10, 40)
        debug("player_hitbox : " + str(self.player.hitbox), 10, 80)
        debug("player_hp : " + str(self.player.hp), 10, 160)
        debug("monster_hp : " + str(self.monster.hp), 10, 120)
        #debug("Monster_isAttack : " + str(self.monster.isAttack), 10, 120)
        #debug("Spell_isAttack : " + str(self.monster.spell.isAttack), 10, 160)

        self.fade_in()
        debug(self.game_state, WIDTH // 2, HEIGHT // 2) #게임 장면 바뀌는 거 확인용

        pygame.display.update()

    def fade_in(self):
        # alpha 값 조절해서 fade in 효과 내기
        # scene 생성 후 alpha 값이 차츰 작아지다가 0 보다 작아지면 alpha 는 계속 0을 유지한다.
        # scene 삭제 시 fade_out 함수를 호출하면 alpha 값이 다시 차츰 높아지게 한다.
        self.alpha -= 30 if self.alpha > 0 else 0
        self.fade_surf.set_alpha(self.alpha)
        self.display_surface.blit(self.fade_surf, (0, 0))

    def intro_update(self):
        self.display_surface.fill((255, 255, 255))
        debug(self.game_state, WIDTH // 2, HEIGHT // 2)
        self.fade_in()
        pygame.display.update()

    def ending_update(self):
        self.display_surface.fill((255, 255, 255))
        debug(self.game_state, WIDTH // 2, HEIGHT // 2)
        self.fade_in()
        pygame.display.update()

    def fade_out(self): # 장면 전환시, 다음 장면 생성 전에 이 함수를 호출하자
        for alpha in range(0, 300):
            self.fade_surf.set_alpha(alpha)
            self.display_surface.blit(self.fade_surf, (0, 0))
            pygame.display.update()

    # Boss 할 때 혹시 사용할까 싶어서?
    def shake(self):
        pass


class CameraGroup(pygame.sprite.Group): # for level1, level2, level3
    def __init__(self, game_state):
        # general settings
        super(CameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()

        # for camera
        self.half_width = self.display_surface.get_width() // 2 # x 포지션에 사용할 화면 크기
        self.half_height = self.display_surface.get_height() // 2 # 층 만들면 그때 사용할 예정

        # 오프셋 세팅
        #self.offset = [0, 0]
        self.offset = pygame.math.Vector2()

        # 오프셋 변경 기준 x점
        self.left_x_point = 640 # 이 오프셋 포인트 기준으로 플레이어가 오른쪽으로 향하면 그 후로는 플레이어가 화면 중심에 있음
        self.right_x_point = 1850 # 이 오프셋 포인트 기준으로 플레이어가 왼쪽으로 향하면 그 후로는 플레이어가 화면 중심에 있음
        # 위의 포인트 사이에 있을 경우 플레이어는 항상 화면 가운데에 있지만
        # left 포인트보다 왼쪽에 있을 경우에는 오프셋은 left_x_point가 기준이된다. 반대의 경우도 마찬가지다. # custom_draw의 해당 코드에 또 주석 달아놓았음

        # game state에 따라서 배경 변화
        self.game_state = game_state

        #creating the floor s
        self.background_setting(game_state)

    def custom_draw(self, player, game_state, monster):
        self.set_offset(player) # 오프셋 설정함

        # 배경 오프셋 위치 설정
        # 멀리 있는 물체가 더 느리게 변화하고 바닥 물체가 더 빠르게 변화하므로 바닥이 멀리 있는 물체보다 이미지 사이즈가 커야함.
        floor_offset_pos = self.background_floor_rect.topleft - self.offset
        sky_offset_pos = self.background_mountain_rect.topleft - self.offset

        if game_state == 'level1':
            sky_offset_pos[0] *= 0.3 # 멀리있는 하늘은 x포지션의 변화 속도를 가까이있는 바닥보다 느리게 만들기

        # 배경 오프셋에 맞춰 배경(바닥, 벽)그리기
        self.display_surface.blit(self.background_mountain_surf, sky_offset_pos)
        self.display_surface.blit(self.background_floor_surf, floor_offset_pos + (0, -80) )

        # UI 추가
        self.hitbox_draw(player, monster) # player, monster 히트박스 그리기
        self.bar_draw(player, monster) # player 체력, 마나바 그리기, monster 체력바 그리기
        self.icon_setting() # 아이콘 세팅

        # ui그리기
        self.display_surface.blit(self.skill_thunder_icon, (50, 650))
        self.display_surface.blit(self.skill_stone_icon, (150, 650))
        self.display_surface.blit(self.Health_Potion_icon, (250, 650))
        self.display_surface.blit(self.Mana_Potion_icon, (350, 650))

        # 글자쓰기
        debug_surf = font.render(str(player.thunder_cool), True, (0, 0, 0)) #낙뢰마법 쿨
        self.display_surface.blit(debug_surf, (100, 650))
        debug_surf = font.render(str(player.stone_cool), True, (0, 0, 0)) #염력마법 쿨
        self.display_surface.blit(debug_surf, (200, 650))
        debug_surf = font.render(str(player.hp_potion), True, (0, 0, 0)) #체력포션 개수
        self.display_surface.blit(debug_surf, (300, 650))
        debug_surf = font.render(str(player.mp_potion), True, (0, 0, 0)) #마나포션 개수
        self.display_surface.blit(debug_surf, (400, 650))

        self.offset_transfer(player, monster) # player, monster에게 오프셋 전달
        self.hitbox_attackbox_transfer(player, monster) # player, monster에게 서로의 hitbox, attackbox 전달
        self.playerinfo_transfer(player, monster) #monster에게 player 공격력, 공격중인지 전달
        self.monsterinfo_transfer(player, monster) #player에게 monster가 공격력, 공격중인지 전달

        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def background_setting(self, game_state):
        self.background_mountain_surf = pygame.image.load(MAP_IMG_INFO[game_state]['background'])
        if game_state == 'level1':
            self.background_mountain_surf = pygame.transform.scale(self.background_mountain_surf, (1900, 720))
        else:
            self.background_mountain_surf = pygame.transform.scale(self.background_mountain_surf, (2500, 720))
        self.background_mountain_rect = self.background_mountain_surf.get_rect(topleft=(0, 0))

        self.background_floor_surf = pygame.image.load(MAP_IMG_INFO[game_state]['floor'])
        self.background_floor_surf = pygame.transform.scale(self.background_floor_surf, (2500, 800))  # 화면 변화 속도가 달라서 바닥만 대충 크게 리사이즈함. 이미지 리소스 바꾸면 값 바꿀 것
        self.background_floor_rect = self.background_floor_surf.get_rect(topleft=(0, 0))

    def set_offset(self, player):
        if player.hitbox.centerx <= self.left_x_point: # 시작 화면으로부터 left_x_point 범위에 플레이어가 있을 때는 카메라 이동 없음
            self.offset.x = self.left_x_point - self.half_width
        elif player.hitbox.centerx >= self.right_x_point: # right_x_point 부터 끝 장면까지 범위에 플레이어가 있을 때는 카메라 이동 없음
            self.offset.x = self.right_x_point - self.half_width
        else: # left_x_point ~ right_x_point 사이에 플레이어가 있을 때는 플레이어가 중심에 있을 수 있도록 카메라를 이동시킴
            self.offset.x = player.hitbox.centerx - self.half_width

    def offset_transfer(self, player, monster):
        #몬스터 인스턴스에 오프셋 전달
        monster.CameraOffset = self.offset
        #플레이어 인스턴스에 오프셋 전달
        player.CameraOffset = self.offset
    
    def hitbox_attackbox_transfer(self, player, monster):
        #몬스터 인스턴스에 플레이어 박스들 전달
        monster.playerHitbox = player.hitbox
        monster.playerAttackbox = player.attackBox
        #플레이어 인스턴스에 몬스터2 박스들 전달
        player.monsterHitbox = monster.getHitBox()
        player.monsterAttackbox = monster.getAttackBox()
        player.monsterSpellAttackbox = monster.getSpellAttackBox()

    def playerinfo_transfer(self, player, monster):
        monster.playerisAttack = player.isAttack
        monster.playerPower = player.AttackPower
    
    def monsterinfo_transfer(self, player, monster):
        player.monsterisAttack = monster.isAttack
        player.monsterspellisAttack = monster.spell.isAttack
        player.monsterPower = monster.AttackPower

    def hitbox_draw(self, player, monster):
        # 플레이어 히트박스 그리기
        pygame.draw.rect(self.display_surface, (255, 255, 255),
                         sub_Coordinate(player.hitbox, (self.offset[0], self.offset[1], 0, 0)), 3)
        # 몬스터 히트박스 그리기
        pygame.draw.rect(self.display_surface, (255, 0, 0),
                         sub_Coordinate(monster.getHitBox(), (self.offset[0] , self.offset[1], 0, 0)), 3)

    def bar_draw(self, player, monster):
        # 플레이어 체력, 마나 그리기
        pygame.draw.rect(self.display_surface, (255, 0, 0),
                         sub_Coordinate(player.healthbar, (self.offset[0], self.offset[1], 0, 0)), 0)
        pygame.draw.rect(self.display_surface, (0, 0, 255),
                         sub_Coordinate(player.manabar, (self.offset[0], self.offset[1], 0, 0)), 0)
        # 몬스터 체력 그리기
        pygame.draw.rect(self.display_surface, (255, 0, 0),
                         sub_Coordinate(monster.healthbar, (self.offset[0], self.offset[1], 0, 0)), 0)

    def icon_setting(self):
        #아이콘 세팅
        self.skill_thunder_icon = pygame.image.load('image/UI/thunder_icon.png')
        self.skill_thunder_icon = pygame.transform.scale(self.skill_thunder_icon, (40, 40))

        self.skill_stone_icon = pygame.image.load('image/UI/stone_icon.png')
        self.skill_stone_icon = pygame.transform.scale(self.skill_stone_icon, (40, 40))

        self.Health_Potion_icon = pygame.image.load('image/UI/Health_Potion.png')
        self.Health_Potion_icon = pygame.transform.scale(self.Health_Potion_icon, (40, 40))

        self.Mana_Potion_icon = pygame.image.load('image/UI/Mana_Potion.png')
        self.Mana_Potion_icon = pygame.transform.scale(self.Mana_Potion_icon, (40, 40))