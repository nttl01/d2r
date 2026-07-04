from PIL import Image
import numpy as np

# --- 코사인 유사도 계산 함수 ---
def cosine_similarity(img1, img2):
    array1 = np.array(img1)
    array2 = np.array(img2)
    assert array1.shape == array2.shape
    
    h, w, c = array1.shape
    len_vec = h * w * c
    vector_1 = array1.reshape(len_vec,) / 255.
    vector_2 = array2.reshape(len_vec,) / 255.

    cosine_sim = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))
    return cosine_sim

def analyze_images_cosine_only(path_a, path_b, return_results=False):
    """
    두 이미지의 코사인 유사도를 분석합니다.
    return_results가 True이면 결과를 딕셔너리로 반환합니다.
    """
    try:
        img_a = Image.open(path_a)
        img_b = Image.open(path_b)

        # 코사인 유사도 계산
        cos_sim = cosine_similarity(img_a, img_b) * 100 # 백분율로 변환

        if return_results:
            return {
                'cosine_sim': cos_sim
            }
        else:
            print(f"--- '{path_a}' vs '{path_b}' 코사인 유사도 ---")
            print(f"결과: {cos_sim:.2f}%")
            return None

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
    REFERENCE_IMAGE = "s27.png"
    SIMILARITY_THRESHOLD = 98.0 # 유사 판단 기준

    print(f"--- '{REFERENCE_IMAGE}'를 기준으로 다른 이미지들과 코사인 유사도 비교 ---")
    print("대상파일명\t코사인유사도(轵)\t유사여부") # Updated header
    print("-" * 50) # Adjust separator length

    for i in range(2, 41): # s2.png 부터 s40.png 까지
        target_image = f"s{i}.png"
        
        result = analyze_images_cosine_only(REFERENCE_IMAGE, target_image, return_results=True)
        
        if result:
            cos_sim = result['cosine_sim']
            
            similarity_status = "유사" if cos_sim >= SIMILARITY_THRESHOLD else "비유사" # New logic
            
            print(f"{target_image}\t{cos_sim:.2f}\t{similarity_status}") # Updated print
        else:
            print(f"{target_image}\t오류 발생\t-") # Updated error print
