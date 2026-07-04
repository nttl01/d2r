import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("On/Off Switch Examples")
root.geometry("350x500")

# --- 1. Checkbutton Example ---
check_frame = ttk.LabelFrame(root, text="1. Checkbutton")
check_frame.pack(pady=10, padx=10, fill="x")

check_var = tk.IntVar()
check_label = tk.Label(check_frame, text="Off", width=10)

def on_check_toggle():
    if check_var.get() == 1:
        check_label.config(text="On")
    else:
        check_label.config(text="Off")

check_button = ttk.Checkbutton(check_frame, text="Toggle", variable=check_var, command=on_check_toggle)
check_button.pack(side="left", padx=5)
check_label.pack(side="left")


# --- 2. Button Example ---
button_frame = ttk.LabelFrame(root, text="2. Button")
button_frame.pack(pady=10, padx=10, fill="x")

button_state = tk.BooleanVar(value=False)
button_label = tk.Label(button_frame, text="Off", width=10)

def on_button_toggle():
    button_state.set(not button_state.get())
    if button_state.get():
        button_label.config(text="On")
        toggle_button.config(text="Turn Off")
    else:
        button_label.config(text="Off")
        toggle_button.config(text="Turn On")

toggle_button = ttk.Button(button_frame, text="Turn On", command=on_button_toggle)
toggle_button.pack(side="left", padx=5)
button_label.pack(side="left")


# --- 3. Radiobutton Example ---
radio_frame = ttk.LabelFrame(root, text="3. Radiobuttons")
radio_frame.pack(pady=10, padx=10, fill="x")

radio_var = tk.IntVar(value=0)
radio_label = tk.Label(radio_frame, text="Off", width=10)

def on_radio_select():
    if radio_var.get() == 1:
        radio_label.config(text="On")
    else:
        radio_label.config(text="Off")

on_radio = ttk.Radiobutton(radio_frame, text="On", variable=radio_var, value=1, command=on_radio_select)
off_radio = ttk.Radiobutton(radio_frame, text="Off", variable=radio_var, value=0, command=on_radio_select)
on_radio.pack(side="left", padx=5)
off_radio.pack(side="left", padx=5)
radio_label.pack(side="left")


# --- 4. Scale (Slider) Example ---
scale_frame = ttk.LabelFrame(root, text="4. Scale (Slider)")
scale_frame.pack(pady=10, padx=10, fill="x")

scale_var = tk.IntVar()
scale_label = tk.Label(scale_frame, text="Off", width=10)

def on_scale_change(value):
    if scale_var.get() == 1:
        scale_label.config(text="On")
    else:
        scale_label.config(text="Off")

scale = ttk.Scale(scale_frame, from_=0, to=1, orient="horizontal", variable=scale_var, command=on_scale_change)
scale.pack(side="left", padx=5)
scale_label.pack(side="left")


# --- 5. Clickable Label Example ---
label_frame = ttk.LabelFrame(root, text="5. Clickable Label")
label_frame.pack(pady=10, padx=10, fill="x")

label_state = tk.BooleanVar(value=False)
status_label = tk.Label(label_frame, text="Off", width=10)

def on_label_click(event):
    label_state.set(not label_state.get())
    if label_state.get():
        clickable_label.config(text="[ ON ]", fg="green")
        status_label.config(text="On")
    else:
        clickable_label.config(text="[ OFF ]", fg="red")
        status_label.config(text="Off")

clickable_label = tk.Label(label_frame, text="[ OFF ]", fg="red", cursor="hand2")
clickable_label.pack(side="left", padx=5)
status_label.pack(side="left")
clickable_label.bind("<Button-1>", on_label_click)


root.mainloop()
