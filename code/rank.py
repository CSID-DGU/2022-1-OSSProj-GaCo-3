from os import walk
import pygame, sys
from settings import *
from player import *
from level import *

# 고민 : support.py에 함수를, settings에 아래의 RANK_FILE_PATH를 저장해서 쓸까?
#       아니면 그냥 이렇게 따로 rank.py 에서 랭킹 관련 일을 모두 정의할까? -> 이게 더 나은가..? 복잡하지 않게?

RANK_FILE_PATH = "rank/user_score.txt"

# user name과 score를 입력받아 user_score.txt의 마지막 줄에 저장
def save_current_score(user_name, time_score):
    data = f"{user_name}, {time_score}\n"
    rank_file = open(RANK_FILE_PATH, 'a')
    rank_file.write(data)
    rank_file.close()

# user_score.txt 의 기록들을 순위에 따라 정렬하여 저장
def sort_rank_file():
    result = "" # 마지막에 다시 저장해줄 rank content
    rank_file = open(RANK_FILE_PATH, 'r') # 읽기 모드로 파일 열기
    lines = rank_file.readlines() # rank file의 각 라인의 string을 담은 list
    rank_file.close() # 파일 닫기

    # 파일에 아무 내용도 없을 경우
    if len(lines) == 0:
        return

    rank_dict = {}
    for line in lines: # 한 줄 한 줄 읽어서 rank_dict에 'user_name':score 형태로 저장
        line = line.rstrip()
        line = line.split(',')
        user_name, score = line[0], float(line[1].strip())
        rank_dict[user_name] = score

    # 딕셔너리를 score(value) 기준으로 정렬하기
    sorted_rank_dict_list = sorted(rank_dict.items(), key=lambda item: item[1]) # 리스트됨

    for idx, dict_content in enumerate(sorted_rank_dict_list):
        if idx == 9: # 상위 10개만 저장하기
            break
        key, value = dict_content
        data = f"{key}, {rank_dict[key]}\n"
        result += data

    # rank_file 에 정렬한 내용 저장하기
    rank_file = open(RANK_FILE_PATH, 'w') # 쓰기 모드로 파일 열기
    rank_file.write(result) # 결과 저장하기
    rank_file.close() # 파일 닫기

# 순위 기록 모두 지우기
def delete_rank_all():
    rank_file = open(RANK_FILE_PATH, 'w')
    rank_file.write("")
    rank_file.close()


# 랭킹 화면 그릴 때 사용할 랭킹 파일 읽어오는 함수
def ranking_info() -> list: # 이중 리스트 반환. list = [[user_name, score], ...]
    ranking_list = []

    rank_file = open(RANK_FILE_PATH, 'r')
    lines = rank_file.readlines()
    rank_file.close()

    for line in lines:
        line = line.split(',')
        user_name, score = map(str, line)
        ranking_list.append([user_name, score])

    return ranking_list

# 테스트용 출력
def print_rank_file():
    rank_file = open(RANK_FILE_PATH, 'r')
    lines = rank_file.readlines()
    rank_file.close()
    for line in lines:
        print(line, end="")