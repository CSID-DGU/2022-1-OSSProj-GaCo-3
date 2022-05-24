import string
import pygame
from settings import *
from support import *
from debug import *
from sound import sound

class soundManager():
    SoundMap = {}

    def __init__(self):
        pass

    @staticmethod
    def find_sound(name)-> sound :
        Sound = soundManager.SoundMap.get(name)
        #호출한 곳에서 None인지 아닌지 체크해서 사용해주길 바람
        return Sound

    @staticmethod
    def load_sound(name, path)-> bool:
        #중복된 이름의 사운드가 있을 경우 false 리턴
        #사운드를 사용하는 곳에서 Load 함수 이후에 반드시 위의 find_sound 함수로 사운드를 가져와서 사용할 것
        if(soundManager.SoundMap.get(name) != None):
            return False

        Sound = sound(name, path)
        
        soundManager.SoundMap[name] = Sound

        return True
        
    @staticmethod
    def play(name, loop = False)-> None:
        Sound = soundManager.find_sound(name)

        if(Sound == None):
            return

        #중복되게 사운드가 재생되는 것을 막기 위해
        #이 사운드가 재생되는 채널이 없을 경우에만 재생
        if(Sound.get_num_channels() == 0):
            if(loop):
                Sound.play(-1)
            else:
                Sound.play(0)
        

    @staticmethod
    def stop(name)-> None:
        Sound = soundManager.find_sound(name)

        if(Sound == None):
            return

        Sound.stop()

    @staticmethod
    def fadeout(name, time: int): # 사운드 페이드아웃 효과
        Sound = soundManager.find_sound(name)
        
        if(Sound == None):
            return

        Sound.fadeout(time)

    @staticmethod
    def set_volume(name, volume : float): #0.0 ~ 1.0 사이의 값으로 볼륨 조절
        
        if volume > 1.0 or volume < 0.0:
            return
        
        Sound = soundManager.find_sound(name)
        
        if(Sound == None):
            return

        Sound.set_volume(volume)