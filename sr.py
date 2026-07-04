from PIL import Image

def crop_image(input_path, output_path, left, top, width, height):
    """
    이미지를 잘라 지정된 경로에 저장합니다.

    :param input_path: 원본 이미지 파일 경로
    :param output_path: 저장할 이미지 파일 경로
    :param left: 자르기 시작할 왼쪽 x 좌표
    :param top: 자르기 시작할 위쪽 y 좌표
    :param width: 자를 너비
    :param height: 자를 높이
    """
    try:
        # 이미지 열기
        with Image.open(input_path) as img:
            # 자를 영역 설정 (left, top, right, bottom)
            box = (left, top, left + width, top + height)
            
            # 이미지 자르기
            cropped_img = img.crop(box)
            
            # 자른 이미지 저장
            cropped_img.save(output_path)
            
            print(f"이미지를 성공적으로 잘라 '{output_path}'에 저장했습니다.")

    except FileNotFoundError:
        print(f"오류: '{input_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"이미지 처리 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # --- 설정값 ---
    INPUT_IMAGE_PATH = "d2r.png"
    
    # 시작 좌표 및 크기
    INITIAL_X = 1398
    INITIAL_Y = 589
    CROP_WIDTH = 42
    CROP_HEIGHT = 42
    
    # 반복 설정
    HORIZONTAL_REPEATS = 10  # 가로 반복 횟수
    VERTICAL_REPEATS = 4     # 세로 반복 횟수
    X_INCREMENT = 49         # 가로 이동 픽셀
    Y_INCREMENT = 49         # 세로 이동 픽셀

    # --- 이미지 캡처 루프 ---
    capture_number = 1
    for h_idx in range(HORIZONTAL_REPEATS):
        current_x = INITIAL_X + (h_idx * X_INCREMENT)
        for v_idx in range(VERTICAL_REPEATS):
            current_y = INITIAL_Y + (v_idx * Y_INCREMENT)
            
            # 저장할 파일명 생성 (s1_x,y.png, s2_x,y.png, ...)
            output_filename = f"s{capture_number}_{current_x},{current_y}.png"
            
            # 이미지 자르기 함수 호출
            crop_image(
                input_path=INPUT_IMAGE_PATH,
                output_path=output_filename,
                left=current_x,
                top=current_y,
                width=CROP_WIDTH,
                height=CROP_HEIGHT
            )
            capture_number += 1
