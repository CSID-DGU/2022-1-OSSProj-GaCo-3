#-*-coding:utf-8-*-
import time
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
        self.user_name = "클릭 후 이름 입력"
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
        # 메뉴 레이아웃
        self.leading = 50

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


        # 랭킹 화면
        self.ranks_background_surf = pygame.image.load(f'{self.main_path}ranks.png').convert_alpha()
        self.ranks_background_rect = self.ranks_background_surf.get_rect(topleft=(0, 0))

        # 랭킹 화면 버튼들
        # 메뉴로 돌아가는 버튼
        self.back_to_menu_button_surf = pygame.image.load(f'{self.main_path}btn_to_menu.png').convert_alpha()
        self.back_to_menu_button = self.back_to_menu_button_surf.get_rect(center=self.story_button_pos)

        # 랭킹 기록 초기화 버튼
        self.delete_button_surf = pygame.image.load(f'{self.main_path}ranks_delete.png').convert_alpha()
        self.delete_button = self.delete_button_surf.get_rect(center=self.key_button_pos)


        # 메뉴 화면 버튼들
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


        # 이겼을 때 배경화면
        self.win_background_surf = pygame.image.load(f'{self.main_path}clear_background.png').convert_alpha()
        self.win_background_rect = self.win_background_surf.get_rect(topleft=(0, 0))

        # 이겼을 때, 저장 후 배경화면
        self.win_background_after_save_surf = pygame.image.load(f'{self.main_path}clear_background_after_save.png').convert_alpha()
        self.win_background_after_save_rect = self.win_background_after_save_surf.get_rect(topleft=(0, 0))

        # 이겼을 때, 기록 저장 버튼
        self.save_button_surf = pygame.image.load(f'{self.main_path}save_button.png').convert_alpha()
        self.save_button = self.save_button_surf.get_rect(center=self.start_button_pos)

        # 이겼을 때, 유저 텍스트 인풋 커서
        self.text_cursor = pygame.image.load(f'{self.main_path}text_cursor.png').convert_alpha()

        # 졌을 때 배경화면
        self.lose_background_surf = pygame.image.load(f'{self.main_path}lose_background.png').convert_alpha()
        self.lose_background_rect = self.lose_background_surf.get_rect(topleft=(0, 0))

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

    # 랭킹 정보 그리기
    def ranks_draw(self, ranking_list):
        # 이름, 순위 공통의 시작 y축이 필요
        rank_start_y = HEIGHT // 3 + 20

        # 이름 center x 축이 필요하고
        name_centerx = WIDTH // 2 - 105

        # 순위 center x 축이 필요하다
        rank_centerx = (WIDTH // 3) * 2 + 65

        # 순위 사이의 간격도 확인해야함
        rank_leading = 38

        if len(ranking_list) == 0:  # 랭킹 정보가 아무것도 없으면
            surf = MENU_FONT.render("NO LOG", True, WHITE)
            rect = surf.get_rect(center=(name_centerx, HEIGHT // 2))
            self.screen.blit(surf, rect)

        else:  # 랭킹 정보가 하나라도 있으면
            for idx, info in enumerate(ranking_list):
                name_surf = CONTENT_FONT.render(info[0], True, WHITE)
                rank_surf = CONTENT_FONT.render(info[1].strip(), True, WHITE)

                name_rect = name_surf.get_rect(center=(name_centerx, rank_start_y + rank_leading * idx))
                rank_rect = rank_surf.get_rect(center=(rank_centerx, rank_start_y + rank_leading * idx))

                self.screen.blit(name_surf, name_rect)
                self.screen.blit(rank_surf, rank_rect)

    def ranks(self): # 랭킹 화면
        # 랭킹 정보 정렬 -> 이건 저장할 때 같이 해줘야하는 건데 일단 여기서 함. 나중에 필요 없으면 지울 것.
        sort_rank_file()
        ranking_list = ranking_info()
        while True:
            self.screen.blit(self.ranks_background_surf, self.ranks_background_rect)
            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.ranks_draw(ranking_list)

            # 버튼들
            self.screen.blit(self.back_to_menu_button_surf, self.back_to_menu_button) # 다시 메뉴로 돌아가는 버튼
            self.screen.blit(self.delete_button_surf, self.delete_button)  # 기록 초기화 버튼

            # 버튼 눌림 체크
            if self.is_clicked: # 버튼이 눌렸는데
                if self.back_to_menu_button.collidepoint(mouse_x, mouse_y): # back_to_menu_button rect를 누르면
                    return # ranks() 종료하고 메뉴로 돌아가기
                elif self.delete_button.collidepoint(mouse_x, mouse_y): # reset_rank_button rect를 누르면
                    delete_rank_all() # rank/user_score.txt 안의 내용을 모두 삭제
                    sort_rank_file()
                    ranking_list = ranking_info()
                    self.ranks_draw(ranking_list)

            self.click_check()
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

    def user_input(self, input_box_width):
        # input_box_width가 250 이상되면 더 입력못하게 하자
        for event in pygame.event.get():
            quit_check(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_name = self.user_name[:-1]
                else:
                    if input_box_width > 250: #일정 크기 이상을 넘어가면 유저인풋을 받지 않기.
                        pass
                    else:
                        self.user_name += event.unicode

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_clicked = True

    def user_name_mdify(self):
        if self.user_name == "클릭 후 이름 입력": # 초기값
            self.user_name == ""

        replace_chars = [' ', ','] # 공백문자, 쉼표는 제거
        for char in replace_chars:
            if char in self.user_name:
                self.user_name = self.user_name.replace(char, "")

    def win(self): # True를 반환하면 다시 시작
        self.user_name = "클릭 후 이름 입력"
        name_rank_centerx = WIDTH//2 + 80
        name_y = HEIGHT // 2 + 40
        rank_y = HEIGHT // 2 - 40
        name_input_box_rect = pygame.Rect((0, 0), (50, 40))
        color_active = WHITE
        color_passive = (50, 50, 50) # 회색
        color = color_passive
        input_active = False

        # 저장버튼을 한 번이라도 눌렀으면 다시 저장 못하게 하고 메뉴로 돌아가라는 메세지만 띄우기
        is_saved = False

        # # 유저 인풋 박스에서 사용자 입력을 기다리는 커서
        # line_color = 0
        # input_line_color = (line_color, line_color, line_color)  # 인풋 박스가 활성화되면 깜빡거리게 하기

        while True:
            if not is_saved:
                self.screen.blit(self.win_background_surf, self.win_background_rect)
            else:
                self.screen.blit(self.win_background_after_save_surf, self.win_background_after_save_rect)

            # mouse info
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.is_clicked: # 버튼이 눌렸는데
                if name_input_box_rect.collidepoint(mouse_x, mouse_y) and not is_saved: # 인풋박스를 누르면
                    if self.user_name == "클릭 후 이름 입력": # 처음 클릭했을 때만 이름 삭제
                        self.user_name = ""
                    input_active = True
                else:
                    input_active = False

            self.is_clicked = False

            if input_active:
                color = color_active
                line_color = 255 if time.time() % 1 > 0.5 else 0 # 커서가 깜빡일 수 있게
            else:
                color = color_passive
                line_color = 0

            # 커서 색 바꾸기
            input_line_color = (line_color, line_color, line_color)

            # 이벤트 체크, 유저 인풋 받기
            for event in pygame.event.get():
                quit_check(event)
                if event.type == pygame.KEYDOWN:
                    if input_active: # 유저인풋 박스가 활성화되었을 때만 입력받기
                        pygame.draw.line(self.screen, input_line_color, name_input_box_rect.bottomleft,
                                         name_input_box_rect.bottomright)
                        if event.key == pygame.K_BACKSPACE:
                            self.user_name = self.user_name[:-1]

                        elif event.key == pygame.K_RETURN:  # 엔터 누르면 다시 인풋박스를 인에이블 상태로
                            input_active = False
                            color = color_passive

                        else:
                            if name_input_box_rect.w > 250:  # 일정 크기 이상을 넘어가면 유저인풋을 받지 않기.
                                pass
                            else:
                                self.user_name += event.unicode

                if event.type == pygame.MOUSEBUTTONUP:  # 클릭 체크
                    if event.button == 1:
                        self.is_clicked = True

            self.screen.blit(self.save_button_surf, self.save_button)  # 저장 버튼 그리기
            self.screen.blit(self.back_to_menu_button_surf, self.back_to_menu_button) #다시 돌아가기 버튼

            # 저장 버튼 눌렸을 경우
            if self.is_clicked: # 버튼이 눌렸는데
                if self.save_button.collidepoint(mouse_x, mouse_y): # start button rect를 누르면
                    self.user_name_mdify() # 유저네임 가공
                    if len(self.user_name) == 0: # 유저네임이 아무것도 입력되지 않았다면
                        print('no user name')
                        # 경고창을 띄우기

                    else: # 유저네임에 어떤 글자가 들어가 있다면
                        save_current_score(self.user_name, self.time_score) # 기록파일에 유저네임과 점수 저장
                        is_saved = True  # 저장했다는 플래그
                        # 저장했다는 알림, 메뉴로 돌아가세요라고 안내하기

                elif self.back_to_menu_button.collidepoint(mouse_x, mouse_y): # 돌아가기 버튼 눌릴 경우
                    return # 함수 종료, 메뉴로 돌아가기

            # 인풋박스 그리기
            line_start_position = name_input_box_rect.bottomright - pygame.Vector2(30, 5)
            line_end_position = name_input_box_rect.bottomright - pygame.Vector2(10, 5)
            pygame.draw.rect(self.screen, color, name_input_box_rect, 2)
            if input_active:
                pygame.draw.line(self.screen, input_line_color, line_start_position, line_end_position, 5)

            # 사용자 이름 사각형
            user_name_surf = CONTENT_FONT.render(self.user_name, True, color)
            name_input_box_rect.center = (name_rank_centerx, name_y)
            self.screen.blit(user_name_surf, (name_input_box_rect.x + 10, name_input_box_rect.y))
            name_input_box_rect.w = user_name_surf.get_width() + 40

            # 방금 전 게임 기록 렌더링
            score = str(self.time_score)
            time_score_surf = CONTENT_FONT.render(score, True, WHITE)
            time_score_rect = time_score_surf.get_rect(center=(name_rank_centerx, rank_y))
            self.screen.blit(time_score_surf, time_score_rect)

            # 화면 업데이트
            pygame.display.update()

    def lose(self):
        while True:
            self.screen.blit(self.lose_background_surf, self.lose_background_rect)

            if self.is_return_key_pressed():
                return

            # 화면 업데이트
            pygame.display.update()

    def click_check(self): # 버튼을 눌렀다 뗐을 때를 감지
        self.is_clicked = False
        for event in pygame.event.get():
            quit_check(event)

            if event.type == pygame.MOUSEBUTTONUP:
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