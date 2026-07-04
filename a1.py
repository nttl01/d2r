

from imp_ocr import *

# img_name = "D2R_20260704_010847_inven.png"

# x, y = 1792, 66
# x2, y2 = 1908, 112
# result = myOcr(img_name,  x, y, x2, y2)
# print(f"--- 영역 지정 완료: 좌상단({x}, {y}) ~ 우하단({x2}, {y2}) ===> {result}")

# # hp 량 감지
# x, y = 486, 910
# x2, y2 = 650, 940
# result = myOcr(img_name,  x, y, x2, y2, "NUM_ONLY")
# print(f"--- 영역 지정 완료: 좌상단({x}, {y}) ~ 우하단({x2}, {y2}) ===> {result}")

# # mp 량 감지
# x, y = 1300, 910
# x2, y2 = 1470, 940
# result = myOcr(img_name,  x, y, x2, y2,"NUM_ONLY")
# print(f"--- 영역 지정 완료: 좌상단({x}, {y}) ~ 우하단({x2}, {y2}) ===> {result}")

#================================
img_name = "name.png"
x, y = 840, 300
x2, y2 = 1480, 622
result = myOcr(img_name,  x, y, x2, y2)
print(f"--- 영역 지정 완료: 좌상단({x}, {y}) ~ 우하단({x2}, {y2}) ===> {result}")
