'''
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
'''

import pyautogui as pag
import time
import random
import keyboard
import cv2
import sys
import os
from datetime import datetime
from PIL import ImageGrab

#=====[함수 영역] (시작) =========================================
# ===[함수]=== 실행 중임을 나타내는 풍차를 출력하는 함수
def printWindmill() :
    global mCount
    spin_char = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    mCount += 1
    if mCount == len(spin_char) : 
        mCount = 0   
    return spin_char[mCount]

# ===[함수]=== 출력 일시를 함께 표시하는 print 함수
def printTimeMsg( pMsg, pBr = 0 ) :
    dt = datetime.now()
    dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
    if pBr == 0 :
        print("[",dtStr,"] ", pMsg )
    else :
        print("\r[",dtStr,"] ", pMsg, end="")

# ===[함수]=== 출력시 글자의 색상을 지정한다.
def msgColor( pColorName, pText ) :
    pColorName = pColorName.upper()
    color_dic = {"RED":"31","GREEN":"32","YELLOW":"33","BLUE":"34",        #글자색
                "RRED":"41","RGREEN":"42","RYELLOW":"43","RBLUE":"44"      #배경색
                }.get(pColorName, "색상명오류")
    return "\033[" + color_dic + "m" + pText + "\033[m"

# ===[함수]=== 상태 메세지 출력 처리 함수
def get_KeyMsg( pHelperFlag=False, pBufferTime = "" ) :
    mKeyMsg = " "        
    if pHelperFlag :
        mKeyMsg += msgColor( "rGreen", " [ = 용병 ")
    else :
        mKeyMsg += " [ = 용병 "
    if pBufferTime == "" :
        mKeyMsg += " ]=버프 "
    else :
        mKeyMsg += msgColor( "rGreen", " ]=버프 ["+pBufferTime+"s]")
    mKeyMsg += " 0=종료 9=캡쳐     " 
    return mKeyMsg

# ===[함수]=== RGB값을 받아 색상을 판별하는 함수 
#   RGB(87,72,48) 빨강이지만 붉은끼만 있는것
def get_cName(pRgb_dic) :
    p1 = pRgb_dic[0]
    p2 = pRgb_dic[1]
    p3 = pRgb_dic[2]
    mGapMin = 30                # 다른 색상과의 최소 이정도 차이는 나야 색구분이 된다일때 그 임의 설정값
    if p1 > 240 and p2 > 240 and p3 > 240 :
        return "white"    
    elif (p1 > 70 and p1 < 113) and (p2 >= 0 and p2 < 7) and (p3 > 70 and p3 < 120) :
        return "violet"
    elif (p1 > p2 and p1 > p3) and (p1 - p2 > mGapMin and p1 - p3 > mGapMin) :
        return "red"
    elif (p2 > p1 and p2 > p3) and (p2 - p1 > mGapMin and p2 - p3 > mGapMin) : 
        return "green"
    elif (p3 > p1 and p3 > p2) and (p3 - p1 > mGapMin and p3 - p2 > mGapMin) :
        return "blue"
    if p1 < 50 and p2 < 50 and p3 < 50 :
        return "black"
    else :
        return "unknown"+str(p1)+"/"+str(p2)+"/"+str(p3)    

# ===[함수]=== 화면에 출력해주는 함수 (시작) 
def printMsg(pPosDic, pColor, pTitle, pag1) :
    tPos = pPosDic
    pag1.moveTo(tPos[0], tPos[1])
    print(pTitle + " 확인 ==> ", end=" ")
    print(" 모니터 절대 좌표 xy위치 : (" + str(tPos[0]) + "," + str(tPos[1]) +") 로 이동", end=" ")
    print(" / 컬러 : " + pColor)
    time.sleep(1)
#=====[함수 영역] (종료) =========================================

#===== 실행 환경 설정값 설정 (시작) ================================
#===== 사용자 지정 환경 설정값 설정 (시작) =====
mPotionTime = 5                             # 포션 연속 먹는 딜레이 초 간격
posTest = 0                                 # posTest = 0 : 정상 동작 
                                            # posTest = 1 : 좌표위치 및 색상 테스트 모드 동작

# 캐릭터 hp, mp, 용병 hp 사이즈 초기값 부여
pFull = 132     # 피통 최고값
mFull = 74     # 마나통 최고값
yFull = 117     # 용병 피통 최고값 (용병 상태창의 생명력값)

# 수동으로 물약먹는 %값 설정하려면 0보다 큰값을 입력하세요
pReProSet = 0
mReProSet = 60
yReProSet = 0

