 #-*-coding:utf-8-*-

import pygame
from function import*

pygame.init() #초기화 init 호출

screen_width = 10#1280 #가로 크기
screen_height = 10#720 #세로 크기
screen = pygame.display.set_mode((screen_width,screen_height)) #디스플레이 뜨게 하기

pygame.display.set_caption("악마의 성") #게임 이름

#FPS
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load("../image/map/Background.png")
background = pygame.transform.scale(background, (screen_width,screen_height)) #크기 지정
ground = pygame.image.load("../image/map/Start_Map.png")
ground = pygame.transform.scale(ground, (screen_width,screen_height)) #크기 지정

#캐릭터 불러오기
spriteSheet_player_stand_R = SpriteSheet('player/stand.png',485/5,95,5,5,5,200,200,False)
spriteSheet_player_stand_L = SpriteSheet('player/standL.png',485/5,95,5,5,5,200,200,True)
spriteSheet_player_walk_R = SpriteSheet('player/walking.png',776/8,97,8,8,8,200,200,False)
spriteSheet_player_walk_L = SpriteSheet('player/walkingL.png',776/8,97,8,8,8,200,200,True)
spriteSheet_player_Run_R = SpriteSheet('player/running.png',970/10,95,10,10,10,190,190,False)
spriteSheet_player_Run_L = SpriteSheet('player/runningL.png',970/10,95,10,10,10,190,190,True)
spriteSheet_player_Jump_L = SpriteSheet('player/jumpL.png',1163/12,96,12,12,12,200,200,True)
spriteSheet_player_Jump_R = SpriteSheet('player/jump.png',1163/12,96,12,12,12,200,200,False)

spr_player = {} #플레이어 스프라이트 시트
spr_player['stand_R'] = createSpriteSet(spriteSheet_player_stand_R,0,4)
spr_player['stand_L'] = createSpriteSet(spriteSheet_player_stand_L,0,4)
spr_player['walk_R'] = createSpriteSet(spriteSheet_player_walk_R,0,7)
spr_player['walk_L'] = createSpriteSet(spriteSheet_player_walk_L,0,7)
spr_player['Run_R'] = createSpriteSet(spriteSheet_player_Run_R,0,9)
spr_player['Run_L'] = createSpriteSet(spriteSheet_player_Run_L,0,9)
spr_player['Jump_L'] = createSpriteSet(spriteSheet_player_Jump_L,0,11)
spr_player['Jump_R'] = createSpriteSet(spriteSheet_player_Jump_R,0,11)

# 플레이어 컨트롤 변수
keyLeft = False
keyRight = False
keyLeft_Run = False
KeyLeft_Run = False

player_rect = pygame.Rect(100,400,200,200)  # 플레이어 히트박스 #차례대로 좌상x, 좌상y, 넓이, 높이
player_movement = [0, 0] 
player_vspeed = 0                   # 플레이어 y가속도
player_flytime = 0                  # 공중에 뜬 시간
player_action = 'stand_R'           # 플레이어 현재 행동
player_state = 0                    #(0: stand, 1: walk, 2: run, 3: jump, 4: stand_attack, 5: walk_attack, 6: run_attack, 7: jump_attack)
player_frame = 0                    # 플레이어 애니메이션 프레임
player_frameSpeed = 20               # 플레이어 애니메이션 속도(낮을 수록 빠름. max 1)
player_frameTimer = 0
player_flip = False                 # 플레이어 이미지 반전 여부 (False: RIGHT)
player_loop = True                  # 애니메이션 루프 (True: loop, False: Reverse)
player_animationMode = True         # 애니메이션 모드 (True: 반복, False: 한번)

#플레이어 행동별 프레임스피드
player_stand_framespeed = 20
player_walk_framspeed = 7
player_run_framspeed = 7
player_jump_framespeed = 5

player_attack_timer = 0             # 플레이어 공격 타이머


