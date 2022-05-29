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

    def menu(self): # 맨 처음 시작. 메뉴 화면
        while True:
            self.screen.fill(BLACK)
            centerx = WIDTH//2
            centery = HEIGHT//2
            leading = 50
            button_size = (50, 20)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 제목
            title_surf = LARGE_FONT.render("DEVIL's CASTLE", True, RED)
            title_rect = title_surf.get_rect(center=(centerx, centery - 2 * leading))

            # 유저 네임 입력 창

            # 시작 버튼 -> intro 보여주고 run() 실행 ->
            start_button = pygame.Rect((centerx, centery), button_size)

            # 랭킹 버튼 -> ranks() 실행 (랭킹화면)
            ranks_button = pygame.Rect((centerx, centery + leading), button_size)

            # 종료 버튼 -> 게임 종료, 화면 닫음
            exit_button = pygame.Rect((centerx, centery + 2 * leading), button_size)

            # 버튼 눌림 체크
            if self.is_clicked: # 버튼이 눌렸는데
                if start_button.collidepoint(mouse_x, mouse_y): # start button rect를 누르면
                    self.run() # 게임 시작
                elif ranks_button.collidepoint(mouse_x, mouse_y):
                    self.ranks() # 랭크 화면으로 이동
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    # 게임 종료
                    pygame.quit()
                    sys.exit()

            # 이벤트 체크
            self.click_check()

            # 화면 업데이트
            self.screen.blit(title_surf, title_rect)
            pygame.draw.rect(self.screen, RED, start_button) # 시작 버튼 그리기
            pygame.draw.rect(self.screen, GREEN, ranks_button) # 랭킹 버튼 그리기
            pygame.draw.rect(self.screen, BLUE, exit_button) # 종료 버튼 그리기

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

if __name__ == '__main__':
    game = Game()
    game.menu()