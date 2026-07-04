import time
import sys
import threading

def _spinner_animation(stop_event, text):
    """내부에서 사용되는 스피너 애니메이션 함수"""
    # Gemini UI와 동일한 점자 문자 시퀀스
    braille_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    
    i = 0
    while not stop_event.is_set():
        # 회전 문자와 텍스트를 함께 출력
        sys.stdout.write(f"\r{braille_chars[i]} {text}")
        sys.stdout.flush()
        i = (i + 1) % len(braille_chars)
        time.sleep(0.08) # 부드러운 애니메이션을 위한 속도 조절
    # 작업 완료 후 줄을 깨끗이 지웁니다.
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")
    sys.stdout.flush()

class BrailleSpinner:
    """
    with 구문과 함께 사용하는 점자 스피너 컨텍스트 매니저 (Gemini 스타일).

    사용 예시:
    with BrailleSpinner("처리 중..."):
        time.sleep(5)
    """
    def __init__(self, text="진행 중..."):
        self._text = text
        self._stop_spinner = threading.Event()
        self._spinner_thread = None

    def __enter__(self):
        """with 구문 시작 시 커서를 숨기고 스피너 스레드를 시작합니다."""
        sys.stdout.write('\033[?25l')  # 커서 숨기기
        sys.stdout.flush()
        self._spinner_thread = threading.Thread(
            target=_spinner_animation,
            args=(self._stop_spinner, self._text)
        )
        self._spinner_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """with 구문 종료 시 스피너 스레드를 정지시키고 커서를 다시 표시합니다."""
        self._stop_spinner.set()
        if self._spinner_thread:
            self._spinner_thread.join()
        sys.stdout.write('\033[?25h')  # 커서 보이기
        sys.stdout.flush()

# --- 사용 예시 ---
if __name__ == "__main__":
    print("작업을 시작합니다...")
    with BrailleSpinner("처리 중..."):
        time.sleep(5) # 5초 동안 작업 시뮬레이션
    print("작업이 성공적으로 완료되었습니다!")