"""
설명 :
게임 창화면 크기 : 1920 * 1080
스킨 : D3 로 설정
프로그램 종료 : b
버프 시작/종료 : y
  L-- 성기사 : 신성한방패 : F6 으로 설정한다.


pip install pyautogui
pip install opencv-python      # cv2 설치
pip install pillow             # PIL 설치
pip install keyboard
"""

import pyautogui as pag
import time
import random
import keyboard
import cv2
import sys
import os
from datetime import datetime
from PIL import ImageGrab

# =====[함수 영역] (시작) =========================================
# 풍차 함수의 global 변수 초기화
mCount = 0


# ===[함수]=== 실행 중임을 나타내는 풍차를 출력하는 함수
def printWindmill():
    global mCount
    spin_char = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    mCount += 1
    if mCount == len(spin_char):
        mCount = 0
    return spin_char[mCount]


# ===[함수]=== 출력 일시를 함께 표시하는 print 함수
def printTimeMsg(pMsg, pBr=0):
    dt = datetime.now()
    dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
    if pBr == 0:
        print("[", dtStr, "] ", pMsg)
    else:
        print("\r[", dtStr, "] ", pMsg, end="")


# ===[함수]=== 출력시 글자의 색상을 지정한다.
def msgColor(pColorName, pText):
    pColorName = pColorName.upper()
    color_dic = {
        "RED": "31",
        "GREEN": "32",
        "YELLOW": "33",
        "BLUE": "34",  # 글자색
        "RRED": "41",
        "RGREEN": "42",
        "RYELLOW": "43",
        "RBLUE": "44",  # 배경색
    }.get(pColorName, "색상명오류")
    return "\033[" + color_dic + "m" + pText + "\033[m"


# ===[함수]=== 상태 메세지 출력 처리 함수
def get_KeyMsg(pHelperFlag=False, pBufferTime="", pGoatmanFlag=False):
    mKeyMsg = " "
    if pHelperFlag:
        mKeyMsg += msgColor("rGreen", " ( 용병 )")
    else:
        mKeyMsg += " ( 용병 "
    if pBufferTime == "":
        mKeyMsg += " ]=버프 "
    else:
        mKeyMsg += msgColor("rGreen", " ]=버프 [" + pBufferTime + "s]")
    if pGoatmanFlag:
        mKeyMsg += msgColor("rGreen", " [=염소인간소환 ")
    else:
        mKeyMsg += " [=염소인간소환 "
    mKeyMsg += " 0=종료 9=캡쳐 8=일시정지     "
    return mKeyMsg


# ===[함수]=== RGB값을 받아 색상을 판별하는 함수
#   RGB(87,72,48) 빨강이지만 붉은끼만 있는것
def get_cName(pRgb_dic):
    p1 = pRgb_dic[0]
    p2 = pRgb_dic[1]
    p3 = pRgb_dic[2]
    mGapMin = 30  # 다른 색상과의 최소 이정도 차이는 나야 색구분이 된다일때 그 임의 설정값
    if p1 > 240 and p2 > 240 and p3 > 240:
        return "white"
    elif (p1 > 70 and p1 < 113) and (p2 >= 0 and p2 < 7) and (p3 > 70 and p3 < 120):
        return "violet"
    elif (p1 > p2 and p1 > p3) and (p1 - p2 > mGapMin and p1 - p3 > mGapMin):
        return "red"
    elif (p2 > p1 and p2 > p3) and (p2 - p1 > mGapMin and p2 - p3 > mGapMin):
        return "green"
    elif (p3 > p1 and p3 > p2) and (p3 - p1 > mGapMin and p3 - p2 > mGapMin):
        return "blue"
    if p1 < 50 and p2 < 50 and p3 < 50:
        return "black"
    else:
        return "unknown" + str(p1) + "/" + str(p2) + "/" + str(p3)


# ===[함수]=== 화면에 출력해주는 함수 (시작)
def printMsg(pPosDic, pColor, pTitle, pag1):
    tPos = pPosDic
    pag1.moveTo(tPos[0], tPos[1])
    print(pTitle + " 확인 ==> ", end=" ")
    print(" 모니터 절대 좌표 xy위치 : (" + str(tPos[0]) + "," + str(tPos[1]) + ") 로 이동", end=" ")
    print(" / 컬러 : " + pColor)
    time.sleep(1)


# ===== 프로그램 실행 영역 (종료) ===================================
