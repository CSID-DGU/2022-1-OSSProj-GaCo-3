# -*-coding:utf-8-*-

import pygame
from settings import *
from function import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, PLAYER_SIZE, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.rect = pygame.Rect(pos[0], pos[1], PLAYER_SIZE[0], PLAYER_SIZE[1])  # 플레이어 히트박스 #차례대로 좌상x, 좌상y, 넓이, 높이

        self.import_player_assets()
        self.image = self.spr['stand'][0]

        # 플레이어 컨트롤 변수
        self.keyLeft = False
        self.keyRight = False
        self.keyLeft_Run = False
        self.keyRight_Run = False

        self.movement = [0, 0]
        self.vspeed = 0  # 플레이어 y가속도
        self.flytime = 0  # 공중에 뜬 시간
        self.action = 'stand'  # 플레이어 현재 행동
        self.state = 0  # (0: stand, 1: walk, 2: run, 3: jump, 4: stand_attack, 5: walk_attack, 6: run_attack, 7: jump_attack)
        self.frame = 0  # 플레이어 애니메이션 프레임
        self.frameSpeed = 20  # 플레이어 애니메이션 속도(낮을 수록 빠름. max 1)
        self.frameTimer = 0
        self.flip = False  # 플레이어 이미지 반전 여부 (False: RIGHT)
        self.loop = True  # 애니메이션 루프 (True: loop, False: Reverse)
        self.animationMode = True  # 애니메이션 모드 (True: 반복, False: 한번)

        # 플레이어 행동별 프레임스피드
        self.stand_framespeed = 20
        self.walk_framspeed = 7
        self.run_framspeed = 7
        self.jump_framespeed = 5
        self.attack_timer = 0  # 플레이어 공격 타이머

    def import_player_assets(self):
        character_path = 'image/player/'
        self.spr = {'stand':[], 'standL':[], 'walking':[], 'walkingL':[],
                    'running':[], 'runningL':[], 'jump':[], 'jumpL':[]}

        for spr_name in self.spr.keys():
            print(character_path+spr_name+'.png')
            self.spr[spr_name] = import_sprites_image(character_path + spr_name +'.png',
                                                      PLAYER_IMG_INFO[spr_name]['idx'],
                                                      PLAYER_IMG_INFO[spr_name]['size'], False)

    def input(self):

        pass

    def move(self):
        pass

    def get_status(self):
        pass

    def animate(self):
        pass

    def update(self):
        self.input()
        self.get_status()
        self.control()
        self.animate()
        self.move()

    def control(self):
        # 플레이어 컨트롤
        self.movement = [0, 0]  # 플레이어 이동 초기화
        # 걷기상태
        if self.state == 1:
            if self.keyLeft:
                self.movement[0] -= 4
            if self.keyRight:
                self.movement[0] += 4

        # 달리기상태
        if self.state == 2:
            if self.keyLeft_Run:
                self.movement[0] -= 8
            if self.keyRight_Run:
                self.movement[0] += 8
        # 점프상태 이동속도
        if self.state == 3:
            if self.keyLeft_Run:
                self.movement[0] -= 4
            if self.keyRight_Run:
                self.movement[0] += 4
            if self.keyLeft:
                self.movement[0] -= 4
            if self.keyRight:
                self.movement[0] += 4

        # 중력
        self.movement[1] += self.vspeed
        self.vspeed += 0.6
        if self.vspeed > 10:
            self.vspeed = 10

        # loop
        if self.loop:
            self.frameTimer += 1  # 플레이어 애니메이션 타이머
            if self.frameTimer >= self.frameSpeed:
                self.frame += 1
                self.frameTimer = 0
                if self.frame >= len(self.spr[self.action]):
                    if self.animationMode == True:
                        self.frame = 0
                    else:
                        self.frame -= 1
        # reverse_loop
        else:
            self.frameTimer += 1  # 플레이어 애니메이션 타이머
            if self.frameTimer >= self.frameSpeed:
                self.frame -= 1
                self.frameTimer = 0
                if self.frame <= 0:
                    if self.animationMode == True:
                        self.frame = len(self.spr[self.action]) - 1
                    else:
                        self.frame += 1

        # 플레이어 드로우
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.spr[self.action][self.frame], (self.rect.x, self.rect.y))

        for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?

            # 정지상태
            if self.state == 0:
                if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                    if event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walkingL', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft = True
                        self.keyRight = False

                    elif event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walking', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft = False
                        self.keyRight = True

                    elif event.key == pygame.K_SPACE and self.action == 'standL':  # 캐릭터를 왼쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 11, self.action, 'jumpL', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, False)
                        self.keyLeft = False
                        self.keyRight = False
                        self.vspeed = -15

                    elif event.key == pygame.K_SPACE and self.action == 'stand':  # 캐릭터를 오른쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'jump', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, True)
                        self.keyLeft = False
                        self.keyRight = False
                        self.vspeed = -15

                    elif event.key == pygame.K_z and event.key == pygame.K_LEFT:  # 캐릭터를 왼쪽으로 달림
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'runningL', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft_Run = True
                        self.keyRight_Run = False
                        self.keyLeft = False
                        self.keyRight = False

                    elif event.key == pygame.K_z and event.key == pygame.K_RIGHT:  # 캐릭터를 오른쪽으로 달림
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'running', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = True
                        self.keyLeft = False
                        self.keyRight = False

            # 걷기상태
            if self.state == 1:
                if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                    if event.key == pygame.K_z and self.keyLeft == True:  # 캐릭터를 왼쪽으로 달림
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'runningL', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft_Run = True
                        self.keyRight_Run = False
                        self.keyLeft = False
                        self.keyRight = False
                    elif event.key == pygame.K_z and self.keyRight == True:  # 캐릭터를 오른쪽으로 달림
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'running', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = True
                        self.keyLeft = False
                        self.keyRight = False
                    elif event.key == pygame.K_RIGHT and self.keyLeft == True:  # 캐릭터를 왼쪽걷다가 오른쪽 걷기
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walking', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft = False
                        self.keyRight = True
                    elif event.key == pygame.K_LEFT and self.keyRight == True:  # 캐릭터를 오른쪽걷다가 왼쪽 걷기
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walkingL', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft = True
                        self.keyRight = False
                    elif event.key == pygame.K_SPACE and self.action == 'walkingL':  # 캐릭터를 왼쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 11, self.action, 'jumpL', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, False)
                        self.keyLeft = True
                        self.keyRight = False
                        self.vspeed = -15

                    elif event.key == pygame.K_SPACE and self.action == 'walking':  # 캐릭터를 오른쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'jump', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, True)
                        self.keyLeft = False
                        self.keyRight = True
                        self.vspeed = -15

                if event.type == pygame.KEYUP:  # 방향키를 떼면 멈춤
                    if event.key == pygame.K_LEFT and self.keyLeft == True:
                        self.state = 0
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'standL', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft = False
                    elif event.key == pygame.K_RIGHT and self.keyRight == True:
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'stand', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, True)
                        self.state = 0
                        self.keyRight = False

            # 달리기상태
            if self.state == 2:
                if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                    if event.key == pygame.K_RIGHT and self.keyLeft_Run == True:  # 캐릭터를 왼쪽달리다가 오른쪽 달리기
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'running', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = True
                    elif event.key == pygame.K_LEFT and self.keyRight_Run == True:  # 캐릭터를 오른쪽달리다가 왼쪽 달리기
                        self.state = 2
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'runningL', self.frameSpeed, self.run_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft_Run = True
                        self.keyRight_Run = False
                    elif event.key == pygame.K_SPACE and self.action == 'runningL':  # 캐릭터를 왼쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 11, self.action, 'jumpL', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, False)
                        self.keyLeft_Run = True
                        self.keyRight_Run = False
                        self.vspeed = -15

                    elif event.key == pygame.K_SPACE and self.action == 'running':  # 캐릭터를 오른쪽으로 보며 점프
                        self.state = 3
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'jump', self.frameSpeed, self.jump_framespeed,
                            self.animationMode, False, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = True
                        self.vspeed = -15

                if event.type == pygame.KEYUP:  # 쉬프트를 떼면 걷기/ 방향키를 떼면 멈춤
                    if event.key == pygame.K_z and self.keyLeft_Run == True:
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walkingL', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft_Run = False
                        self.keyRight_Run = False
                        self.keyLeft = True
                        self.keyRight = False
                    elif event.key == pygame.K_z and self.keyRight_Run == True:
                        self.state = 1
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'walking', self.frameSpeed, self.walk_framspeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = False
                        self.keyLeft = False
                        self.keyRight = True
                    elif event.key == pygame.K_LEFT and self.keyLeft_Run == True:
                        self.state = 0
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'standL', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, False)
                        self.keyLeft_Run = False
                        self.keyRight_Run = False
                        self.keyLeft = False
                        self.keyRight = False
                    elif event.key == pygame.K_RIGHT and self.keyRight_Run == True:
                        self.state = 0
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'stand', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, True)
                        self.keyLeft_Run = False
                        self.keyRight_Run = False
                        self.keyLeft = False
                        self.keyRight = False
            # 점프상태
            if self.state == 3:
                if self.rect.bottom < 600:
                    if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
                        if event.key == pygame.K_RIGHT:  # 점프상태에서 오른쪽으로 이동
                            self.keyLeft = False
                            self.keyRight = True
                            self.keyLeft_Run = False
                            self.keyRight_Run = False
                        elif event.key == pygame.K_LEFT:  # 점프상태에서 왼쪽으로 이동
                            self.keyLeft = True
                            self.keyRight = False
                            self.keyLeft_Run = False
                            self.keyRight_Run = False
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_RIGHT and self.keyRight == True:  # 점프상태에서 오른쪽으로 이동하다가 정지
                            self.keyLeft = False
                            self.keyRight = False
                            self.keyLeft_Run = False
                            self.keyRight_Run = False
                        elif event.key == pygame.K_LEFT and self.keyLeft == True:  # 점프상태에서 왼쪽으로 이동하다가 정지
                            self.keyLeft = False
                            self.keyRight = False
                            self.keyLeft_Run = False
                            self.keyRight_Run = False
                # 착지->정지
                else:
                    self.state = 0
                    self.keyLeft = False
                    self.keyRight = False
                    self.keyLeft_Run = False
                    self.keyRight_Run = False
                    if self.action == 'jump':
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'stand', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, True)
                    elif self.action == 'jumpL':
                        self.frame, self.action, self.frameSpeed, self.animationMode, self.loop = change_playerAction(
                            self.frame, 0, self.action, 'standL', self.frameSpeed, self.stand_framespeed,
                            self.animationMode, True, self.loop, False)

            self.rect.left += self.movement[0]  # 수평이동값
            self.rect.top += self.movement[1]

        # 플레이어 수직거리 제한
        if self.rect.bottom > 600:
            self.rect.bottom = 600