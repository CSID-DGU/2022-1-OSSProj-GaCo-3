 #-*-coding:utf-8-*-

import pygame, sys, os
from datafile import *
from pygame.locals import *
import pygame.mixer

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
         #게임 컨트롤 변수
        pygame.display.set_caption('RPG tutorial')                                      # 창 이름 설정
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),0,32) #스크린생성
        
        self.camera_scroll = [40, 0]              # 카메라 이동 좌표

        #리소스 불러오기
        self.spriteSheet_player = SpriteSheet('player/stand.png',485/5,95,1,5,5,200,200)
        self.spriteSheet_player_p = SpriteSheet('spriteSheet1.png', 16, 16, 8, 8, 12,1000,300)
        
        self.spr_player = {} #플레이어 스프라이트 시트
        self.spr_player['stand'] = createSpriteSet(self.spriteSheet_player,0,4)
        self.spr_player['stay'] = createSpriteSet(self.spriteSheet_player_p, [0])
        
        # 플레이어 컨트롤 변수
        self.keyLeft = False
        self.keyRight = False

        self.player_rect = pygame.Rect((100,400), (600, 700))  # 플레이어 히트박스
        self.player_movement = [0, 0]            # 플레이어 프레임당 속도
        self.player_vspeed = 0                   # 플레이어 y가속도
        self.player_flytime = 0                  # 공중에 뜬 시간

        self.player_action = 'stand'              # 플레이어 현재 행동
        self.player_frame = 0                    # 플레이어 애니메이션 프레임
        self.player_frameSpeed = 1               # 플레이어 애니메이션 속도(낮을 수록 빠름. max 1)
        self.player_frameTimer = 0
        self.player_flip = False                 # 플레이어 이미지 반전 여부 (False: RIGHT)
        self.player_animationMode = True         # 애니메이션 모드 (False: 반복, True: 한번)
        self.player_walkSoundToggle = False
        self.player_walkSoundTimer = 0

        self.player_attack_timer = 0             # 플레이어 공격 타이머
        self.player_attack_speed = 15            # 플레이어 공격 속도
        
        self.run() # 게임 실행
    
    def run(self):
        # 메인루프 
        while True:
                    
            self.screen.fill(BACKGROUND_COLOR) #화면 초기화
            
            # 플레이어 애니메이션 타이머
            self.player_frameTimer += 1                          
            if self.player_frameTimer >= self.player_frameSpeed:
                self.player_frame +=1
                self.player_frameTimer = 0

                if self.player_frame >= len(self.spr_player[self.player_action]):
                    if self.player_animationMode == True:
                        self.player_frame = 0
                    else:
                        self.player_frame -= 1
                        
            # 플레이어 드로우
            self.screen.blit(pygame.transform.flip(self.spr_player[self.player_action][self.player_frame], self.player_flip, False)
                               , (self.player_rect.x , self.player_rect.y))
            
            #이벤트 컨트롤
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            
            pygame.display.update()
            self.clock.tick(60)
            
game = Game() # 게임실행 
             
             