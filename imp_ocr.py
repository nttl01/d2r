import cv2
import pytesseract

# [필수] 1단계에서 설치한 Tesseract 프로그램 실행 파일 경로를 명시합니다.
# 경로 앞에 R을 붙여 원시 문자열로 지정해야 역슬래시(\) 에러가 나지 않습니다.
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract.exe'

def myOcr(pImg_name, x,y,x2,y2, pMode = "ALL" ):
    # 1. 원본 이미지 불러오기
    #img_path = 'd2r.png'
    #image = cv2.imread(pImg_name)
    cropped_image = pImg_name.crop((x,y,x2,y2))
    cropped_image.save("cropped_after.png")

    if cropped_image is None:
        print(f"❌ 이미지를 불러올 수 없습니다. 경로를 확인하세요: {pImg_name}")
        exit()

    # 2. 지정한 좌상단(x, y) ~ 우하단(x2, y2) 영역 좌표 설정
    #x, y = 1792, 66
    #x2, y2 = 1908, 112

    # 3. 이미지 크롭 (OpenCV 행렬 연산은 [y축 범위, x축 범위] 순서입니다)
    #cropped_image = image[y:y2, x:x2]


    if pMode == "ALL" :
        # 4. Tesseract OCR 수행 (한글+영어 언어 지정)
        # --psm 6: 하나의 단어 또는 단일 텍스트 블록으로 간주하여 인식률을 높이는 옵션
        custom_config = r'--psm 6'
    elif pMode == "NUM_ONLY":
        # --psm 7: 잘라낸 이미지가 하나의 단일 텍스트 줄(Line)일 때 최적의 성능을 냅니다.
        # 숫자 및 특수 기호(소수점, 콤마, 금액 등)만 인식 하는 옵션 적용
        custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789.,/ '
    elif pMode == "ENG_ONLY":
        #영어 대문자만 허용 (코드, 알파벳 아이디 등)
        custom_config = r'--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ '
    elif pMode == "CUT_ONLY":
        #특정 문자 차단 (블랙리스트)
        custom_config = r'--psm 6 -c tessedit_char_blacklist=!@#$%^&*()_+'



    # 5. 결과 출력
    #print(f"--- 영역 지정 완료: 좌상단({x}, {y}) ~ 우하단({x2}, {y2}) ---")
    #print(f"인식된 텍스트:\n{text.strip()}")
    #print("실행완료!")


    """
    # 1. 크롭 이미지 내 단어 데이터 추출
    #data = pytesseract.image_to_data(cropped_image, lang='kor+eng', config=custom_config, output_type=pytesseract.Output.DICT)

    print("--- 단어 단위 상대 좌표 결과 ---")
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        # 빈 문자열이나 신뢰도 -1인 블록은 제외
        if int(data['conf'][i]) < 0 or not data['text'][i].strip():
            continue

        word = data['text'][i]
        # 잘라낸 이미지(cropped_image)의 좌상단을 (0,0)으로 잡았을 때의 상대 좌표
        cx = data['left'][i]
        cy = data['top'][i]
        cw = data['width'][i]
        ch = data['height'][i]

        print(f"텍스트: {word} | 크롭내 위치: 좌상단({cx}, {cy}) 크기({cw}x{ch}) | 신뢰도: {data['conf'][i]}%")

    return data
    """

    text = pytesseract.image_to_string(cropped_image, lang='kor+eng', config=custom_config)

    return text



