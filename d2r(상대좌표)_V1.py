"""
설명 :
게임 창화면 크기 : 1920 * 1080
스킨 : D3 로 설정
프로그램 종료 : 0
버프 시작/종료 : ]
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

# from d2r_con_paladin import *  # 팔라딘 캐릭터 설정값
# from d2r_con_sorcer import *  # 소서리스 캐릭터 설정값
from d2r_con_worlock import *  # 워록 캐릭터 설정값
from imp_d2r import *  # 함수 영역
from imp_ocr import *

# ===== 실행 환경 설정값 설정 (시작) ================================
# ===== 사용자 지정 환경 설정값 설정 (시작) =====
mPotionTime = 5  # 포션 연속 먹는 딜레이 초 간격
posTest = 0  # posTest = 0 : 정상 동작
#            # posTest = 1 : 좌표위치 및 색상 테스트 모드 동작

# 화면 체크하는 좌표 위치 설정
#   게임 화면이 창모드(1920*1080) 일때 사용하는 값임
#   아래는 active window info 프로그램에서 relative(상대좌표) 값임
#   * 실행하면 캡쳐 기능있는데 그걸로 캡쳐하여 위치 확인해 입력하면됨
pTopXY = (475, 950)  # 피 구슬 상단 y좌표 (상단,하단 좌표 입력은 %물약 먹는 위치 계산 위함)
pLowXY = (475, 1097)  # 피 구슬 하단 y 좌표
mTopXY = (1450, 950)  # 엠 구슬 상단 y좌표
mLowXY = (1450, 1097)  # 엠 구슬 하단 y좌표
yLeftXY = (35, 60)  # 용병 피바 좌측 끝 지점
yRightXY = (90, 60)  # 용병 피바 우측 끝 지점
pGoatmanXY = (140, 60)  # 염소인간 피바 좌측 끝 지점 - 이거 없다면 죽은것이므로 다시 살려야됨
cPos1 = (502, 995)  # 게임화면인지 확인하는 체크포인트 (피약의 반사처리되는 부분(흰색))
xStartP = 1125
yHoldP = 1086
slotXy = ((xStartP, yHoldP), (xStartP + (62 * 1), yHoldP), (xStartP + (62 * 2), yHoldP), (xStartP + (62 * 3), yHoldP))  # 물약 벨트 슬롯 좌표(슬롯1 xy좌표, 슬롯2 xy좌표, ...)
# ===== 사용자 지정 환경 설정값 설정 (종료)

# ===== 변수 기본값 설정 (시작)
# 피 채우는 최소값이 20% 이하로 가지 않도록 한다
mAutoMin = 30
# 피 채우는 최대값이 80% 이하로 가지 않도록 한다
mAutoMax = 80

# 물약 회복량으로 체크할 % 위치 계산
if pReProSet > 0:
    pRePro = pReProSet
else:
    pRePro = int((pFull - pBottle) * 100 / pFull)  # %이하로 떨어지면 피약사용 할 %계산  //살짝 일찍 먼저 먹게하기위해 10% 보정
    if pRePro < mAutoMin:
        pRePro = mAutoMin
    if pRePro > mAutoMax:
        pRePro = mAutoMax

if mReProSet > 0:
    mRePro = mReProSet
else:
    mRePro = int((mFull - mBottle) * 100 / mFull)  # %이하로 떨어지면 엠약사용 할 %계산
    if mRePro < mAutoMin:
        mRePro = mAutoMin
    if mRePro > mAutoMax:
        mRePro = mAutoMax

if yReProSet > 0:
    yRePro = yReProSet
else:
    yRePro = int((yFull - pBottle) * 100 / yFull)  # 용병 피약 사용 % 위치 (용병도 캐릭터 피약 같이 사용함) 용병 10% 만큼 내려 너무 자주 사용안하게 한다
    if yRePro < mAutoMin:
        yRePro = mAutoMin
    if yRePro > mAutoMax:
        yRePro = mAutoMax

# 물약 사용여부 체크할 % 값으로 체크할 화면 좌표 계산
pRange = pLowXY[1] - pTopXY[1]
pY = pTopXY[1] + (pRange - int(pRange * pRePro / 100))
mRange = mLowXY[1] - mTopXY[1]
mY = mTopXY[1] + (mRange - int(mRange * mRePro / 100))
yX = yLeftXY[0] + int((yRightXY[0] - yLeftXY[0]) / 100 * yRePro)
pPos1 = (pTopXY[0], pY)  # 피약 먹을 위치 확인 지점
mPos1 = (mTopXY[0], mY)  # 엠약 먹을 위치 확인 지점
yPos1 = (yLeftXY[0], yLeftXY[1])  # 용병은 2개의 포인트를 체크하여 최소지점 이하면 죽은걸로 간주하여 물약 처리 안함
yPos2 = (yX, yRightXY[1])  # 용병 피약 먹을 위치 확인 지점
# 비상상태 물약 사용여부 체크할 % 값으로 체크할 화면 좌표 계산
pRange = pLowXY[1] - pTopXY[1]
pEmerY = pTopXY[1] + (pRange - int(pRange * emergencyProSet / 100))
yEmerX = yLeftXY[0] + int((yRightXY[0] - yLeftXY[0]) / 100 * emergencyProSet)
pEmerPos1 = (pTopXY[0], pEmerY)  # 피약 먹을 위치 확인 지점
yEmerPos1 = (yEmerX, yRightXY[1])  # 용병 피약 먹을 위치 확인 지점

# 물약 사용 딜레이 시간 변수 초기값 부여
pStartTime = time.time() - mPotionTime  # 피약 먹은 시간 변수
mStartTime = time.time() - mPotionTime  # 엠약 먹는 시간 변수
yStartTime = time.time() - mPotionTime  # 용병 피약 먹는 시간 변수

# 버프변수 초기화
mBuffFlag = False  # 버프 사용 여부
mBuff1Time = ""  # 버프 남은 시간 저장 변수
mGoatmanFlag = False  # 염소인간 자동 소환 실행 여부 체크 변수

# 용병 물약 먹기 실행 on/off 변수 초기화
mHelperFlag = False

# 물약 상태 문구를 1번만 출력하게 하는 변수 초기화
pHelpMsgYN = 1

# 마을명
vill_dict = {"자매단 야영지":True, "루트 골레인":True, "쿠라스트 부두":True, "혼돈의 요새":True, "하가로스":True}

# 프로그램이 실행되는 폴더 위치 조회
try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(os.path.abspath(__file__))
# ===== 변수 기본값 설정 (종료)
# ===== 실행 환경 설정값 설정 (종료) ================================

# ===== 프로그램 실행 영역 (시작) ===================================
# 물약 경고 처리
if pFull - pBottle <= 0:
    print(" [경고] 피통보다 물약이 큽니다. 확인후 수정하시기 바랍니다.")

if mFull - mBottle <= 0:
    print(" [경고] 마나통보다 마나물약이 큽니다. 확인후 수정하시기 바랍니다.")

if pRePro <= 50:
    print(" ")
    print(" *** [경고] HP약 체크가 50%이하로 한번에 죽을수있습니다. *** ")
    print(" ")

sys.stdout.write("\033[?25l")  # 커서 숨기기
sys.stdout.flush()

mHelperFlag = True  # 용병 물약 먹기 기능 항상 on
mPauseFlag = False  # 일시정지 기능 처리

# 무한 반복하며 화면을 확인하고 처리하는 while 영역 (시작)
while True:
    time.sleep(0.2)  # 무한루프의 cpu 점유율을 낮추기 위해 잠시 대기 (0.2초)

    if keyboard.is_pressed("0"):  # or keyboard.is_pressed('Y'):
        sys.stdout.write("\033[?25h")  # 커서 보이기
        sys.stdout.flush()
        print("")
        print(" 프로그램을 종료 합니다.")
        break

    if keyboard.is_pressed("8"):  # 프로그램 일시정지 기능
        if mPauseFlag:
            mPauseFlag = False
        else:
            mPauseFlag = True
            print("")
            print(" 프로그램을 일시중지 중 입니다.... 8=재실행, 0=종료     ")
            time.sleep(0.5)

    if mPauseFlag:
        continue

    if keyboard.is_pressed("]"):  # or keyboard.is_pressed('K'):
        if mBuffFlag:  # 버프 실행 토글 처리
            mBuffFlag = False
            mBuff1Time = ""
            # print(" 자동 버프 기능을 종료 합니다.")
        else:
            mBuffFlag = True
            mStartTimeBuff1 = time.time() - mBuff1[3]  # 버프 시작시간 설정
            # print(" 자동 버프 기능을 실행 합니다.")

    if keyboard.is_pressed("["):
        if mGoatmanFlag:  # 염소인간 자동 소환 실행 토글 처리
            mGoatmanFlag = False
            # print(" 염소인간 자동 소환 기능을 종료 합니다.")
        else:
            mGoatmanFlag = True
            # print(" 염소인간 자동 소환 기능을 실행 합니다.")

    """
    if keyboard.is_pressed('[') : #or keyboard.is_pressed('L'):

        if mHelperFlag :                                  # 용병 물약 실행 토글 처리
            mHelperFlag = False
            #print(" 용병 물약 기능을 종료 합니다.")
        else :
            mHelperFlag = True
            #print(" 용병 물약 기능을 실행 합니다.")
    """
    if keyboard.is_pressed("9"):
        # 전체화면 캡쳐 (제목타이틀 포함 그래야 캡쳐 이미지 좌표값이 프로그램 코드 좌표와 1:1 매칭됨)
        img1 = ImageGrab.grab((fw.left, fw.top, fw.right, fw.bottom))
        dt = datetime.now()
        dtStr = dt.strftime("%Y%m%d_%H%M%S")
        base_path = "C:\\currdata\\바탕화면"  # 주석처리하면 프로그램 소스 경로에 저장됨
        img1.save(base_path + "\\D2R_" + dtStr + ".png")
        print("바탕화면에 화면을 캡쳐 했습니다.")

    # 게임창이 활성화 되었는지 여부 확인
    #   게임창에서만 키값을 입력하고 화면을 체크하도록 하기 위해서
    fw = pag.getActiveWindow()
    try:
        winTitle = fw.title
    except AttributeError as err:
        winTitle = ""
    if winTitle != "Diablo II: Resurrected":  # 디아블로 게임 화면 일때만 동작하게 한다.
        # dt = datetime.now()
        # dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
        # print("[",dtStr,"] ")
        if pHelpMsgYN == 1:  # 물약 메세지는 한번만 출력한다.
            print("")
            print(" Hp max: " + str(pFull) + ", 1병회복량: " + str(pBottle) + ", 체크지점: " + str(pRePro) + " %, 비상체크지점: " + str(emergencyProSet) + " %")
            print(" Mp max: " + str(mFull) + ", 1병회복량: " + str(mBottle) + ", 체크지점: " + str(mRePro) + " %")
            print(" 용병 Hp max: " + str(yFull) + ", 1병회복량: " + str(pBottle) + ", 체크지점: " + str(yRePro) + " %, 비상체크지점: " + str(emergencyProSet) + " %")
            pHelpMsgYN = 0
        printTimeMsg(" -- " + str(printWindmill() + " 게임창을 활성화해야 합니다.  --"), 1)
        continue
    else:
        pHelpMsgYN = 1

    # 화면을 캡쳐하여 색상정보를 추출한다.
    screen = ImageGrab.grab((fw.left, fw.top, fw.right, fw.bottom))
    pRgb1 = screen.getpixel(pPos1)  # hp
    mRgb1 = screen.getpixel(mPos1)  # mp
    yRgb1 = screen.getpixel(yPos1)  # 용병 피 바 1
    yRgb2 = screen.getpixel(yPos2)  # 용병 피 바 2 용병이 죽었는지 확인용
    gRgb1 = screen.getpixel(pGoatmanXY)  # 염소인간 피바 좌측 끝 지점
    cRgb1 = screen.getpixel(cPos1)  # 게임 화면인지 체크하기 위한 포인트
    pEmerRgb1 = screen.getpixel(pEmerPos1)  # 캐릭 피 바 비상상태 체크 포인트
    yEmerRgb1 = screen.getpixel(yEmerPos1)  # 캐릭 피 바 비상상태 체크 포인트
    pRes1 = get_cName(pRgb1)  # 추출한 rgb값의 색상을 구분한다.
    mRes1 = get_cName(mRgb1)
    yRes1 = get_cName(yRgb1)
    yRes2 = get_cName(yRgb2)
    gRes1 = get_cName(gRgb1)  # 염소인간 피바 좌측 끝 지점
    cRes1 = get_cName(cRgb1)
    pEmerRes1 = get_cName(pEmerRgb1)
    yEmerRes1 = get_cName(yEmerRgb1)

    #screen.save(base_path + "\\cap_ocr.png")

    #우측상단 마을명 ocr
    x, y, x2, y2 = 1750, 87, 1917, 107
    ocr_vill_name = myOcr(screen,  x, y, x2, y2)

    # hp 량 ocr
    x, y, x2, y2 = 386, 900, 570, 926
    aa = str(myOcr(screen, x, y, x2, y2, "NUM_ONLY"))
    result = aa.split('/')
    ocr_hp_curr = result[0]
    ocr_hp_full = result[1]

    # mp 량 ocr
    x, y, x2, y2 = 1300, 900, 1570, 926
    aaa = str(myOcr(screen, x, y, x2, y2,"NUM_ONLY"))
    result = aaa.split('/')
    ocr_mp_curr = result[0]
    ocr_mp_full = result[1]

    #print(" ocr ==> ",ocr_vill_name,aa,aaa)
    print(" ocr ==> ",ocr_vill_name,aa,ocr_hp_curr,ocr_hp_full,aaa, ocr_mp_curr,ocr_mp_full)

    # ===== 테스트 모드 일때 처리 영역
    if posTest == 1:
        time.sleep(1)
        print("")
        print("")
        print(" 활성창 명 : " + fw.title)  # Diablo II: Resurrected
        print(" 창크기 : ", fw.size)  # 실행 창의 크기 정보(width, height), Size(width=1938, height=1060)
        print(" 창 좌표 좌상(x,y) 우하(x,y) : (", fw.left, fw.top, ") (", fw.right, fw.bottom, ")")  # 실행 창의 좌표 정보, -9 -9 1929 1051
        # pyautogui.click(fw.left + 25, fw.top + 20)  # 실행 창을 줄이거나 이동해도 해당 위치에서 마우스 클릭이 됨

        dt = datetime.now()
        dtStr = dt.strftime("%Y%m%d%H%M%S")
        # screen.save(base_path+"\\D2R_test"+dtStr+".png")       # 화면을 캡쳐한다.

        print("")
        mTmpXY = yPos1
        # 마우스 포인터는 모니터의 절대좌표로 지정해야 하기 때문에 fw.left처럼 창의 위치값을 더해준다.
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), yRes1, " 용병 hp 최저 지점", pag)
        mTmpXY = yEmerPos1
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), yEmerRes1, " 용병 hp 비상상태 : " + str(emergencyProSet) + "% 지점", pag)
        mTmpXY = yPos2
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), yRes2, " 용병 hp " + str(yRePro) + "% 지점", pag)

        mTmpXY = pPos1
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), pRes1, " HP " + str(pRePro) + "% 지점", pag)
        print("      RGB : ", str(pRgb1[0]) + " " + str(pRgb1[1]) + " " + str(pRgb1[2]))
        mTmpXY = pEmerPos1
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), pEmerRes1, " hp 비상상태 : " + str(emergencyProSet) + "% 지점", pag)

        print("")
        i = 0
        for slotXyOne in slotXy:
            i = i + 1
            sRgbTemp = screen.getpixel(slotXyOne)
            tResTemp = get_cName(sRgbTemp)
            mTmpXY = slotXyOne
            printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), tResTemp, " 밸트 " + str(i) + " 지점", pag)
            print("      RGB : ", str(sRgbTemp[0]) + " " + str(sRgbTemp[1]) + " " + str(sRgbTemp[2]))

        print("")
        mTmpXY = mPos1
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), mRes1, " MP " + str(mRePro) + "% 지점", pag)
        print("      RGB : ", str(mRgb1[0]) + " " + str(mRgb1[1]) + " " + str(mRgb1[2]))

        break

    # ===== 게임 화면인지 여부 확인 =====
    if cRes1 != "white":  # 실 게임 화면인지 확인
        printTimeMsg(" 게임 화면이 아님. [0]=종료            " + str(printWindmill()), 1)
        continue

    # ===== 캐릭터 hp 있는지 구슬 확인 후 처리
    pEmerPostionYN = 0  # 활력포션을 먹음여부 체크
    if not (pEmerRes1 == "red" or pEmerRes1 == "green"):  # 비상상황인지 체크 // red=정상, green=중독
        print(" 피 부족 : ", end=" ")
        # 밸트의 피약 확인하여 먹기
        i = 0
        for slotRgb in slotXy:
            i = i + 1
            colorValue = get_cName(screen.getpixel(slotRgb))
            if colorValue == "violet":  # 활력포션이라면 바로 먹는다.
                pag.typewrite(str(i))
                print(str(i) + "번 슬롯 활력 포션 먹음(Hp 채움)")
                time.sleep(1)
                pEmerPostionYN = 1  # 활력포션을 먹음
                break
    if pEmerPostionYN == 0:  # 활력포션을 안먹었으면 일반 피약 먹기 시도
        if (pRes1 == "red" or pRes1 == "green"):  # 정상적인 피 먹는 위치 체크 // red=정상, green=중독
            printTimeMsg(str(printWindmill()) + get_KeyMsg(mHelperFlag, mBuff1Time, mGoatmanFlag), 1)
        else:
            print(" 피 부족 : ", end=" ")
            # 밸트의 피약 확인하여 먹기
            i = 0
            for slotRgb in slotXy:
                i = i + 1
                colorValue = get_cName(screen.getpixel(slotRgb))
                if colorValue == "red":  # 밸트 슬롯에서 포션 존재 확인
                    pEndTime = time.time()
                    if abs(pEndTime - pStartTime) > mPotionTime:
                        pag.typewrite(str(i))
                        print(str(i) + "번 슬롯 p 포션 먹음")
                        pStartTime = time.time()
                    else:
                        print("hp 포션 대기 타임")
                    break
            if i > 3:
                print(" 밸트에 hp 포션 없음")

    # ===== 캐릭터 마나 있는지 확인 후 처리
    if mRes1 == "blue":
        printTimeMsg(str(printWindmill()) + get_KeyMsg(mHelperFlag, mBuff1Time, mGoatmanFlag), 1)
    else:
        print(" 마나 부족 : ", end=" ")
        # 슬롯의 엠약 확인하여 먹기
        i = 0
        for slotRgb in slotXy:
            i = i + 1
            colorValue = get_cName(screen.getpixel(slotRgb))
            if colorValue == "blue":  # 밸트 슬롯에서 포션 존재 확인
                mEndTime = time.time()
                if abs(mEndTime - mStartTime) > mPotionTime:
                    pag.typewrite(str(i))
                    print(str(i) + "번 슬롯 mana 포션 먹음")
                    mStartTime = time.time()
                else:
                    print("mana 포션 대기 타임")
                break
            if colorValue == "violet":  # 활력포션이라면 바로 먹는다.
                pag.typewrite(str(i))
                print(str(i) + "번 슬롯 활력 포션 먹음(mana 채움)")
                time.sleep(1)
                break
        if i > 3:
            print(" 밸트에 mana 포션 없음")

    # ===== 용병 hp 있는지 확인 후 처리
    # 2곳의 색상을 확인하여 둘다 없다면 죽은걸로 간주하여 피 처리 안함
    yEmerPotionYN = 0  # 활력포션을 먹음여부 체크
    if mHelperFlag and yRes1 == "green" and yRes2 != "green":
        print(" 용병 피 부족 : ", end=" ")
        if yEmerRes1 != "green":  # 비상상황인지 체크 // red=정상, green=중독
            # 피약 슬롯 확인하여 먹기
            i = 0
            for slotRgb in slotXy:
                i = i + 1
                colorValue = get_cName(screen.getpixel(slotRgb))
                if colorValue == "violet":  # 활력포션이라면 바로 먹는다.
                    pag.typewrite(str(i))
                    print(str(i) + "번 슬롯 활력 포션 먹음(용병 hp 채움)")
                    time.sleep(1)
                    yEmerPotionYN = 1  # 활력포션을 먹음
                    break
            if i > 3:
                print(" 밸트에 활력 포션 없음")
        if yEmerPotionYN == 0:  # 활력포션을 안먹었으면 일반 피약 먹기 시도
            # 피약 슬롯 확인하여 먹기
            i = 0
            for slotRgb in slotXy:
                i = i + 1
                colorValue = get_cName(screen.getpixel(slotRgb))
                if colorValue == "red":
                    yEndTime = time.time()
                    if abs(yEndTime - yStartTime) > mPotionTime:
                        pag.hotkey("shift", str(i))
                        print(str(i) + "번 슬롯 hp 포션 먹음")
                        yStartTime = time.time()
                    else:
                        print("hp 포션 대기 타임")
                    break
            if i > 3:
                print(" 밸트에 hp 포션 없음")

    # ===== 자동 버프 처리
    if mBuffFlag:
        if mBuff1[0]:
            mEndTimeBuff1 = time.time()
            if abs(mEndTimeBuff1 - mStartTimeBuff1) > mBuff1[3]:
                pag.hotkey(mBuff1[2])
                # print("[버프] "+mBuff1[1]+" / 실행하였습니다.")
                mStartTimeBuff1 = time.time()
            else:
                mBuff1Time = str(mBuff1[3] - int(abs(mEndTimeBuff1 - mStartTimeBuff1)))
                # print("[버프] "+mBuff1[1]+" / " + str(mBuff1[3] - int(abs(mEndTimeBuff1 - mStartTimeBuff1))) + " 초 후 재실행 ")

    # ===== 염소인간 자동 소환 처리
    if mGoatmanFlag:
        if yRes1 == "green" and gRes1 != "green":   #용병이 있을때만 소환을 체크해 실행한다.
            if mGoatmanBuff[0]:
                pag.hotkey(mGoatmanBuff[2])
                print("염소인간 소환을 실행 하였습니다.")
                time.sleep(0.5)


# 무한 반복하며 화면을 확인하고 처리하는 while 영역 (종료)
# ===== 프로그램 실행 영역 (종료) ===================================
