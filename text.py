import pytesseract
from PIL import Image
import os
import cv2
import time # 시간 측정을 위해 time 모듈 임포트

def find_all_text_locations(image_path, text_to_find, tesseract_cmd_path, min_confidence=30):
    """
    여러 이미지 전처리 방식을 시도하고 결과를 종합하여 인식률을 극대화합니다.
    """
    if not os.path.exists(image_path):
        return f"오류: 이미지를 찾을 수 없습니다: {image_path}"

    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path

    try:
        original_image = cv2.imread(image_path)
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        # 1. 여러 버전의 이미지를 준비합니다.
        images_to_process = {
            'original': original_image,
            'gray': gray,
            'binary': cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            'binary_inv': cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        }

        all_found_items = []

        # 2. 각 이미지 버전에 대해 OCR을 실행합니다.
        for method, image_data in images_to_process.items():
            data = pytesseract.image_to_data(image_data, lang='kor', output_type=pytesseract.Output.DICT)
            
            words = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) != -1 and data['text'][i].strip() != "":
                    words.append({
                        'text': data['text'][i],
                        'conf': int(data['conf'][i]),
                        'coords': (data['left'][i], data['top'][i])
                    })

            text_len = len(text_to_find)
            for i in range(len(words) - text_len + 1):
                sequence = "".join([words[j]['text'] for j in range(i, i + text_len)])
                if sequence == text_to_find:
                    avg_conf = sum([words[j]['conf'] for j in range(i, i + text_len)]) / text_len
                    if avg_conf >= min_confidence:
                        all_found_items.append({
                            'text': sequence,
                            'coords': words[i]['coords'],
                            'confidence': avg_conf
                        })

        # 3. 중복된 결과를 제거하여 최종 목록을 만듭니다.
        if not all_found_items:
            return []

        final_results = []
        for item in sorted(all_found_items, key=lambda x: x['confidence'], reverse=True):
            is_duplicate = False
            for final_item in final_results:
                # 좌표가 10픽셀 이내로 가까우면 중복으로 간주합니다.
                if abs(item['coords'][0] - final_item['coords'][0]) < 10 and abs(item['coords'][1] - final_item['coords'][1]) < 10:
                    is_duplicate = True
                    break
            if not is_duplicate:
                final_results.append(item)
        
        return final_results

    except FileNotFoundError:
        return f"오류: Tesseract를 찾을 수 없습니다. 지정된 경로를 확인하세요: {tesseract_cmd_path}"
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

if __name__ == "__main__":
    start_time = time.time() # 프로그램 시작 시간 기록

    tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    image_filename = "name.png"
    text_to_search = "열쇠"

    # 여러 방법을 시도하므로, 신뢰도 임계값을 약간 낮춥니다 (30).
    results = find_all_text_locations(image_filename, text_to_search, tesseract_path, min_confidence=30)

    if isinstance(results, list) and results:
        print(f"이미지에서 '{text_to_search}' 글자를 {len(results)}개 찾았습니다.")
        # 좌표 순서로 정렬하여 출력
        sorted_results = sorted(results, key=lambda x: (x['coords'][1], x['coords'][0]))
        for i, item in enumerate(sorted_results):
            print(f"  순번 {i+1}: 좌표 (x, y) = {item['coords']} (평균 신뢰도: {item['confidence']:.2f}%)")
    elif isinstance(results, list) and not results:
        print(f"이미지에서 '{text_to_search}' 글자를 찾지 못했습니다.")
    else:
        print(results) # 오류 메시지 출력

    end_time = time.time() # 프로그램 종료 시간 기록
    print(f"\n프로그램 수행 시간: {end_time - start_time:.2f}초")
