import pygame
from settings import *
from support import *
from debug import *

class sound():
    def __init__(self, name, path):
        self.sound = pygame.mixer.Sound(path)
        self.name = name
        
    def play(self, loop = False)-> None:
        #중복되게 사운드가 재생되는 것을 막기 위해
        #이 사운드가 재생되는 채널이 없을 경우에만 재생
        if(self.sound.get_num_channels() == 0):
            if(loop):
                self.sound.play(-1)
            else:
                self.sound.play(0)

    def stop(self)-> None:
        self.sound.stop()

    def fadeout(self, time: int): # 사운드 페이드아웃 효과
        self.sound.fadeout(time)

    def set_volume(self, volume : float): #0.0 ~ 1.0 사이의 값으로 볼륨 조절
        self.sound.set_volume(volume)

