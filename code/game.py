#-*-coding:utf-8-*-
#
import pygame, sys
from settings import *
from player import *
from level import *

class Game:
    def __init__(self):
        #general setup
        pygame.init()  # 초기화 init 호출
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 디스플레이 뜨게 하기
        pygame.display.set_caption("The Devil's Castle")  # 게임 이름

        # FPS
        self.clock = pygame.time.Clock()
        
        self.level = Level()


    def run(self):
        while True:
            # 플레이어 인풋 받을 때 event 체크를 함. 그때 종료 조건 확인하기 때문에 여기서 할 필요 없지만 기능 분리를 위해 일단 살려놓음
            for event in pygame.event.get():
                quit_check(event)
                
            print(self.level.player.status)
            print(self.level.player.status_num)
            

            df = self.clock.tick(FPS) # 게임 화면의 초당 프레임 수를 설정
            self.level.run(df)  #df: 프레임
            pygame.display.update()  # 게임 화면을 다시 그리기!


if __name__ == '__main__':
    game = Game()
    game.run()