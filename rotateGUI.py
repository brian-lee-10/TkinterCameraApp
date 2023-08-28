from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import threading 
from queue import Queue

# --- VARIABLES --- #
current_res = (320, 240)
width, height = current_res
key_num = 0

# Initialize Camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create queue
frame_queue = Queue(maxsize=1)

# --- FUNCTIONS --- # 
# Camera thread
def camera_thread():
    while True:
        ret, frame = cam.read() 
        frame = np.rot90(frame, key_num)
        
        if ret:
            # Add frame to queue
            frame_queue.put(frame) 

camera_thread = threading.Thread(target=camera_thread)
camera_thread.start()

# GUI thread
def gui_update():  
    if not frame_queue.empty():
        frame = frame_queue.get()
        
        opencvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(opencvImage)
        imgtk = ImageTk.PhotoImage(image=img) 
        
        label_widget.imgtk = imgtk
        label_widget.configure(image=imgtk)
      
    label_widget.after(10, gui_update)

def resize_window():
    if key_num == 0 or key_num == 2:
        root.geometry(f"{width}x{height}")
    if key_num == 1 or key_num ==3:
        root.geometry(f"{height}x{width}")

def rotate_cam():
    global key_num
    key_num = key_num+1
    if key_num >= 4:
        key_num = 0
    resize_window()    

def set_res(res):
    global width, height
    width, height = res
  
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    resize_window()

def set_res_320():
    set_res((320, 240))

def set_res_640():
    set_res((640, 480))

def set_res_800():
    set_res((800,600))


# --- MAIN --- #
# Create tk app
root = Tk()
root.title("Webcam")
root.geometry(f"{width}x{height}")

# quit app whenever "Escape" is pressed
root.bind('<Escape>', lambda e: root.quit())

button1 = Button(root, text="Rotate Camera", command=rotate_cam)
button1.pack()
button1.config(font=("Helvetica", 16))

# Create a label and display it on app
label_widget = Label(root)
label_widget.pack(fill=BOTH, expand=YES)

# --- Menu --- #
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="320x240", command=set_res_320)
file_menu.add_command(label="640x480", command=set_res_640)
file_menu.add_command(label="800x600", command=set_res_800)

menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

gui_update() 
root.mainloop()
cam.release()