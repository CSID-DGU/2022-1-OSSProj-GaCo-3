#-*-coding:utf-8-*-

import pygame, sys
from settings import *
from level import *
from rank import *

class Game:
    def __init__(self):
        #general setup
        pygame.init()  # 초기화 init 호출
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 디스플레이 뜨게 하기
        pygame.display.set_caption("The Devil's Castle")  # 게임 이름

        # FPS
        self.clock = pygame.time.Clock()
        
        self.level = Level()

        # ranking setup
        self.user_name = "Test_name" # 시작화면에서 입력받기
        self.game_start_time = None # 레벨1 시작할 때 시간
        self.game_end_time = None # 레벨3 클리어 했을 때 시간
        self.time_score = None # 게임 끝났을 때 시간 계산 후 저장

        self.is_clicked = False # 메뉴에서 클릭 이벤트 저장

        menu_button_height =  HEIGHT//7
        self.start_button_pos = (WIDTH//2, menu_button_height * 6)  # start button center 위치
        self.ranks_button_pos = (WIDTH // 2 - WIDTH//7, menu_button_height * 6)  # rank button center 위치
        self.exit_button_pos = (WIDTH // 2 + WIDTH//7, menu_button_height * 6)  # exit button center 위치
        self.story_button_pos = (WIDTH // 7, menu_button_height) # 임시
        self.key_button_pos = ((WIDTH // 7) * 6, menu_button_height) # 임시

        self.import_assets() # 이미지 등을 모두 로드해놓고 시작하기

        # for fade in/out
        self.fade_surf = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surf.fill((0, 0, 0)) # surface 검은 색으로 채움
        self.alpha = 255 # 장면 생성 처음엔 까만 화면
        self.fade_surf.set_alpha(self.alpha)

    def import_assets(self):
        self.main_path = 'image/etc/'
        # menu background
        self.background_surf = pygame.image.load(f'{self.main_path}menu_background.png').convert_alpha()
        self.background_surf = pygame.transform.scale(self.background_surf, (WIDTH, HEIGHT))
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        # intro 화면들
        self.start_surf = pygame.image.load(f'{self.main_path}start_1.png').convert_alpha()
        self.start_rect = self.start_surf.get_rect(topleft=(0, 0))

        self.story_surf = pygame.image.load(f'{self.main_path}story_2.png').convert_alpha()
        self.story_rect = self.story_surf.get_rect(topleft=(0, 0))

        self.key_surf = pygame.image.load(f'{self.main_path}key_3.png').convert_alpha()
        self.key_rect = self.key_surf.get_rect(topleft=(0, 0))

        # 메뉴 레이아웃
        self.leading = 50
        # self.button_size = (50, 20)

        # 시작 버튼 -> intro 보여주고 run() 실행 ->
        self.start_button_surf = pygame.image.load(f'{self.main_path}menu_start.png').convert_alpha()
        self.start_button = self.start_button_surf.get_rect(center=self.start_button_pos)

        # 랭킹 버튼 -> ranks() 실행 (랭킹화면)
        self.ranks_button_surf = pygame.image.load(f'{self.main_path}menu_rank.png').convert_alpha()
        self.ranks_button = self.ranks_button_surf.get_rect(center=self.ranks_button_pos)

        # 종료 버튼 -> 게임 종료, 화면 닫음
        self.exit_button_surf = pygame.image.load(f'{self.main_path}menu_exit.png').convert_alpha()
        self.exit_button = self.exit_button_surf.get_rect(center=self.exit_button_pos)

        # 스토리 버튼 -> 스토리(배경) 설명 화면
        self.story_button_surf = pygame.image.load(f'{self.main_path}menu_story.png').convert_alpha() # 이미지 교체 필요
        self.story_button = self.exit_button_surf.get_rect(center=self.story_button_pos)

        # 키 설명 버튼 -> 키 설명 화면으로
        self.key_button_surf = pygame.image.load(f'{self.main_path}menu_key.png').convert_alpha() # 이미지 교체 필요
        self.key_button = self.exit_button_surf.get_rect(center=self.key_button_pos)

    def menu(self): # 맨 처음 시작. 메뉴 화면
        self.intro()
        while True:
            self.screen.blit(self.background_surf, self.background_rect)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 버튼 눌림 체크
            if self.is_clicked: # 버튼이 눌렸는데
                if self.start_button.collidepoint(mouse_x, mouse_y): # start button rect를 누르면
                    self.run() # 게임 시작
                elif self.ranks_button.collidepoint(mouse_x, mouse_y):
                    self.ranks() # 랭크 화면으로 이동
                elif self.exit_button.collidepoint(mouse_x, mouse_y):
                    # 게임 종료
                    pygame.quit()
                    sys.exit()
                elif self.story_button.collidepoint(mouse_x, mouse_y):
                    self.story_scene()
                elif self.key_button.collidepoint(mouse_x, mouse_y):
                    self.key_scene()

            # 이벤트 체크
            self.click_check()

            # 화면 업데이트
            self.screen.blit(self.start_button_surf, self.start_button)
            self.screen.blit(self.ranks_button_surf, self.ranks_button)
            self.screen.blit(self.exit_button_surf, self.exit_button)
            self.screen.blit(self.story_button_surf, self.story_button)
            self.screen.blit(self.key_button_surf, self.key_button)

            #self.fade_in()
            pygame.display.update()

    def ranks(self): # 랭킹 화면
        # 랭킹 정보 정렬 -> 이건 저장할 때 같이 해줘야하는 건데 일단 여기서 함. 나중에 필요 없으면 지울 것.
        sort_rank_file()
        ranking_list = ranking_info()
        while True:
            self.screen.fill(WHITE)
            centerx = WIDTH // 2
            centery = HEIGHT // 2
            leading = 50
            button_size = (50, 20)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 제목
            title_surf = LARGE_FONT.render("RANKING", True, RED)
            title_rect = title_surf.get_rect(center=(centerx, centery - 6 * leading))

            # 랭킹 정보 그리기
            rank_start_y = centery - 5 * leading # 랭킹 로그 시작할 y값

            if len(ranking_list) == 0: # 랭킹 정보가 아무것도 없으면
                surf = CONTENT_FONT.render("NO LOG", True, BLACK)
                rect = surf.get_rect(topleft=(centerx, centery))
                self.screen.blit(surf, rect)

            else: # 랭킹 정보가 하나라도 있으면
                for idx, info in enumerate(ranking_list):
                    surf = CONTENT_FONT.render(f"{idx} | {info[0]} : {info[1]}", True, BLACK)
                    rect = surf.get_rect(topleft=(centerx, rank_start_y + idx * leading))
                    self.screen.blit(surf, rect)

            # 다시 메뉴로 돌아가는 버튼
            back_to_menu_button = pygame.Rect((centerx, centery + 5 * leading), button_size)

            # 기록 초기화 버튼
            reset_rank_button = pygame.Rect((centerx, centery + 6 * leading), button_size)

            # 버튼 눌림 체크
            if self.is_clicked: # 버튼이 눌렸는데
                if back_to_menu_button.collidepoint(mouse_x, mouse_y): # back_to_menu_button rect를 누르면
                    return # ranks() 종료하고 메뉴로 돌아가기
                elif reset_rank_button.collidepoint(mouse_x, mouse_y): # reset_rank_button rect를 누르면
                    delete_rank_all() # rank/user_score.txt 안의 내용을 모두 삭제

            self.click_check()

            # 화면 업데이트
            self.screen.blit(title_surf, title_rect)
            pygame.draw.rect(self.screen, RED, back_to_menu_button)  # 메뉴로 돌아가는 버튼 그리기
            pygame.draw.rect(self.screen, GREEN, reset_rank_button)  # 랭킹 초기화 버튼 그리기

            pygame.display.update()

    # 메인 게임 실행 루프
    def run(self):
        self.level = Level()
        self.game_start_time = pygame.time.get_ticks()
        while True:
            time = (pygame.time.get_ticks() - self.game_start_time) / 1000 # 레벨1 시작부터 현재까지의 진행시간(초)-> 타이머
            self.level.time = time

            # 플레이어 인풋 받을 때 event 체크를 함. 그때 종료 조건 확인하기 때문에 여기서 할 필요 없지만 기능 분리를 위해 일단 살려놓음
            for event in pygame.event.get():
                quit_check(event)

            df = self.clock.tick(FPS) # 게임 화면의 초당 프레임 수를 설정
            self.level.run(df)  #df: 프레임
            pygame.display.update()  # 게임 화면을 다시 그리기!

            if self.level.done: # 게임 종료 플래그
                break # while 벗어나서 시간 저장하고 함수 실행 종료

        self.game_end_time = pygame.time.get_ticks()
        self.time_score = (self.game_end_time - self.game_start_time) / 1000 # 초 단위로 저장?

        # 게임 종료후, level에 저장된 게임 상태(플레이어가 클리어했는지 등)를 통해 다음 엔딩 씬이 정해짐
        # 클리어했을 경우 : 승리 축하 화면
        # 졌을 경우 : 패배 화면
        if self.level.is_clear: # 클리어했으면
            self.win()
        else: # 졌으면
            self.lose()

    def win(self):
        # 이겼으니까 user_name이랑 score 저장할 것.
        save_current_score(self.user_name, self.time_score) # 아직 user_name 창을 안 만들어서.. 일단 test name으로 저장함
        while True:
            self.screen.fill(BLACK)
            centerx = WIDTH // 2
            centery = HEIGHT // 2
            leading = 50
            button_size = (50, 20)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 제목
            title_surf = LARGE_FONT.render("YOU WIN!", True, WHITE)
            title_rect = title_surf.get_rect(center=(centerx, centery))

            # 다시 메뉴로 돌아가는 버튼
            back_to_menu_button = pygame.Rect((centerx, centery + 5 * leading), button_size)

            # 버튼 눌림 체크
            if self.is_clicked: # 버튼이 눌렸는데
                if back_to_menu_button.collidepoint(mouse_x, mouse_y): # back_to_menu_button rect를 누르면
                    return # 종료하고 menu()로 돌아가기

            self.click_check()

            # 화면 업데이트
            self.screen.blit(title_surf, title_rect)
            pygame.draw.rect(self.screen, RED, back_to_menu_button)  # 메뉴로 돌아가는 버튼 그리기

            pygame.display.update()

    def lose(self): # 수정필요
        while True:
            self.screen.fill(BLACK)
            centerx = WIDTH // 2
            centery = HEIGHT // 2
            leading = 50
            button_size = (50, 20)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 제목
            title_surf = LARGE_FONT.render("YOU LOSE!", True, WHITE)
            title_rect = title_surf.get_rect(center=(centerx, centery))

            # 다시 메뉴로 돌아가는 버튼
            back_to_menu_button = pygame.Rect((centerx, centery + 5 * leading), button_size)

            # 버튼 눌림 체크
            if self.is_clicked:  # 버튼이 눌렸는데
                if back_to_menu_button.collidepoint(mouse_x, mouse_y):  # back_to_menu_button rect를 누르면
                    return  # 종료하고 menu()로 돌아가기

            self.click_check()

            # 화면 업데이트
            self.screen.blit(title_surf, title_rect)
            pygame.draw.rect(self.screen, RED, back_to_menu_button)  # 메뉴로 돌아가는 버튼 그리기

            pygame.display.update()

    def click_check(self):
        self.is_clicked = False
        for event in pygame.event.get():
            quit_check(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_clicked = True

    def intro(self): # 처음 시작화면.
        intro_number = 1
        while True:
            if intro_number == 1: # 게임 이름 화면
                self.screen.blit(self.start_surf, self.start_rect)

            elif intro_number == 2: # 게임 배경(스토리) 설명 화면
                self.screen.blit(self.story_surf, self.story_rect)

            elif intro_number == 3: # 게임 키 설명 화면
                self.screen.blit(self.key_surf, self.key_rect)
            else:
                return

            # 엔터키 누르면 다음 화면으로 넘어감. + intro_number == 4 가 되면 intro() 종료하고 메뉴로 넘어감.
            if self.is_return_key_pressed():
                intro_number += 1

            self.fade_in()
            pygame.display.update()

    def story_scene(self): # 메뉴에서 스토리 버튼 누르면 함수 실행
        while True:
            self.screen.blit(self.story_surf, self.story_rect)
            if self.is_return_key_pressed(): # 엔터 키 누르면
                return # 종료
            pygame.display.update()

    def key_scene(self): # 메뉴에서 키 버튼 누르면 함수 실행
        while True:
            self.screen.blit(self.key_surf, self.key_rect)
            if self.is_return_key_pressed(): # 엔터 키 누르면
                return # 종료
            pygame.display.update()

    def is_return_key_pressed(self):
        for event in pygame.event.get():
            quit_check(event)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    return True
        return False

    def fade_in(self):
        # alpha 값 조절해서 fade in 효과 내기
        # scene 생성 후 alpha 값이 차츰 작아지다가 0 보다 작아지면 alpha 는 계속 0을 유지한다.
        # scene 삭제 시 fade_out 함수를 호출하면 alpha 값이 다시 차츰 높아지게 한다.
        self.alpha -= 30 if self.alpha > 0 else 0
        self.fade_surf.set_alpha(self.alpha)
        self.screen.blit(self.fade_surf, (0, 0))

    def fade_out(self): # 장면 전환시, 다음 장면 생성 전에 이 함수를 호출하자
        for alpha in range(0, 300):
            self.fade_surf.set_alpha(alpha)
            self.display_surface.blit(self.fade_surf, (0, 0))
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.menu()