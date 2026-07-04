'''
 ## 퍼스트 디센던트 게임

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
import gc
import numpy as np
from datetime import datetime
from PIL import ImageGrab, Image

# 실행 중임을 나타내는 풍차를 출력하는 함수
def printSpin() :
    global mCount    
    spin_char = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    mCount += 1
    if mCount == len(spin_char) : 
        mCount = 0   
    return spin_char[mCount]

# 출력 일시를 함께 표시하는 print 함수
def printTimeMsg( pMsg, pBr = 0 ) :    
    dt = datetime.now()
    dtStr = dt.strftime("%Y-%m-%d %H:%M:%S")
    pMsg = pMsg + "         "
    if pBr == 0 :
        print("[",dtStr,"] " + printSpin() + pMsg )        # 0 = 줄바꿈 처리함
    else :        
        print("\r[",dtStr,"] " + printSpin() + pMsg, end="")

# 출력시 글자의 색상을 지정한다.
def msgColor( pColorName, pText ) :
    pColorName = pColorName.upper()
    color_dic = {"RED":"31","GREEN":"32","YELLOW":"33","BLUE":"34",        #글자색
                "RRED":"41","RGREEN":"42","RYELLOW":"43","RBLUE":"44"      #배경색
                }.get(pColorName, "색상명오류")
    return "\033[" + color_dic + "m" + pText + "\033[m"


# https://velog.io/@krec7748/Pillow-Cosine-Similiarity%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%9C%A0%EC%82%AC%EB%8F%84-%EB%B9%84%EA%B5%90
def cosine_similarity(img1, img2):
    #size_temp = img2.size
    #img1 = img1.resize(size_temp)  # 비교 대상의 이미지 크기를 원본과 동일하게 조정한다.
    array1 = np.array(img1)
    array2 = np.array(img2)
    assert array1.shape == array2.shape
    
    h, w, c = array1.shape
    len_vec = h * w * c
    vector_1 = array1.reshape(len_vec,) / 255.
    vector_2 = array2.reshape(len_vec,) / 255.

    #결과가 0~1 사이의 실수로 나온다 0.99xxxxx  이면 거의 같다고 판단함 
    cosine_similarity = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
    if cosine_similarity * 100 > 98 :   # 99% 이상이면 같다고 판단하여 결과 처리함
        mResult = True
    else :
        mResult = False
    return mResult
#============= 실행 환경 설정값 설정 (시작) ========================
#===== 좌표위치 설정
# 게임 창화면(1920*1080)````
# <<===아래는 active window info 프로그램에서 relative(상대좌표) 값임===>>
cPos1    = ( 571,  997)     # 게임화면인지 확인하는 체크포인트 ( q 이미지 부분 )

#===== 시스템 환경 설정값 설정
qDelayTime = 0.1    # 실행 딜레이 간격 (초)

posTest = 0     # posTest = 0 : 정상 동작 
                # posTest = 1 : 좌표위치 및 색상 테스트 모드 동작
#============= 실행 환경 설정값 설정 (종료) ========================

#============= 변수 기본값 설정 (시작) =======================
# 실행 여부 체크 변수 초기화
mRunQ = False
mRunE = False
mRunR = False
mRunCVZ = False

#풍차 함수의 global 변수 초기화
mCount = 0
mCountCvz = 0
mCountQ = 0
mCountE = 0
mCountR = 0

#비교이미지의 원본파일 로딩
# 이미지 경로 설정
try:
    # PyInstaller로 빌드되었을 때의 경로 처리
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(os.path.abspath(__file__))

imgOrg_E = Image.open(base_path + "\\e.png")
imgOrg_Q = Image.open(base_path + "\\q.png")
imgOrg_R = Image.open(base_path + "\\r.png")
imgOrg_LS = Image.open(base_path + "\\ls.png")
imgCapCnt = 0
#============= 변수 기본값 설정 (종료) =======================

#============= 반복하며 화면을 확인하고 처리하는 영역 (시작) =
sys.stdout.write('\033[?25l')  # 커서 숨기기
sys.stdout.flush()
while True:
    time.sleep(0.1)                                     # 무한루프의 cpu 점유율을 낮추기 위해 잠시 대기 (0.2초)
    
    if keyboard.is_pressed('0') or keyboard.is_pressed(')'):
        sys.stdout.write('\033[?25h')  # 커서 보이기
        sys.stdout.flush()
        print(" 프로그램을 종료 합니다.")
        break
    '''
    if keyboard.is_pressed('shift') :
        pag.typewrite("z")
        mRandom = random.randrange(5,7) / 10    # 0.4 ~ 0.7 초의 랜덤 딜레이 값을 추가한다.
        time.sleep(mRandom)
        pag.typewrite("c")
        mRandom = random.randrange(5,7) / 10    
        time.sleep(mRandom)
        pag.typewrite("v")        
        printTimeMsg("CVZ 처리함.")
    '''
    if keyboard.is_pressed('5') :
        # 전체화면 캡쳐        
        img1 = ImageGrab.grab((fw.left+8,fw.top+31,fw.left+1920+8,fw.top+1080+31))
        dt = datetime.now()
        dtStr = dt.strftime("%Y%m%d%H%M%S")
        img1.save(base_path+"\\"+dtStr+".png")
        print(" 화면을 캡쳐 했습니다.")

    if keyboard.is_pressed('6') :
        if mRunCVZ :
            mRunCVZ = False
            print(" CVZ 클릭 종료")
        else :
            mRunCVZ = True
            mCountCvz = 0
            print(" CVZ 클릭 반복 시작")
    
    if keyboard.is_pressed('7'):
        if mRunR :                                  # 기능 실행 토글 처리
            mRunR = False
            print(" R 클릭 종료")
        else : 
            mCountR = 0 # 클릭 횟수를 카운트
            mRunR = True
            rStartTime = time.time()               # 실행 딜레이 시간 체크 변수 초기화 
            mCountCvz = 0
            mCountQ = 0
            print(" R 클릭 반복 시작")

    if keyboard.is_pressed('8'):
        if mRunQ :                                  # 기능 실행 토글 처리
            mRunQ = False
            print(" Q 클릭 종료")
        else :
            mRunQ = True
            qStartTime = time.time()               # 실행 딜레이 시간 체크 변수 초기화 
            print(" Q 클릭 반복 시작")

    if keyboard.is_pressed('9'):
        if mRunE :                                  # 기능 실행 토글 처리
            mRunE = False
            print(" E 클릭 종료")
        else : 
            mCountE = 0 # 클릭 횟수를 카운트
            mRunE = True
            eStartTime = time.time()               # 실행 딜레이 시간 체크 변수 초기화 
            mCountCvz = 0
            mCountQ = 0
            print(" E 클릭 반복 시작")

    fw = pag.getActiveWindow()   
    try:
        winTitle = fw.title
    except AttributeError as err :
        winTitle = ""
    
    if winTitle != "The First Descendant  " :           # 게임 화면 일때만 동작하게 한다.
        printTimeMsg(" 게임창을 활성화해야 합니다.", 1)
        continue
    
    # 테스트 모드 일때 처리 영역  
    if posTest == 1 :
        # 전체화면 캡쳐
        img1 = ImageGrab.grab((fw.left+8,fw.top+31,fw.left+1920+8,fw.top+1080+31))
        img1.save("c:\\currdata\\all.png")
        time.sleep(1)        
        # q 이미지 캡쳐
        img1 = ImageGrab.grab((fw.left+809+8,fw.top+854+31,fw.left+825+8,fw.top+873+31))
        img1.save("c:\\currdata\\q.png")
        time.sleep(1)
        # e 이미지 캡쳐 (상호작용 시 나오는 것)
        img1 = ImageGrab.grab((fw.left+1018+8,fw.top+637+31,fw.left+1030+8,fw.top+654+31))
        img1.save("c:\\currdata\\e.png") 
        # r 이미지 캡쳐 (임무 재시작, 우측하단 부분)
        img1 = ImageGrab.grab((fw.left+1611+8,fw.top+898+31,fw.left+1623+8,fw.top+913+31))
        img1.save("c:\\currdata\\r.png") 
        # 루나 스택 쌓은거 확인 1091,997 / 1109,1007
        img1 = ImageGrab.grab((fw.left+1091+8,fw.top+997+31,fw.left+1109+8,fw.top+1007+31))
        img1.save("c:\\currdata\\ls.png")  
                
        fw = pag.getActiveWindow()    
        time.sleep(1)
        print("활성창 명 :" + fw.title)    #Diablo II: Resurrected
        print("창크기 : ", fw.size)  # 실행 창의 크기 정보(width, height), Size(width=1938, height=1060)
        print("창 좌표 좌상xy 우하xy :", fw.left, fw.top, fw.right, fw.bottom)  # 실행 창의 좌표 정보 
        #pyautogui.click(fw.left + 25, fw.top + 20)  # 실행 창을 줄이거나 이동해도 해당 위치에서 마우스 클릭이 됨
        break

    # ===== 기능 실행 여부에 따른 키보드 클릭 =====
    if mRunCVZ :
        # 루나 스택 쌓은거 확인 
        #  L 스킬설명 https://gall.dcinside.com/mgallery/board/view/?id=first_descendant&no=602029
        imgCap = ImageGrab.grab((fw.left+1091+8,fw.top+997+31,fw.left+1109+8,fw.top+1007+31))
        imgCapCnt = imgCapCnt + 1
        if cosine_similarity(imgCap, imgOrg_LS) :
            pag.typewrite("z")
            mRandom = random.randrange(5,7) / 10            # 0.5 ~ 0.7 초의 랜덤 딜레이 값을 추가한다.
            time.sleep(mRandom)
            pag.typewrite("c")
            mRandom = random.randrange(5,7) / 10    
            time.sleep(mRandom)
            pag.typewrite("v")
            mRandom = random.randrange(5,7) / 10            # 딜레이 처리해서 다시 z가 눌리지 않도록 처리
            time.sleep(mRandom)
            mCountCvz += 1
            printTimeMsg(" CVZ run. "+str(mCountCvz)+"회") 
        else :
            time.sleep(0.1)                                 #딜레이 타임 처리
    
    if mRunQ :
        # q 이미지 캡쳐  // q클릭 가능한 화면인지 구분한다.
        imgCap = ImageGrab.grab((fw.left+809+8,fw.top+854+31,fw.left+825+8,fw.top+873+31))
        imgCapCnt = imgCapCnt + 1
        if cosine_similarity(imgCap, imgOrg_Q) :
            qTempTime = time.time() - qStartTime            # 지난번 q누른 후 흘러간 시간 계산
            if qTempTime > qDelayTime :
                pag.typewrite("q")
                mCountQ += 1
                print(" Q 클릭 "+str(mCountQ) + "회 "+str(int(qTempTime*100)/100)+"s 간격")
                mRandom = random.randrange(1,3) / 10        # 0.1 ~ 0.3 초의 랜덤 딜레이 값을 추가한다.
                qStartTime = time.time() + mRandom          
        else :
            time.sleep(0.1)                                 #딜레이 타임 처리
      
    if mRunE :
        # e 이미지 캡쳐        
        imgCap = ImageGrab.grab((fw.left+1018+8,fw.top+637+31,fw.left+1030+8,fw.top+654+31))
        imgCapCnt = imgCapCnt + 1
        if cosine_similarity(imgCap, imgOrg_E) :
            #길게 누르기
            pag.keyDown('e')                                # e 키를 누른 상태를 유지합니다.
            mRandom = 0.5 + (random.randrange(1,3) / 10)    
            time.sleep(mRandom)                             # 키누르고 있는 시간 처리
            pag.keyUp('e')                                  # e 키를 뗍니다. 
            eTempTime = time.time() - eStartTime            # 지난번 e키를 누른 후 흘러간 시간 계산
            mCountE += 1
            printTimeMsg(" e 클릭("+str(int(eTempTime)//60)+"m"+str(int(eTempTime)%60)+"s 소요) " + str(mCountE) +"회")
            eStartTime = time.time()  
        else :
            time.sleep(0.1)                                 #딜레이 타임 처리

    if mRunR :
        # r 이미지 캡쳐        
        imgCap = ImageGrab.grab((fw.left+1611+8,fw.top+898+31,fw.left+1623+8,fw.top+913+31))
        imgCapCnt = imgCapCnt + 1
        if cosine_similarity(imgCap, imgOrg_R) :
            #길게 누르기
            pag.keyDown('r')                                # e 키를 누른 상태를 유지합니다.
            mRandom = 0.9 + (random.randrange(1,3) / 10)    # 0.1 ~ 0.2 초의 랜덤 딜레이 값을 추가한다.
            time.sleep(mRandom)                             # 키누르고 있는 시간 처리
            pag.keyUp('r')                                  # e 키를 뗍니다. 
            rTempTime = time.time() - rStartTime            # q누른 후 흘러간 시간 계산
            mCountR += 1
            printTimeMsg(" r 클릭("+str(int(rTempTime)//60)+"m"+str(int(rTempTime)%60)+"s 소요) " + str(mCountR) +"회")
            rStartTime = time.time()  
        else :
            time.sleep(0.1)                                 #딜레이 타임 처리

    # 실행중인 명령 상태 표시 처리
    mDspMsg = "  5=캡쳐 "
    if mRunCVZ :    mDspMsg += msgColor("rGreen", " 6=cvz ")
    else :          mDspMsg += " 6=cvz "    
    if mRunR :      mDspMsg += msgColor("rGreen", " 7=R ")
    else :          mDspMsg += " 7=R "  
    if mRunQ :      mDspMsg += msgColor("rGreen", " 8=Q ")
    else :          mDspMsg += " 8=Q "      
    if mRunE :      mDspMsg += msgColor("rGreen", " 9=E ")
    else :          mDspMsg += " 9=E "
    mDspMsg += " 0=종료  "
    printTimeMsg( mDspMsg, 1)

    if imgCapCnt > 300 :
        imgCapCnt = 0
        del imgCap
        gc.collect()
        printTimeMsg(" gc clear")

#============= 반복하며 화면을 확인하고 처리하는 영역 (종료) =
 