#이벤트 루프
running = True
while running:
    clock.tick(60) #게임 화면의 초당 프레임 수를 설정
    
    screen.blit(background, (0,0)) #배경 그리기
    screen.blit(ground, (0,0)) #배경 그리기
    
    # 플레이어 컨트롤
    player_movement = [0, 0]                       # 플레이어 이동 초기화
    #걷기상태
    if player_state == 1:
        if keyLeft:
            player_movement[0] -= 4
        if keyRight:
            player_movement[0] += 4
    
    #달리기상태
    if player_state == 2:
        if keyLeft_Run:
            player_movement[0] -= 8
        if keyRight_Run:
            player_movement[0] += 8
    #점프상태 이동속도
    if player_state == 3:
        if keyLeft_Run:
            player_movement[0] -= 4
        if keyRight_Run:
            player_movement[0] += 4
        if keyLeft:
            player_movement[0] -= 4
        if keyRight:
            player_movement[0] += 4
        
    #중력
    player_movement[1] += player_vspeed
    player_vspeed += 0.6
    if player_vspeed > 10:
        player_vspeed = 10
    
    #loop
    if player_loop:
        player_frameTimer += 1                       # 플레이어 애니메이션 타이머
        if player_frameTimer >= player_frameSpeed:
            player_frame +=1
            player_frameTimer = 0
            if player_frame >= len(spr_player[player_action]):
                if player_animationMode == True:
                    player_frame = 0
                else:
                    player_frame -= 1
    #reverse_loop
    else:
        player_frameTimer += 1                       # 플레이어 애니메이션 타이머
        if player_frameTimer >= player_frameSpeed:
            player_frame -=1
            player_frameTimer = 0
            if player_frame <= 0:
                if player_animationMode == True:
                    player_frame = len(spr_player[player_action])-1
                else:
                    player_frame += 1
    
    # 플레이어 드로우
    screen.blit(spr_player[player_action][player_frame], (player_rect.x , player_rect.y))
    
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT:
            running = False
        
    #정지상태
    if player_state == 0:
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_L', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, False)
                keyLeft = True
                keyRight = False
            elif event.key ==pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_R', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, True)
                keyLeft = False
                keyRight = True
            elif event.key ==pygame.K_SPACE and player_action == 'stand_L': # 캐릭터를 왼쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,11, player_action, 'Jump_L', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, False)
                keyLeft = False
                keyRight = False
                player_vspeed = -15
            elif event.key ==pygame.K_SPACE and player_action == 'stand_R': # 캐릭터를 오른쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Jump_R', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, True)
                keyLeft = False
                keyRight = False
                player_vspeed = -15
            elif event.key == pygame.K_z and event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로 달림
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_L', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, False)
                keyLeft_Run = True
                keyRight_Run = False
                keyLeft = False
                keyRight = False
            elif event.key == pygame.K_z and event.key ==pygame.K_RIGHT: # 캐릭터를 오른쪽으로 달림
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_R', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = True
                keyLeft = False
                keyRight = False
            
    
    #걷기상태
    if player_state == 1:
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_z and keyLeft == True: # 캐릭터를 왼쪽으로 달림
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_L', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, False)
                keyLeft_Run = True
                keyRight_Run = False
                keyLeft = False
                keyRight = False
            elif event.key == pygame.K_z and keyRight == True: # 캐릭터를 오른쪽으로 달림
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_R', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = True
                keyLeft = False
                keyRight = False
            elif event.key == pygame.K_RIGHT and keyLeft == True: # 캐릭터를 왼쪽걷다가 오른쪽 걷기
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_R', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, True)
                keyLeft = False
                keyRight = True
            elif event.key == pygame.K_LEFT and keyRight == True: # 캐릭터를 오른쪽걷다가 왼쪽 걷기
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_L', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, False)
                keyLeft = True
                keyRight = False
            elif event.key ==pygame.K_SPACE and player_action == 'walk_L': # 캐릭터를 왼쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,11, player_action, 'Jump_L', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, False)
                keyLeft = True
                keyRight = False
                player_vspeed = -15
            elif event.key ==pygame.K_SPACE and player_action == 'walk_R': # 캐릭터를 오른쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Jump_R', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, True)
                keyLeft = False
                keyRight = True
                player_vspeed = -15

        if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT and keyLeft == True:
                player_state = 0
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_L', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, False)
                keyLeft = False
            elif event.key == pygame.K_RIGHT and keyRight == True:
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_R', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, True)
                player_state = 0
                keyRight = False
    
    #달리기상태
    if player_state == 2:
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_RIGHT and keyLeft_Run == True: # 캐릭터를 왼쪽달리다가 오른쪽 달리기
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_R', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = True
            elif event.key == pygame.K_LEFT and keyRight_Run == True: # 캐릭터를 오른쪽달리다가 왼쪽 달리기
                player_state = 2
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Run_L', player_frameSpeed, player_run_framspeed, player_animationMode, True, player_loop, False)
                keyLeft_Run = True
                keyRight_Run = False
            elif event.key ==pygame.K_SPACE and player_action == 'Run_L': # 캐릭터를 왼쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,11, player_action, 'Jump_L', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, False)
                keyLeft_Run = True
                keyRight_Run = False
                player_vspeed = -15
            elif event.key ==pygame.K_SPACE and player_action == 'Run_R': # 캐릭터를 오른쪽으로 보며 점프
                player_state = 3
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'Jump_R', player_frameSpeed, player_jump_framespeed, player_animationMode, False, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = True
                player_vspeed = -15

        if event.type == pygame.KEYUP: # 쉬프트를 떼면 걷기/ 방향키를 떼면 멈춤
            if event.key == pygame.K_z and keyLeft_Run == True:
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_L', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, False)
                keyLeft_Run = False
                keyRight_Run = False
                keyLeft = True
                keyRight = False
            elif event.key == pygame.K_z and keyRight_Run == True:
                player_state = 1
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'walk_R', player_frameSpeed, player_walk_framspeed, player_animationMode, True, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = False
                keyLeft = False
                keyRight = True
            elif event.key == pygame.K_LEFT and keyLeft_Run == True:
                player_state = 0
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_L', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, False)
                keyLeft_Run = False
                keyRight_Run = False
                keyLeft = False
                keyRight = False
            elif event.key == pygame.K_RIGHT and keyRight_Run == True:
                player_state = 0
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_R', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, True)
                keyLeft_Run = False
                keyRight_Run = False
                keyLeft = False
                keyRight = False
    #점프상태
    if player_state == 3:
        if player_rect.bottom < 600:
            if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
                if event.key == pygame.K_RIGHT: # 점프상태에서 오른쪽으로 이동
                    keyLeft = False
                    keyRight = True
                    keyLeft_Run = False
                    keyRight_Run = False
                elif event.key == pygame.K_LEFT: # 점프상태에서 왼쪽으로 이동
                    keyLeft = True
                    keyRight = False
                    keyLeft_Run = False
                    keyRight_Run = False
            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT and keyRight == True: # 점프상태에서 오른쪽으로 이동하다가 정지
                    keyLeft = False
                    keyRight = False
                    keyLeft_Run = False
                    keyRight_Run = False
                elif event.key == pygame.K_LEFT and keyLeft == True: # 점프상태에서 왼쪽으로 이동하다가 정지
                    keyLeft = False
                    keyRight = False
                    keyLeft_Run = False
                    keyRight_Run = False
        #착지->정지
        else:
            player_state = 0
            keyLeft = False
            keyRight = False
            keyLeft_Run = False
            keyRight_Run = False
            if player_action == 'Jump_R':
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_R', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, True)
            elif player_action == 'Jump_L':
                player_frame, player_action, player_frameSpeed, player_animationMode, player_loop = change_playerAction(
                player_frame,0, player_action, 'stand_L', player_frameSpeed, player_stand_framespeed, player_animationMode, True, player_loop, False)
                
        

    player_rect.left += player_movement[0]  #수평이동값
    player_rect.top += player_movement[1]
    
    #플레이어 수직거리 제한
    if player_rect.bottom > 600 :
        player_rect.bottom = 600
    
    pygame.display.update() #게임 화면을 다시 그리기!
    
pygame.quit()