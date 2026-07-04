
'''
 ## 퍼스트 디센던트 게임

 pip install pyautogui
 pip install opencv-python      # cv2 설치
 pip install pillow             # PIL 설치
'''

import pyautogui as pag
import time
import random
import cv2
import gc
import numpy as np
from datetime import datetime
from PIL import ImageGrab, Image
import tkinter as tk
from tkinter import scrolledtext
import threading
import os

#============= 전역 변수 설정 =======================
mRunQ = False
mRunE = False
mCount = 0
imgOrg_Q = None
imgOrg_E = None

#============= GUI 제어 함수 =======================
def start_q():
    """자동 Q 시작"""
    global mRunQ, mRunE
    if not mRunQ:
        mRunQ = True
        mRunE = False
        log_message("자동 Q 시작")
        status_var.set("상태: 자동 Q 실행 중...")

def start_e():
    """자동 E 시작"""
    global mRunQ, mRunE
    if not mRunE:
        mRunQ = False
        mRunE = True
        log_message("자동 E 시작")
        status_var.set("상태: 자동 E 실행 중...")

def stop_all():
    """모든 자동화 정지"""
    global mRunQ, mRunE
    if mRunQ or mRunE:
        mRunQ = False
        mRunE = False
        log_message("자동화 정지")
        status_var.set("상태: 대기 중")

def log_message(msg):
    """로그 메시지를 GUI 텍스트 창에 추가"""
    dt = datetime.now().strftime("%H:%M:%S")
    full_msg = f"[{dt}] {msg}\n"
    
    # GUI가 준비되었는지 확인
    if 'log_text' in globals() and log_text.winfo_exists():
        log_text.insert(tk.END, full_msg)
        log_text.see(tk.END)
    else:
        print(full_msg.strip())

def on_closing():
    """창을 닫을 때 호출되는 함수"""
    stop_all()
    root.destroy()

def key_press(event):
    """키보드 입력 처리"""
    if event.char == '8':
        start_q()
    elif event.char == '9':
        start_e()
    elif event.char == '0':
        stop_all()

#============= 핵심 로직 함수 =======================
def printWindmill():
    """실행 중 표시기"""
    global mCount
    mCount = (mCount + 1) % 4
    return "|/-\""[mCount]

def cosine_similarity(img1, img2):
    """두 이미지의 코사인 유사도 계산"""
    if img1 is None or img2 is None:
        return False
    try:
        size_temp = img2.size
        img1 = img1.resize(size_temp)
        array1 = np.array(img1)
        array2 = np.array(img2)
        if array1.shape != array2.shape:
            return False
        
        len_vec = array1.size
        vector_1 = array1.flatten() / 255.
        vector_2 = array2.flatten() / 255.

        similarity = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
        return similarity > 0.95
    except Exception:
        return False

def automation_logic():
    """자동화 메인 루프 (별도 스레드에서 실행)"""
    global mRunQ, mRunE, imgOrg_E, imgOrg_Q
    
    qStartTime = 0
    imgCapCnt = 0
    mCountE = 0

    while True:
        if not (mRunQ or mRunE):
            time.sleep(0.2)
            continue

        fw = pag.getActiveWindow()
        winTitle = fw.title if fw else ""

        if "The First Descendant" not in winTitle:
            if status_var.get() != "상태: 게임 창을 활성화하세요.":
                status_var.set("상태: 게임 창을 활성화하세요.")
            time.sleep(1)
            continue
        
        if mRunQ:
            status_var.set("상태: 자동 Q 실행 중...")
        elif mRunE:
            status_var.set("상태: 자동 E 실행 중...")

        try:
            if mRunQ:
                # q 이미지 캡쳐  // q클릭 가능한 화면인지 구분한다.
                imgCap = ImageGrab.grab((fw.left+809+8,fw.top+864+31,fw.left+825+8,fw.top+883+31))
                if cosine_similarity(imgCap, imgOrg_Q):
                    if time.time() - qStartTime > 0.1:
                        pag.typewrite("q")
                        log_message(f"Q 클릭")
                        qStartTime = time.time() + random.uniform(0.1, 0.2)
                else:
                    # 상태 메시지가 계속 업데이트되는 것을 방지
                    if not status_var.get().endswith("..."):
                        status_var.set(f"Q checking... {printWindmill()}")

            elif mRunE:
                # e 이미지 캡쳐
                imgCap = ImageGrab.grab((fw.left+1018+8,fw.top+637+31,fw.left+1030+8,fw.top+654+31))
                if cosine_similarity(imgCap, imgOrg_E):
                    pag.keyDown('e')
                    time.sleep(0.5 + random.uniform(0.1, 0.3))
                    pag.keyUp('e')
                    mCountE += 1
                    log_message(f"==> E 클릭 ({mCountE} 회)")
                    qStartTime = time.time()
                else:
                    if not status_var.get().endswith("..."):
                        status_var.set(f"E checking... {printWindmill()}")
            
            imgCapCnt += 1
            if imgCapCnt > 300:
                imgCapCnt = 0
                gc.collect()
                log_message("gc clear")

        except Exception as e:
            log_message(f"오류 발생: {e}")
        
        time.sleep(0.2)

#============= 프로그램 시작점 =======================
if __name__ == "__main__":
    # 이미지 경로 설정
    try:
        # PyInstaller로 빌드되었을 때의 경로 처리
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    q_image_path = os.path.join(base_path, "q.png")
    e_image_path = os.path.join(base_path, "e.png")

    # GUI 설정
    root = tk.Tk()
    root.title("TFD Automation")
    root.geometry("500x350")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # 프레임
    control_frame = tk.Frame(root, padx=10, pady=10)
    control_frame.pack(fill=tk.X)

    log_frame = tk.Frame(root, padx=10, pady=10)
    log_frame.pack(fill=tk.BOTH, expand=True)

    # 컨트롤 버튼
    tk.Button(control_frame, text="자동 Q 시작", command=start_q, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="자동 E 시작", command=start_e, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(control_frame, text="정지", command=stop_all, width=15).pack(side=tk.LEFT, padx=5)

    # 상태 표시줄
    status_var = tk.StringVar()
    status_var.set("상태: 대기 중")
    status_label = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    # 로그 텍스트
    log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state=tk.NORMAL, font=("Malgun Gothic", 9))
    log_text.pack(fill=tk.BOTH, expand=True)

    # 이미지 로드
    try:
        imgOrg_Q = Image.open(q_image_path)
        log_message(f"'{q_image_path}' 로드 성공")
    except FileNotFoundError:
        imgOrg_Q = None
        log_message(f"오류: '{q_image_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        imgOrg_Q = None
        log_message(f"'{q_image_path}' 로드 중 오류: {e}")

    try:
        imgOrg_E = Image.open(e_image_path)
        log_message(f"'{e_image_path}' 로드 성공")
    except FileNotFoundError:
        imgOrg_E = None
        log_message(f"오류: '{e_image_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        imgOrg_E = None
        log_message(f"'{e_image_path}' 로드 중 오류: {e}")

    # 자동화 로직을 별도 스레드에서 실행
    automation_thread = threading.Thread(target=automation_logic, daemon=True)
    automation_thread.start()

    log_message("** 프로그램 시작 **")
    if imgOrg_Q is None or imgOrg_E is None:
        log_message("경고: 이미지 파일이 제대로 로드되지 않았습니다. 기능이 동작하지 않을 수 있습니다.")
    else:
        log_message("GUI 버튼을 사용하여 제어하세요.")
    
    # GUI 메인 루프


