import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scale (Slider) Example")
root.geometry("300x100")

# --- 스타일 설정 ---
style = ttk.Style()
# 'clam' 테마는 스타일링에 더 유연합니다.
try:
    style.theme_use('clam')
except tk.TclError:
    # clam 테마를 사용할 수 없는 경우, 의도한 대로 보이지 않을 수 있습니다.
    pass

# 'On' 상태는 녹색으로 설정합니다.
# default_trough_color = style.lookup('TScale', 'troughcolor')

style.configure("On.Horizontal.TScale", troughcolor='green')
style.configure("Off.Horizontal.TScale", troughcolor='grey')


scale_frame = ttk.LabelFrame(root, text="Scale (Slider)")
scale_frame.pack(pady=10, padx=10, fill="x")

scale_var = tk.IntVar()
scale_label = tk.Label(scale_frame, text="Off", width=10)

scale = ttk.Scale(
    scale_frame,
    from_=0,
    to=1,
    orient="horizontal",
    variable=scale_var,
)

def on_scale_change(value):
    if scale_var.get() == 1:
        scale_label.config(text="On")
        scale.configure(style="On.Horizontal.TScale")
    else:
        scale_label.config(text="Off")
        scale.configure(style="Off.Horizontal.TScale")

scale.config(command=on_scale_change)

# 초기 상태 설정
on_scale_change(None)

scale.pack(side="left", padx=5)
scale_label.pack(side="left")

root.mainloop()