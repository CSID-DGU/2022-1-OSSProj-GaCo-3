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
from scene import *
from abyss import *

class Level:
    def __init__(self):
        # game state for scene transition
        self.scene_num = 0
        self.game_state = GAME_STATES[self.scene_num] # intro 부터 시작
        self.stage_changing = False
        self.can_change_stage = True
        self.time = None # game.py -> run() 에서 보내줌

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = CameraGroup(self.game_state)
        self.obstacle_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        # 게임 클리어했는지 여부
        self.is_clear = False # 레벨3까지 플레이어가 죽지 않고, 레벨3에서 보스가 죽으면 True로 전환한다.

        # 플레이어가 죽거나 / 레벨3의 보스 몬스터가 죽으면 self.done == True 가 된다.
        self.done = False

    def create_map(self):
        # player 생성
        self.player = Player(PLAYER_COOR_ini, PLAYER_SIZE, [self.visible_sprites], self.obstacle_sprites)
        # monster 생성
        self.monster = Abyss(ABYSS_COOR_ini, ABYSS_SIZE, [self.visible_sprites], self.obstacle_sprites)
        # scene 생성
        self.scene = Scene(self.player, self.monster, self.scene_num, self.game_state, self.visible_sprites) #시작은 game_state = 'intro'임

    def run(self, df):
        self.scene.update(df, self.time)
        self.scene_manager(self.scene)

    def monster_create(self, game_state):
        if game_state == 'level1': # monster1 생성 후 바꿔야함
            return Abyss(ABYSS_COOR_ini, ABYSS_SIZE, [self.visible_sprites], self.obstacle_sprites)

        if game_state == 'level2':
            return Bringer(BRINGER_COOR_ini, BRINGER_SIZE, [self.visible_sprites], self.obstacle_sprites)

        if game_state == 'level3': # boss 생성 후 바꿔야함
            return Bringer(BRINGER_COOR_ini, BRINGER_SIZE, [self.visible_sprites], self.obstacle_sprites)

        # intro, ending
        return Bringer(BRINGER_COOR_ini, BRINGER_SIZE, [self.visible_sprites], self.obstacle_sprites)

    def scene_manager(self, scene):
        scene_change = False
        # scnee change event를 체크하고(현재는 마우스 클릭)
        # 들어왔으면 scene_change = True -> 아래에서 장면 변환 시 초기화 작업 해줌
        for event in pygame.event.get():
            quit_check(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                scene.fade_out() # 장면 fade_out
                scene_change = True

        if self.player.isDead: # 플레이어가 죽었으면
            self.scene.BGM.stop()#BGM 종료
            self.done = True # 게임 종료

        if self.monster.isDead: # 몬스터가 죽었으면
            self.scene.BGM.stop()#BGM 종료
            scene_change = True # 장면 전환

        if scene_change:
            # scene_num 증가시켜서 game_state 바꾸기
            if self.scene_num < len(GAME_STATES) - 1:
                self.scene_num += 1
            else: # game_state 끝까지 재생했을 경우 : 레벨3에서 다시 장면 바꾸고자 scene_change 를 호출했을 경우
                self.scene_num = 0
                self.is_clear = True
                self.done = True # 게임을 종료하고 메뉴 화면으로 돌아가기

            self.game_state = GAME_STATES[self.scene_num]

            self.player.hp = PLAYER_HP # 레벨 바뀌면 플레이어 hp 회복하기
            self.player.mp = PLAYER_MP # 레벨 바뀌면 플레이어 mp 회복하기
            self.monster.kill()  # 이전 레벨 몬스터 죽이기
            self.monster.spell.kill() # 몬스터 스펠 죽이기
            self.monster = self.monster_create(self.game_state)  # 몬스터 생성
            self.scene.BGM.stop()
            self.scene = Scene(self.player, self.monster, self.scene_num, self.game_state, self.visible_sprites)  # 다음 장면 생성