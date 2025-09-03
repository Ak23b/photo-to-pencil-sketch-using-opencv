import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# ======================
# Filters
# ======================
def apply_grayscale():
    global img, panel
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        display_image(gray, is_gray=True)

def apply_blur():
    global img, panel
    if img is not None:
        blurred = cv2.GaussianBlur(img, (7, 7), 0)
        display_image(blurred)

def apply_sharpen():
    global img, panel
    if img is not None:
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(img, -1, kernel)
        display_image(sharpened)

def apply_edge_detection():
    global img, panel
    if img is not None:
        edges = cv2.Canny(img, 100, 200)
        display_image(edges, is_gray=True)

# ======================
# Editor
# ======================
def increase_brightness():
    global img, panel
    if img is not None:
        bright = cv2.convertScaleAbs(img, alpha=1, beta=40)
        display_image(bright)

def decrease_brightness():
    global img, panel
    if img is not None:
        dark = cv2.convertScaleAbs(img, alpha=1, beta=-40)
        display_image(dark)

def rotate_image():
    global img, panel
    if img is not None:
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, 45, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        display_image(rotated)

def resize_image():
    global img, panel
    if img is not None:
        resized = cv2.resize(img, None, fx=0.5, fy=0.5)
        display_image(resized)

# ======================
# Webcam
# ======================
def start_webcam():
    global cap, webcam_running
    if not webcam_running:
        cap = cv2.VideoCapture(0)
        webcam_running = True
        update_webcam()

def stop_webcam():
    global cap, webcam_running
    if webcam_running:
        webcam_running = False
        cap.release()

def update_webcam():
    global cap, webcam_running, webcam_panel
    if webcam_running:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
            webcam_panel.imgtk = imgtk
            webcam_panel.config(image=imgtk)
        webcam_panel.after(20, update_webcam)

# ======================
# Helpers
# ======================
def open_image():
    global img, panel
    path = filedialog.askopenfilename()
    if path:
        img = cv2.imread(path)
        display_image(img)

def display_image(cv_img, is_gray=False):
    global panel, img
    if not is_gray:
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv_img))
    panel.imgtk = imgtk
    panel.config(image=imgtk)
    img = cv_img if not is_gray else cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)

# ======================
# Main App
# ======================
root = tk.Tk()
root.title("Vision Studio")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Tabs
filters_tab = tk.Frame(notebook, bg="white")
editor_tab = tk.Frame(notebook, bg="white")
webcam_tab = tk.Frame(notebook, bg="white")

notebook.add(filters_tab, text="Filters")
notebook.add(editor_tab, text="Editor")
notebook.add(webcam_tab, text="Webcam")

# Global variables
img = None
cap = None
webcam_running = False

# Shared image panel
panel = tk.Label(root)
panel.pack(side="bottom", pady=10)

# Webcam panel
webcam_panel = tk.Label(webcam_tab)
webcam_panel.pack(pady=10)

# ======================
# Button Colors
# ======================
FILTER_BTN_COLOR = "#ADD8E6"   # Light Blue
EDITOR_BTN_COLOR = "#FFC0CB"   # Pink
WEBCAM_BTN_COLOR = "#FFA500"   # Orange

# ======================
# Filters tab buttons
# ======================
tk.Button(filters_tab, text="Open Image", bg=FILTER_BTN_COLOR, command=open_image).pack(pady=5)
tk.Button(filters_tab, text="Grayscale", bg=FILTER_BTN_COLOR, command=apply_grayscale).pack(pady=5)
tk.Button(filters_tab, text="Blur", bg=FILTER_BTN_COLOR, command=apply_blur).pack(pady=5)
tk.Button(filters_tab, text="Sharpen", bg=FILTER_BTN_COLOR, command=apply_sharpen).pack(pady=5)
tk.Button(filters_tab, text="Edge Detection", bg=FILTER_BTN_COLOR, command=apply_edge_detection).pack(pady=5)

# ======================
# Editor tab buttons
# ======================
tk.Button(editor_tab, text="Increase Brightness", bg=EDITOR_BTN_COLOR, command=increase_brightness).pack(pady=5)
tk.Button(editor_tab, text="Decrease Brightness", bg=EDITOR_BTN_COLOR, command=decrease_brightness).pack(pady=5)
tk.Button(editor_tab, text="Rotate", bg=EDITOR_BTN_COLOR, command=rotate_image).pack(pady=5)
tk.Button(editor_tab, text="Resize", bg=EDITOR_BTN_COLOR, command=resize_image).pack(pady=5)

# ======================
# Webcam tab buttons
# ======================
tk.Button(webcam_tab, text="Start Webcam", bg=WEBCAM_BTN_COLOR, command=start_webcam).pack(pady=5)
tk.Button(webcam_tab, text="Stop Webcam", bg=WEBCAM_BTN_COLOR, command=stop_webcam).pack(pady=5)

root.mainloop()