# 자동 버프 (실행여부 1=run / 0=중지, 버프명, 단축키, 자동실행시간(초))
mBuff1 = (1,"(성기사)신성한방패", "f6", 90)    
#mBuff1 = (1,"(소서)얼어붙은갑옷", "f6", 144) 

# 사용할 hp 물약을 지정
#===== 팔라딘
pBottle = 45     #체력1 미량 치유물약
#pBottle = 90     #체력2 소량 치유물약
#pBottle = 150    #체력3     치유물약
#pBottle = 270    #체력4 대량 치유물약
#pBottle = 480    #체력5 초대량 치유물약

mBottle = 30     #마나1 미량 마나물약
#mBottle = 60      #마나2 소량 마나물약
#mBottle = 120    #마나3     마나물약
#mBottle = 225    #마나4 대량 마나물약
#mBottle = 375    #마나5 초대량 마나물약

#===== 소서리스
#pBottle = 30     #체력1 미량 치유물약
#pBottle = 60     #체력2 소량 치유물약
#pBottle = 100    #체력3     치유물약
#pBottle = 180    #체력4 대량 치유물약
#pBottle = 320    #체력5 초대량 치유물약

#mBottle = 40     #마나1 미량 마나물약
#mBottle = 80      #마나2 소량 마나물약
#mBottle = 160    #마나3     마나물약
#mBottle = 300    #마나4 대량 마나물약
#mBottle = 500    #마나5 초대량 마나물약


# 화면 체크하는 좌표 위치 설정
#   게임 화면이 창모드(1920*1080) 일때 사용하는 값임 
#   아래는 active window info 프로그램에서 relative(상대좌표) 값임
#   * 실행하면 캡쳐 기능있는데 그걸로 캡쳐하여 위치 확인해 입력하면됨
pTopXY   = ( 547,  957)                     # 피 구슬 상단 y좌표 (상단,하단 좌표 입력은 %물약 먹는 위치 계산 위함)
pLowXY   = ( 547, 1097)                     # 피 구슬 하단 y 좌표
mTopXY   = (1388,  957)                     # 엠 구슬 상단 y좌표
mLowXY   = (1388, 1097)                     # 엠 구슬 하단 y좌표
yLeftXY  = (  48,  124)                     # 용병 피바 좌측 끝 지점 
yRightXY = (  90,  124)                     # 용병 피바 우측 끝 지점
cPos1    = ( 571,  997)                     # 게임화면인지 확인하는 체크포인트 (피약의 반사처리되는 부분(흰색))
xStartP  = 665
slotXy   = ((xStartP, 1077),(xStartP+(67*1), 1077),(xStartP+(67*2), 1077),(xStartP+(67*3), 1077)) # 물약 벨트 슬롯 좌표(슬롯1 xy좌표, 슬롯2 xy좌표, ...)
#===== 사용자 지정 환경 설정값 설정 (종료)

#===== 변수 기본값 설정 (시작) 
# 피 채우는 최소값이 20% 이하로 가지 않도록 한다
mAutoMin = 30
# 피 채우는 최대값이 80% 이하로 가지 않도록 한다
mAutoMax = 80

# 물약 회복량으로 체크할 % 위치 계산
if pReProSet > 0:
    pRePro = pReProSet
else :
    pRePro = int((pFull-pBottle)*100/pFull)     # %이하로 떨어지면 피약사용 할 %계산  //살짝 일찍 먼저 먹게하기위해 10% 보정
    if pRePro < mAutoMin :
        pRePro = mAutoMin
    if pRePro > mAutoMax :
        pRePro = mAutoMax

if mReProSet > 0:
    mRePro = mReProSet
else :
    mRePro = int((mFull-mBottle)*100/mFull)     # %이하로 떨어지면 엠약사용 할 %계산
    if mRePro < mAutoMin :
        mRePro = mAutoMin
    if mRePro > mAutoMax :
        mRePro = mAutoMax

if yReProSet > 0:
    yRePro = yReProSet
else :
    yRePro = int((yFull-pBottle)*100/yFull)     # 용병 피약 사용 % 위치 (용병도 캐릭터 피약 같이 사용함) 용병 10% 만큼 내려 너무 자주 사용안하게 한다 
    if yRePro < mAutoMin :
        yRePro = mAutoMin
    if yRePro > mAutoMax :
        yRePro = mAutoMax

