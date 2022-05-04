#-*-coding:utf-8-*-

import random
import pygame
from settings import *
from support import *
from player import *
from random import choice
from debug import *

class Level():
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

    def run(self,df):
        self.visible_sprites.custom_draw(self.player)
        self.player.update(df)


class CameraGroup(pygame.sprite.Group): # Not implemented yet
    def __init__(self):
        # general settings
        super(CameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()

        #creating the floor s
        self.background_sky_surf = pygame.image.load('image/map/Start_Sky.png')
        self.background_sky_rect = self.background_sky_surf.get_rect(topleft=(0,0))
        self.background_floor_surf = pygame.image.load('image/map/Start_Map.png')
        self.background_floor_rect = self.background_floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        self.display_surface.blit(self.background_sky_surf, (0,0))
        self.display_surface.blit(self.background_floor_surf, (0,-150))
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
