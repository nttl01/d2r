from PIL import Image
import imagehash
import math
from collections import Counter
import colorsys
import numpy as np # New dependency
from sklearn.cluster import KMeans # New dependency

# --- pHash 유사도 계산 함수 (기존 유지) ---
def calculate_phash_similarity(img_a, img_b):
    """pHash를 사용하여 구조적 유사도를 0-100%로 계산합니다."""
    hash_a = imagehash.phash(img_a)
    hash_b = imagehash.phash(img_b)
    hamming_distance = hash_a - hash_b
    return (1 - (hamming_distance / 64)) * 100

# --- K-Means 클러스터링 기반 주요 색상 계열 추출 함수 ---
def get_dominant_color_family_kmeans(img, k=3, exclude_threshold=20):
    """
    K-Means 클러스터링을 사용하여 이미지에서 검정색 배경을 제외하고
    가장 지배적인 색상 계열을 반환합니다.
    k: 찾을 지배적인 색상의 개수 (클러스터 개수)
    exclude_threshold: 이 값보다 낮은 RGB 값은 검정색으로 간주하여 제외합니다.
    """
    # 이미지 크기 조정 (K-Means 성능 향상 및 속도 개선)
    img_resized = img.resize((100, 100)) # Resizing for faster processing
    pixels = np.array(img_resized.getdata())

    # 검정색 또는 매우 어두운 픽셀 필터링
    non_black_pixels = pixels[
        (pixels[:, 0] >= exclude_threshold) |
        (pixels[:, 1] >= exclude_threshold) |
        (pixels[:, 2] >= exclude_threshold)
    ]

    if len(non_black_pixels) == 0: # 필터링 후 픽셀이 없으면
        return "주요 색상 없음 (모두 검정색 또는 어두움)"

    # K-Means 클러스터링 적용
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10) # n_init 추가
    kmeans.fit(non_black_pixels)

    # 각 클러스터의 픽셀 수 계산
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    
    # 가장 많은 픽셀을 가진 클러스터의 중심 색상 (RGB)
    dominant_cluster_index = labels[np.argmax(counts)]
    dominant_rgb = kmeans.cluster_centers_[dominant_cluster_index].astype(int)

    r, g, b = dominant_rgb

    # RGB를 0-1 범위로 정규화 후 HSV로 변환
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

    # 채도(Saturation)가 낮으면 회색 계열로 간주 (0.1 이하)
    # 밝기(Value)가 너무 낮거나 높으면 제외 (0.1 이하, 0.95 이상)
    if s < 0.1:
        return "회색 계열 (K-Means)"
    if v < 0.1:
        return "어두운 계열 (K-Means)"
    if v > 0.95:
        return "흰색 계열 (K-Means)"

    # Hue 값에 따른 색상 계열 분류 (기존 HSV 범위 사용)
    hue_degrees = int(h * 360)

    if (hue_degrees >= 340 or hue_degrees < 20): # Red (slightly wider)
        return "빨강 계열 (K-Means)"
    elif (hue_degrees >= 20 and hue_degrees < 80): # Orange/Yellow
        return "주황/노랑 계열 (K-Means)"
    elif (hue_degrees >= 80 and hue_degrees < 160): # Green
        return "초록 계열 (K-Means)"
    elif (hue_degrees >= 160 and hue_degrees < 230): # Cyan/Light Blue
        return "청록/하늘 계열 (K-Means)"
    elif (hue_degrees >= 230 and hue_degrees < 290): # Blue
        return "파랑 계열 (K-Means)"
    elif (hue_degrees >= 290 and hue_degrees < 340): # Magenta/Purple
        return "자홍/보라 계열 (K-Means)"
    else:
        return "기타 색상 (K-Means)"

def analyze_images(path_a, path_b, return_results=False):
    """
    두 이미지의 구조 유사도와 각 이미지의 주요 색상 계열을 분석합니다.
    return_results가 True이면 결과를 딕셔너리로 반환합니다.
    """
    try:
        img_a = Image.open(path_a)
        img_b = Image.open(path_b)

        # 1. 구조 유사도 (pHash)
        phash_sim = calculate_phash_similarity(img_a, img_b)
        
        # 2. 각 이미지의 주요 색상 계열 분석 (K-Means 사용)
        dominant_color_a = get_dominant_color_family_kmeans(img_a)
        dominant_color_b = get_dominant_color_family_kmeans(img_b)

        # 종합 평가
        overall_evaluation = ""
        if dominant_color_a == dominant_color_b and phash_sim > 80: # 예시 임계값
            overall_evaluation = "유사함"
        elif dominant_color_a != dominant_color_b and phash_sim > 80:
            overall_evaluation = "구조유사, 색상다름"
        else:
            overall_evaluation = "유사하지 않음"

        if return_results:
            return {
                'phash_sim': phash_sim,
                'dominant_color_a': dominant_color_a,
                'dominant_color_b': dominant_color_b,
                'overall_evaluation': overall_evaluation
            }
        else:
            print(f"--- '{path_a}' 분석 ---")
            print(f"  주요 색상 계열: {dominant_color_a}")
            print(f"--- '{path_b}' 분석 ---")
            print(f"  주요 색상 계열: {dominant_color_b}")
            print("-" * 20)
            print(f"두 이미지의 구조 유사도 (pHash): {phash_sim:.2f}%")
            print(f"=> {overall_evaluation}")
            return None # No results to return if not requested

    except FileNotFoundError as e:
        if return_results:
            return None
        else:
            print(f"오류: 파일을 찾을 수 없습니다. ({e})")
            return None
    except Exception as e:
        if return_results:
            return None
        else:
            print(f"오류가 발생했습니다: {e}")
            return None

if __name__ == "__main__":
    REFERENCE_IMAGE = "s1.png"
    
    print(f"--- '{REFERENCE_IMAGE}'를 기준으로 다른 이미지들과 비교 ---\n")
    print("대상파일명\t구조유사도(%)\t참조색상계열\t대상색상계열\t종합평가")
    print("-" * 80)

    # s1.png의 주요 색상 계열을 미리 분석
    try:
        img_ref = Image.open(REFERENCE_IMAGE)
        dominant_color_ref = get_dominant_color_family_kmeans(img_ref)
    except Exception as e:
        print(f"오류: 참조 이미지 '{REFERENCE_IMAGE}' 분석 중 오류 발생: {e}")
        dominant_color_ref = "분석불가"

    for i in range(2, 41): # s2.png 부터 s40.png 까지
        target_image = f"s{i}.png"
        
        result = analyze_images(REFERENCE_IMAGE, target_image, return_results=True)
        
        if result:
            phash_sim = result['phash_sim']
            dominant_color_target = result['dominant_color_b'] # target image's dominant color
            overall_evaluation = ""
            
            if dominant_color_ref == dominant_color_target and phash_sim > 80:
                overall_evaluation = "유사함"
            elif dominant_color_ref != dominant_color_target and phash_sim > 80:
                overall_evaluation = "구조유사, 색상다름"
            else:
                overall_evaluation = "유사하지 않음"
            
            print(f"{target_image}\t{phash_sim:.2f}\t{dominant_color_ref}\t{dominant_color_target}\t{overall_evaluation}")
        else:
            print(f"{target_image}\t오류 발생")
