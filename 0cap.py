# pip install paddlepaddle

# ocr_test.py
from PIL import Image
from paddleocr import PaddleOCR
import os

# PaddleOCR 인스턴스 초기화 (전역 변수 또는 싱글턴 패턴으로 한 번만 초기화)
paddleocr_instance = None

def initialize_paddleocr():
    """PaddleOCR 인스턴스를 초기화하고 반환합니다. 싱글턴 패턴으로 한 번만 초기화되도록 합니다."""
    global paddleocr_instance
    if paddleocr_instance is None:
        print("PaddleOCR 모델을 초기화하는 중입니다. (처음 실행 시 모델 다운로드 필요)")
        # lang='ko'는 한국어 모델을 사용하겠다는 의미입니다.
        # use_gpu=False는 CPU를 사용하겠다는 의미입니다. GPU가 있다면 True로 변경하세요.
        # show_log=False로 설정하면 콘솔에 PaddleOCR 로그가 출력되지 않습니다.
        paddleocr_instance = PaddleOCR(lang='ko', use_gpu=False, show_log=False)
        print("PaddleOCR 모델 초기화 완료.")
    return paddleocr_instance

def ocr_specific_region_with_paddleocr(image_path, x, y, width, height):
    """
    이미지의 특정 영역에 PaddleOCR을 적용하는 함수

    Args:
        image_path (str): 이미지 파일 경로
        x (int): 영역의 좌측 상단 x 좌표
        y (int): 영역의 좌측 상단 y 좌표
        width (int): 영역의 너비
        height (int): 영역의 높이

    Returns:
        str: 추출된 텍스트 (줄바꿈 포함), 추출된 텍스트가 없으면 빈 문자열
    """
    try:
        # PaddleOCR 인스턴스 초기화 (한 번만 실행되도록)
        ocr = initialize_paddleocr()

        # 이미지 열기
        img = Image.open(image_path)

        # 특정 영역 추출 (crop)
        # crop 함수의 인자는 (left, upper, right, lower)
        # right = x + width, lower = y + height
        cropped_img = img.crop((x, y, x + width, y + height))

        # 잘라낸 이미지를 임시 파일로 저장 (PaddleOCR은 파일 경로 또는 numpy array를 입력으로 받음)
        temp_img_path = "temp_cropped_image.png"
        cropped_img.save(temp_img_path)

        # 추출된 영역에 OCR 적용
        result = ocr.ocr(temp_img_path, cls=True)

        extracted_texts = []
        if result and result[0]:
            for line in result[0]:
                text = line[1][0]
                extracted_texts.append(text)

        # 임시 파일 삭제
        os.remove(temp_img_path)

        return "\n".join(extracted_texts).strip() if extracted_texts else ""

    except Exception as e:
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        return f"OCR 처리 중 오류 발생: {e}"

# --- 사용 예시 ---
example_image_path = "d2r.png"
region_x, region_y, region_width, region_height = 1790,70,250, 100

if not os.path.exists(example_image_path):
    print(f"이미지 파일 '{example_image_path}'을(를) 찾을 수 없습니다.")
    print("테스트를 위해 예시 이미지 파일을 생성합니다.")
    try:
        temp_test_image = Image.new('RGB', (500, 200), color = 'white')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(temp_test_image)
        # Windows 기본 폰트 경로 (예: 맑은 고딕)
        font_path_win = "C:/Windows/Fonts/malgunbd.ttf"
        font = None
        if os.path.exists(font_path_win):
            try:
                font = ImageFont.truetype(font_path_win, 20)
            except Exception as e:
                print(f"맑은 고딕 폰트 로딩 오류: {e}. 기본 폰트를 사용합니다.")
        if font is None:
            font = ImageFont.load_default() # 기본 폰트 로드
            print("경고: 맑은 고딕 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")

        draw.text((110, 60), "안녕하세요 PaddleOCR!", fill=(0,0,0), font=font)
        draw.text((110, 80), "Hello PaddleOCR!", fill=(0,0,0), font=font)
        temp_test_image.save(example_image_path)
        print(f"'{example_image_path}' 파일이 생성되었습니다. 이제 OCR을 테스트할 수 있습니다.")
    except Exception as create_e:
        print(f"테스트 이미지 생성 중 오류 발생: {create_e}")
else:
    print(f"이미지 파일 '{example_image_path}'을(를) 찾았습니다. OCR을 시작합니다.")

# 실제 OCR 실행
result_text = ocr_specific_region_with_paddleocr(example_image_path, region_x, region_y, region_width, region_height)
print(f"\nPaddleOCR로 추출된 텍스트:\n{result_text}")

