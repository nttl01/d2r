import cv2
import numpy as np
import os
import time # 시간 측정을 위해 time 모듈 임포트

def find_all_image_locations(main_image_path, template_image_path, threshold=0.8):
    """
    main_image에서 template_image의 모든 발생 위치를 찾습니다.

    Args:
        main_image_path (str): 메인 이미지 파일 경로
        template_image_path (str): 템플릿 이미지 파일 경로
        threshold (float): 매칭 정확도 임계값

    Returns:
        list: 찾은 모든 템플릿의 좌상단 좌표 (x, y) 목록
    """
    if not os.path.exists(main_image_path):
        return f"오류: 메인 이미지를 찾을 수 없습니다: {main_image_path}"
    if not os.path.exists(template_image_path):
        return f"오류: 템플릿 이미지를 찾을 수 없습니다: {template_image_path}"

    main_image = cv2.imread(main_image_path, cv2.IMREAD_UNCHANGED)
    template_image = cv2.imread(template_image_path, cv2.IMREAD_UNCHANGED)

    if main_image is None:
        return f"오류: 메인 이미지를 읽을 수 없습니다: {main_image_path}"
    if template_image is None:
        return f"오류: 템플릿 이미지를 읽을 수 없습니다: {template_image_path}"

    # 템플릿의 너비와 높이
    t_w, t_h = template_image.shape[:2]

    # 템플릿 매칭 수행
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    
    # 임계값 이상의 위치 찾기
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1])) # (x, y) 좌표로 변환

    if not locations:
        return []

    # 중복된 위치를 그룹화하여 제거 (Non-Maximum Suppression과 유사한 효과)
    points = []
    for loc in locations:
        # 현재 위치가 이미 찾은 그룹에 속하는지 확인
        is_grouped = False
        for group_pt in points:
            if abs(loc[0] - group_pt[0]) < t_w * 0.5 and abs(loc[1] - group_pt[1]) < t_h * 0.5:
                is_grouped = True
                break
        
        if not is_grouped:
            points.append(loc)

    return points

if __name__ == "__main__":
    start_time = time.time() # 프로그램 시작 시간 기록

    main_image_filename = "name.png"
    template_image_filename = "ns.png"

    locations = find_all_image_locations(main_image_filename, template_image_filename, threshold=0.8)

    if isinstance(locations, list) and locations:
        print(f"'{template_image_filename}' 이미지를 '{main_image_filename}'에서 {len(locations)}개 찾았습니다.")
        for i, loc in enumerate(locations):
            print(f"  {i+1}: 좌표 (x, y) = {loc}")
    elif isinstance(locations, list) and not locations:
        print(f"'{template_image_filename}' 이미지를 찾지 못했습니다 (정확도 부족).")
    else:
        print(locations) # 오류 메시지 출력

    end_time = time.time() # 프로그램 종료 시간 기록
    print(f"\n프로그램 수행 시간: {end_time - start_time:.2f}초")
