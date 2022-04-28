# -*-coding:utf-8-*-

from os import walk
import pygame
import pygame.image

def import_folder(path):
    surface_list = []
    # walk(path) = (folder name : str, folder list: list, file list: list)
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = path + '/' +image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def import_sprites_image(filename, idx, (size_x, size_y)):
    path = 'image/player/'
    surface_list = []
    max_col = max_index = max_row = idx
    baseImage = pygame.image.load(path+filename).convert()
    width = baseImage.get_width() / max_col
    height = baseImage.get_height()

    for i in range(max_index):  # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
        image = pygame.Surface((width, height))
        image.blit(baseImage, (0, 0), ((i % max_row) * width, (i // max_col) * height, width, height))
        image = pygame.transform.scale(image, (size_x, size_y))
        if 'L' in filename: # 둘 차이 : 왼쪽 오른쪽 방향 <- 이미지 반전하고 저장할 때 달라진 것 같음
            image.set_colorkey((0, 0, 0))  # 뒤에 흰배경 없앰
        else:
            image.set_colorkey((255, 255, 255))  # 뒤에 검은배경 없앰
        surface_list.append(image)
    return surface_list