# 물약 사용여부 체크할 % 값으로 체크할 화면 좌표 계산
pRange = (pLowXY[1] - pTopXY[1])
pY     = pTopXY[1]  + ( pRange - int( pRange * pRePro / 100) )
mRange = (mLowXY[1] - mTopXY[1])
mY     = mTopXY[1]  + ( mRange - int( mRange * mRePro / 100) )
yX     = yLeftXY[0] + int( (yRightXY[0] - yLeftXY[0]) / 100 * yRePro )
pPos1  = (pTopXY[0], pY)                    # 피약 먹을 위치 확인 지점 
mPos1  = (mTopXY[0], mY)                    # 엠약 먹을 위치 확인 지점 
yPos1  = (yLeftXY[0], yLeftXY[1])           # 용병은 2개의 포인트를 체크하여 최소지점 이하면 죽은걸로 간주하여 물약 처리 안함 
yPos2  = (yX, yRightXY[1])                  # 용병 피약 먹을 위치 확인 지점 

# 물약 사용 딜레이 시간 변수 초기값 부여
pStartTime = time.time() - mPotionTime      # 피약 먹은 시간 변수
mStartTime = time.time() - mPotionTime      # 엠약 먹는 시간 변수
yStartTime = time.time() - mPotionTime      # 용병 피약 먹는 시간 변수

# 버프변수 초기화
mBuffFlag  = False                          #버프 사용 여부
mBuff1Time = ""                             #버프 남은 시간 저장 변수 

# 용병 물약 먹기 실행 on/off 변수 초기화
mHelperFlag = False

#풍차 함수의 global 변수 초기화
mCount = 0

#물약 상태 문구를 1번만 출력하게 하는 변수 초기화
pHelpMsgYN = 1

# 프로그램이 실행되는 폴더 위치 조회
try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(os.path.abspath(__file__))
#===== 변수 기본값 설정 (종료) 
#===== 실행 환경 설정값 설정 (종료) ================================

#===== 프로그램 실행 영역 (시작) ===================================
# 물약 경고 처리
if pFull-pBottle <= 0 :
    print(" [경고] 피통보다 물약이 큽니다. 확인후 수정하시기 바랍니다.")
    
if mFull-mBottle <= 0 :
    print(" [경고] 마나통보다 마나물약이 큽니다. 확인후 수정하시기 바랍니다.")
    
if pRePro <= 50 :
    print(" ")
    print(" *** [경고] HP약 체크가 50%이하로 한번에 죽을수있습니다. *** ")  
    print(" ")  

sys.stdout.write('\033[?25l')  # 커서 숨기기
sys.stdout.flush()

