#-*-coding:utf-8-*-

import random
import pygame
from settings import *
from support import *
from player import *
from random import choice
from debug import *

class Level:
    def __init__(self):
        self.player_size = (200, 200)

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):
        # player 생성
        self.player = Player((100, 400), PLAYER_SIZE, [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.player.update()


class CameraGroup(pygame.sprite.Group): # Not implemented yet
    def __init__(self):
        # general settings
        super(CameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()

        # for camera
        self.half_width = self.display_surface.get_width() // 2 # x 포지션에 사용할 화면 크기
        self.half_height = self.display_surface.get_height() // 2 # 층 만들면 그때 사용할 예정

        # 오프셋 세팅
        self.offset = pygame.math.Vector2()

        # 오프셋 변경 기준 x점
        self.left_x_point = 639 # 이 오프셋 포인트 기준으로 플레이어가 오른쪽으로 향하면 그 후로는 플레이어가 화면 중심에 있음
        self.right_x_point = 2800 # 이 오프셋 포인트 기준으로 플레이어가 왼쪽으로 향하면 그 후로는 플레이어가 화면 중심에 있음
        # 위의 포인트 사이에 있을 경우 플레이어는 항상 화면 가운데에 있지만
        # left 포인트보다 왼쪽에 있을 경우에는 오프셋은 left_x_point가 기준이된다. 반대의 경우도 마찬가지다. # custom_draw의 해당 코드에 또 주석 달아놓았음

        #creating the floor s
        self.background_sky_surf = pygame.image.load('image/map/Start_Sky.png')
        self.background_sky_rect = self.background_sky_surf.get_rect(topleft=(0,0))

        self.background_floor_surf = pygame.image.load('image/map/Start_Map.png')
        self.background_floor_surf = pygame.transform.scale(self.background_floor_surf, (4000, 897)) # 화면 변화 속도가 달라서 바닥만 대충 크게 리사이즈함. 이미지 리소스 바꾸면 값 바꿀 것
        self.background_floor_rect = self.background_floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        # offset setting
        if player.rect.centerx <= self.left_x_point: # 시작 화면으로부터 left_x_point 범위에 플레이어가 있을 때는 카메라 이동 없음
            self.offset.x = self.left_x_point - self.half_width
        elif player.rect.centerx >= self.right_x_point: # right_x_point 부터 끝 장면까지 범위에 플레이어가 있을 때는 카메라 이동 없음
            self.offset.x = self.right_x_point - self.half_width
        else: # left_x_point ~ right_x_point 사이에 플레이어가 있을 때는 플레이어가 중심에 있을 수 있도록 카메라를 이동시킴
            self.offset.x = player.rect.centerx - self.half_width

        # 멀리 있는 물체가 더 느리게 변화하고 바닥 물체가 더 빠르게 변화하므로 바닥이 멀리 있는 물체보다 이미지 사이즈가 커야함.
        # 스케일을 맞춰볼까? :
        floor_offset_pos = self.background_floor_rect.topleft - self.offset
        sky_offset_pos = self.background_sky_rect.topleft - self.offset
        sky_offset_pos.x *= 0.3 # 멀리있는 하늘은 x포지션의 변화 속도를 가까이있는 바닥보다 느리게 만들기

        self.display_surface.blit(self.background_sky_surf, sky_offset_pos)
        self.display_surface.blit(self.background_floor_surf, floor_offset_pos + (0,-150))

        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

        debug("player center : "+str(player.rect.center))
        debug("sky pos : "+str(sky_offset_pos), 10, 30)
        debug("floor pos : "+str(floor_offset_pos + (0,-150)), 10, 50)