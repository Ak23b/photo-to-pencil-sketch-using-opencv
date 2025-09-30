import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


# Global variables
img = None
panel = None
cap = None


# Button colors
FILTER_BTN_COLOR = "#ADD8E6"   # Light Blue
EDITOR_BTN_COLOR = "#FFC0CB"   # Pink
WEBCAM_BTN_COLOR = "#FFA500"   # Orange


# ----------------- Image Display -----------------
def display_image(cv_img, is_gray=False):
    global panel, img
    # Convert grayscale images properly
    if not is_gray:
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)


    # Resize to fit window (max 700x400)
    max_w, max_h = 700, 400
    h, w = cv_img.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)  # shrink if too big
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(cv_img, (new_w, new_h))


    imgtk = ImageTk.PhotoImage(image=Image.fromarray(resized))
    panel.imgtk = imgtk
    panel.config(image=imgtk)


    # Store original image (full res) for processing
    img = cv_img if not is_gray else cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)

# ----------------- File Handling -----------------
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    if filepath:
        cv_img = cv2.imread(filepath)
        display_image(cv_img)


# ----------------- Filters -----------------
def apply_grayscale():
    global img
    if img is None: return
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    display_image(gray, is_gray=True)

def apply_blur():
    global img
    if img is None: return
    blurred = cv2.GaussianBlur(img, (15, 15), 0)
    display_image(blurred)

def apply_sharpen():
    global img
    if img is None: return
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    display_image(sharpened)

def apply_edge_detection():
    global img
    if img is None: return
    edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), 100, 200)
    display_image(edges, is_gray=True)

# ----------------- Editor -----------------
def increase_brightness():
    global img
    if img is None: return
    bright = cv2.convertScaleAbs(img, alpha=1, beta=50)
    display_image(bright)

def decrease_brightness():
    global img
    if img is None: return
    dark = cv2.convertScaleAbs(img, alpha=1, beta=-50)
    display_image(dark)

def rotate_image():
    global img
    if img is None: return
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    display_image(rotated)

def resize_image():
    global img
    if img is None: return
    h, w = img.shape[:2]
    resized = cv2.resize(img, (w//2, h//2))
    display_image(resized)

# ----------------- Webcam -----------------
def start_webcam():
    global cap
    cap = cv2.VideoCapture(0)
    show_frame()

def show_frame():
    global cap, panel
    if cap is not None and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(frame, (700, 400))
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(resized))
            panel.imgtk = imgtk
            panel.config(image=imgtk)
        panel.after(10, show_frame)

def stop_webcam():
    global cap
    if cap is not None:
        cap.release()
        messagebox.showinfo("Webcam", "Webcam stopped.")

# ----------------- GUI -----------------
app = tk.Tk()
app.title("Vision Studio")
app.geometry("900x600")

notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both")

# Image display panel
panel = tk.Label(app)
panel.pack()

# Filters Tab
filters_tab = ttk.Frame(notebook)
notebook.add(filters_tab, text="Filters")

tk.Button(filters_tab, text="Grayscale", bg=FILTER_BTN_COLOR, command=apply_grayscale).pack(pady=5)
tk.Button(filters_tab, text="Blur", bg=FILTER_BTN_COLOR, command=apply_blur).pack(pady=5)
tk.Button(filters_tab, text="Sharpen", bg=FILTER_BTN_COLOR, command=apply_sharpen).pack(pady=5)
tk.Button(filters_tab, text="Edge Detection", bg=FILTER_BTN_COLOR, command=apply_edge_detection).pack(pady=5)

# Editor Tab
editor_tab = ttk.Frame(notebook)
notebook.add(editor_tab, text="Editor")

tk.Button(editor_tab, text="Increase Brightness", bg=EDITOR_BTN_COLOR, command=increase_brightness).pack(pady=5)
tk.Button(editor_tab, text="Decrease Brightness", bg=EDITOR_BTN_COLOR, command=decrease_brightness).pack(pady=5)
tk.Button(editor_tab, text="Rotate", bg=EDITOR_BTN_COLOR, command=rotate_image).pack(pady=5)
tk.Button(editor_tab, text="Resize", bg=EDITOR_BTN_COLOR, command=resize_image).pack(pady=5)

# Webcam Tab
webcam_tab = ttk.Frame(notebook)
notebook.add(webcam_tab, text="Webcam")

tk.Button(webcam_tab, text="Start Webcam", bg=WEBCAM_BTN_COLOR, command=start_webcam).pack(pady=5)
tk.Button(webcam_tab, text="Stop Webcam", bg=WEBCAM_BTN_COLOR, command=stop_webcam).pack(pady=5)

# File Menu
menubar = tk.Menu(app)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open Image", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menubar.add_cascade(label="File", menu=file_menu)
app.config(menu=menubar)

app.mainloop()