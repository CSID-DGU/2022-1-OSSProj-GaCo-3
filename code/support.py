# -*-coding:utf-8-*-

from os import walk
import pygame, sys
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

def import_sprites_image(filename, idx, size):
    path = 'image/player2/'
    surface_list = []
    max_col = max_index = max_row = idx
    baseImage = pygame.image.load(path+filename).convert()
    width = baseImage.get_width() / max_col
    height = baseImage.get_height()

    for i in range(max_index):  # 스프라이트 시트의 각 인덱스에 자른 이미지 저장
        image = pygame.Surface((width, height))
        image.blit(baseImage, (0, 0), ((i % max_row) * width, (i // max_col) * height, width, height))
        image = pygame.transform.scale(image, size)
        image.set_colorkey((0, 0, 0))  # 뒤에 흰배경 없앰
        """"
        if 'L' in filename: # 둘 차이 : 왼쪽 오른쪽 방향 <- 이미지 반전하고 저장할 때 달라진 것 같음
            image.set_colorkey((0, 0, 0))  # 뒤에 흰배경 없앰
        else:
            image.set_colorkey((255, 255, 255))  # 뒤에 검은배경 없앰
        """""
        surface_list.append(image)
    return surface_list

def quit_check(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

def sub_Coordinate(coor1, coor2):
    """
    subtract coor2 from coor1
    :param coor1: coordinate 1
    :param coor2: coordinate 2
    :return: (coor1[0] - coor2[0], coor1[1] - coor2[1]) -> tuple.
    """
    res = list(map(lambda x, y : x - y, coor1, coor2))
    return res

#사각형충돌처리함수
#A: 사각형, B: 리스트형태
def collision_check(A, B):
    if A.top < B[1]+B[3] and B[1] < A.bottom and A.left < B[0]+B[2] and B[0] < A.right:
        return True
    else:
        return False