#-*-coding:utf-8-*-

import random
import pygame
from settings import *
from support import *
from player import *
from random import choice
class Level:
    def __init__(self):
        self.player_size = (200, 200)

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()

        #sprite setup
        self.create_map()

    def create_map(self):
        # player 생성
        self.player = Player((100, 400), PLAYER_SIZE, self.visible_sprites)

        pass

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.player.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general settings
        super(YSortCameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()
        # self.half_width = self.display_surface.get_width() // 2
        # self.half_height = self.display_surface.get_height() // 2
        # self.offset = pygame.math.Vector2()

        #creating the floor
        self.background_sky_surf = pygame.image.load('image/map/Start_Sky.png')
        self.background_sky_rect = self.background_sky_surf.get_rect(topleft=(0,0))
        self.background_floor_surf = pygame.image.load('image/map/Start_Map.png')
        self.background_floor_rect = self.background_floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        #getting the offset
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        # floor_offset_pos = self.background_floor_rect.topleft - self.offset
        self.display_surface.blit(self.background_sky_surf, (0,0))
        self.display_surface.blit(self.background_floor_surf, (0,-150))

        # for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
        #     offset_position = sprite.rect.topleft - self.offset
        #     self.display_surface.blit(sprite.image, offset_position)