# 무한 반복하며 화면을 확인하고 처리하는 while 영역 (시작)
while True:
    time.sleep(0.2)                                     # 무한루프의 cpu 점유율을 낮추기 위해 잠시 대기 (0.2초)
        
    if keyboard.is_pressed('0') : #or keyboard.is_pressed('Y'):
        sys.stdout.write('\033[?25h')  # 커서 보이기
        sys.stdout.flush()
        print("")
        print(" 프로그램을 종료 합니다.")
        break
    if keyboard.is_pressed(']') : # or keyboard.is_pressed('K'):
        if mBuffFlag :                                  # 버프 실행 토글 처리
            mBuffFlag = False
            mBuff1Time = ""
            #print(" 자동 버프 기능을 종료 합니다.")
        else :
            mBuffFlag = True
            mStartTimeBuff1 = time.time() - mBuff1[3]   # 버프 시작시간 설정
            #print(" 자동 버프 기능을 실행 합니다.")
    if keyboard.is_pressed('[') : #or keyboard.is_pressed('L'):
        if mHelperFlag :                                  # 용병 물약 실행 토글 처리
            mHelperFlag = False
            #print(" 용병 물약 기능을 종료 합니다.")
        else :
            mHelperFlag = True
            #print(" 용병 물약 기능을 실행 합니다.")
    if keyboard.is_pressed('9') :
        # 전체화면 캡쳐 (제목타이틀 포함 그래야 캡쳐 이미지 좌표값이 프로그램 코드 좌표와 1:1 매칭됨)       
        img1 = ImageGrab.grab((fw.left,fw.top,fw.right,fw.bottom))
        dt = datetime.now()
        dtStr = dt.strftime("%Y%m%d%H%M%S")
        img1.save(base_path+"\\D2R"+dtStr+".png")
        print(" 화면을 캡쳐 했습니다.")    

    # 게임창이 활성화 되었는지 여부 확인 
    #   게임창에서만 키값을 입력하고 화면을 체크하도록 하기 위해서
    fw = pag.getActiveWindow()   
    try:
        winTitle = fw.title
    except AttributeError as err :
        winTitle = "" 
    if winTitle != "Diablo II: Resurrected" :           # 디아블로 게임 화면 일때만 동작하게 한다.
        #dt = datetime.now()
        #dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
        #print("[",dtStr,"] ")
        if pHelpMsgYN == 1 :                            # 물약 메세지는 한번만 출력한다.
            print("")
            print(" Hp max: " + str(pFull) + ", 1병회복량: " + str(pBottle) + ", 체크지점: "+str(pRePro) +" %")
            print(" Mp max: " + str(mFull) + ", 1병회복량: " + str(mBottle) + ", 체크지점: "+str(mRePro) +" %")
            print(" Hp max: " + str(yFull) + ", 1병회복량: " + str(pBottle) + ", 체크지점: "+str(yRePro) +" %")
            pHelpMsgYN = 0
        printTimeMsg(" -- "+str(printWindmill()+" 게임창을 활성화해야 합니다.  --"), 1)
        continue
    else :
        pHelpMsgYN = 1

    #화면을 캡쳐하여 색상정보를 추출한다.
    screen = ImageGrab.grab((fw.left,fw.top,fw.right,fw.bottom))    
    pRgb1 = screen.getpixel(pPos1)      # hp
    mRgb1 = screen.getpixel(mPos1)      # mp
    yRgb1 = screen.getpixel(yPos1)      # 용병 피 바 1
    yRgb2 = screen.getpixel(yPos2)      # 용병 피 바 1
    cRgb1 = screen.getpixel(cPos1)      # 게임 화면인지 체크하기 위한 포인트
    pRes1 = get_cName(pRgb1)            # 추출한 rgb값의 색상을 구분한다.
    mRes1 = get_cName(mRgb1)
    yRes1 = get_cName(yRgb1)
    yRes2 = get_cName(yRgb2)
    cRes1 = get_cName(cRgb1)

    # ===== 테스트 모드 일때 처리 영역
    if posTest == 1 :
        time.sleep(1)
        print("")
        print("")
        print(" 활성창 명 : " + fw.title)       # Diablo II: Resurrected
        print(" 창크기 : ", fw.size)            # 실행 창의 크기 정보(width, height), Size(width=1938, height=1060)
        print(" 창 좌표 좌상(x,y) 우하(x,y) : (", fw.left, fw.top,") (", fw.right, fw.bottom,")")  # 실행 창의 좌표 정보, -9 -9 1929 1051
        #pyautogui.click(fw.left + 25, fw.top + 20)  # 실행 창을 줄이거나 이동해도 해당 위치에서 마우스 클릭이 됨

        dt = datetime.now()
        dtStr = dt.strftime("%Y%m%d%H%M%S")
        #screen.save(base_path+"\\D2R_test"+dtStr+".png")       # 화면을 캡쳐한다.

        print("")
        mTmpXY = yPos1 
        # 마우스 포인터는 모니터의 절대좌표로 지정해야 하기 때문에 fw.left처럼 창의 위치값을 더해준다.
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), yRes1, " 용병 hp 최저 지점", pag)  
        mTmpXY = yPos2         
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), yRes2, " 용병 hp " + str(yRePro) + "% 지점", pag)  
         
        mTmpXY = pPos1          
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), pRes1, " HP "    + str(pRePro) + "% 지점", pag)  
        print("      RGB : ", str(pRgb1[0]) + " " + str(pRgb1[1]) + " " + str(pRgb1[2]))

        print("")
        i = 0
        for slotXyOne in slotXy :
            i = i + 1    
            sRgbTemp = screen.getpixel(slotXyOne)
            tResTemp = get_cName(sRgbTemp)
            mTmpXY = slotXyOne 
            printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), tResTemp, " 밸트 " + str(i) + " 지점", pag)  
            print("      RGB : ", str(sRgbTemp[0]) + " " + str(sRgbTemp[1]) + " " + str(sRgbTemp[2]))

        print("")
        mTmpXY = mPos1 
        printMsg((fw.left + mTmpXY[0], fw.top + mTmpXY[1]), mRes1, " MP "  + str(mRePro) + "% 지점", pag)  
        print("      RGB : ", str(mRgb1[0]) + " " + str(mRgb1[1]) + " " + str(mRgb1[2]))
        
        break

    # ===== 게임 화면인지 여부 확인 =====
    if cRes1 != "white" :                                       # 실 게임 화면인지 확인
        printTimeMsg(" 게임 화면이 아님. [0]=종료            " + str(printWindmill()), 1)
        continue

    #===== 캐릭터 hp 있는지 구슬 확인 후 처리
    if (pRes1 == "red" or pRes1 == "green")  :                  # red=정상, green=중독
        printTimeMsg(str(printWindmill()) + get_KeyMsg(mHelperFlag, mBuff1Time) , 1)            
    else :
        print(" 피 부족 : ", end=" ")
        # 밸트의 피약 확인하여 먹기
        i = 0
        for slotRgb in slotXy :
            i = i + 1    
            colorValue = get_cName(screen.getpixel(slotRgb))
            if colorValue == "red" :                            # 밸트 슬롯에서 포션 존재 확인
                pEndTime = time.time()
                if abs(pEndTime - pStartTime) > mPotionTime :
                    pag.typewrite(str(i))
                    print(str(i)+"번 슬롯 p 포션 먹음")
                    pStartTime = time.time()
                else :
                    print("hp 포션 대기 타임")
                break        
            if colorValue == "violet" :                         # 활력포션이라면 바로 먹는다.
                pag.typewrite(str(i))
                print(str(i)+"번 슬롯 활력 포션 먹음(Hp 채움)")
                time.sleep(1)
                break
            print(" 밸트에 hp 포션 없음")
    
    #===== 캐릭터 마나 있는지 확인 후 처리
    if  mRes1 == "blue" :
        printTimeMsg(str(printWindmill()) + get_KeyMsg(mHelperFlag, mBuff1Time) , 1)
    else :
        print(" 마나 부족 : ", end=" ")
        # 슬롯의 엠약 확인하여 먹기
        i = 0
        for slotRgb in slotXy :
            i = i + 1    
            colorValue = get_cName(screen.getpixel(slotRgb))
            if colorValue == "blue" :                       #밸트 슬롯에서 포션 존재 확인
                mEndTime = time.time()
                if abs(mEndTime - mStartTime) > mPotionTime :
                    pag.typewrite(str(i))
                    print(str(i)+"번 슬롯 mana 포션 먹음")
                    mStartTime = time.time()
                else :
                    print("mana 포션 대기 타임")
                break        
            if colorValue == "violet" :                         # 활력포션이라면 바로 먹는다.
                pag.typewrite(str(i))
                print(str(i)+"번 슬롯 활력 포션 먹음(mana 채움)")
                time.sleep(1)
                break
            print(" 밸트에 mana 포션 없음")

    # ===== 용병 hp 있는지 확인 후 처리
    # 2곳의 색상을 확인하여 둘다 없다면 죽은걸로 간주하여 피 처리 안함
    if mHelperFlag and yRes1 == "red" and yRes2 != "red" :
        print(" 용병 피 부족 : ", end=" ")
        # 피약 슬롯 확인하여 먹기
        i = 0
        for slotRgb in slotXy :
            i = i + 1    
            colorValue = get_cName(screen.getpixel(slotRgb))
            if colorValue == "red" :
                yEndTime = time.time()
                if abs(yEndTime - yStartTime) > mPotionTime :
                    pag.hotkey('shift',str(i))
                    print(str(i)+"번 슬롯 hp 포션 먹음")
                    yStartTime = time.time()
                else :
                    print("hp 포션 대기 타임")
                break        
            if colorValue == "violet" :                             # 활력포션이라면 바로 먹는다.
                pag.typewrite(str(i))
                print(str(i)+"번 슬롯 활력 포션 먹음(용병 hp 채움)")
                time.sleep(1)
                break
            print(" 밸트에 hp 포션 없음")

    # ===== 자동 버프 처리
    if mBuffFlag :
        if mBuff1[0] :
            mEndTimeBuff1 = time.time()
            if abs(mEndTimeBuff1 - mStartTimeBuff1) > mBuff1[3] :
                pag.hotkey(mBuff1[2])
                #print("[버프] "+mBuff1[1]+" / 실행하였습니다.")
                mStartTimeBuff1 = time.time()
            else :
                mBuff1Time = str(mBuff1[3] - int(abs(mEndTimeBuff1 - mStartTimeBuff1)))
                #print("[버프] "+mBuff1[1]+" / " + str(mBuff1[3] - int(abs(mEndTimeBuff1 - mStartTimeBuff1))) + " 초 후 재실행 ")

# 무한 반복하며 화면을 확인하고 처리하는 while 영역 (종료)
#===== 프로그램 실행 영역 (종료) ===================================









