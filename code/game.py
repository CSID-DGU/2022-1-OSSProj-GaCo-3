#-*-coding:utf-8-*-

import pygame, sys
from settings import *
from player import *
from level import *

class Game:
    def __init__(self):
        #general setup
        pygame.init()  # 초기화 init 호출
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 디스플레이 뜨게 하기
        pygame.display.set_caption("deca")  # 게임 이름

        # FPS
        self.clock = pygame.time.Clock()

        self.level = Level()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # 종료버튼 누르면 창 닫고 시스템 종료
                    pygame.quit()
                    sys.exit()

            self.level.run()
            pygame.display.update()  # 게임 화면을 다시 그리기!
            self.clock.tick(FPS)  # 게임 화면의 초당 프레임 수를 설정


if __name__ == '__main__':
    game = Game()
    game.run()