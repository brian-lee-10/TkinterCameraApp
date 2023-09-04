from tkinter import *
from PIL import Image, ImageTk
from queue import Queue
import numpy as np
import cv2
import threading 

# --- VARIABLES --- #
res = (320, 240)
available_cam = []
camera_index = 0
camera_num = 0
key_num = 0

# Initialize Camera
cam = cv2.VideoCapture(camera_index)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])

# Create queue
frame_queue = Queue(maxsize=1)

# --- FUNCTIONS --- # 
# Camera thread
def camera_thread():
    while True:
        ret, frame = cam.read() 

        # Check if frame is loaded
        if ret:
            frame = np.rot90(frame, key_num)
            
            # Add frame to queue
            frame_queue.put(frame)

# GUI thread
def gui_update():  
    if not frame_queue.empty():
        frame = frame_queue.get()
        
        opencvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(opencvImage)
        imgtk = ImageTk.PhotoImage(image=img) 
        
        label_widget.imgtk = imgtk
        label_widget.configure(image=imgtk)
      
    label_widget.after(10, gui_update)

def list_cams():
    is_working = True
    index = 0
    global available_cam, frame
    while is_working:
        camera = cv2.VideoCapture(index)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, frame = camera.read()
            if is_reading:
                available_cam.append(index)
        index +=1
    camera.release()

def resize_window():
    if key_num == 0 or key_num == 2:
        root.geometry(f"{res[0]}x{res[1]}")
    if key_num == 1 or key_num ==3:
        root.geometry(f"{res[1]}x{res[0]}")  

def set_res(new_res):
    global res
    res = new_res
  
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, res[0])
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, res[1])
    resize_window()

def rotate_cam():
    global key_num
    key_num = key_num+1
    if key_num >= 4:
        key_num = 0
    resize_window()  

def cycle_cameras(num):
    global camera_index, cam, res

    camera_index = num
    cam.release()
    cam = cv2.VideoCapture(camera_index)
    set_res(res)
    

def set_res_320():
    set_res((320, 240))

def set_res_640():
    set_res((640, 480))

def set_res_800():
    set_res((800,600))

def exit_app():
    root.quit()
    cam.release()
    camera_thread.join()
    root.destroy()

# --- Find Number of Cameras --- #
list_cams()
camera_num = len(available_cam)

# --- Start Camera Thread --- #
camera_thread = threading.Thread(target=camera_thread)
camera_thread.start()

# Create tk app
root = Tk()
root.title("Webcam")
root.geometry(f"{res[0]}x{res[1]}")
root.bind('<Escape>', lambda e: exit_app()) 

# --- Rotate Button --- #
button1 = Button(root, text="Rotate", command=rotate_cam)
button1.pack()
button1.config(font=("Helvetica", 16))

# --- Exit Button --- # 
exit_button = Button(root, text="Exit App", command=exit_app)
exit_button.pack()
exit_button.config(font=("Helvetica", 16))

# --- Label --- #
label_widget = Label(root)
label_widget.pack(fill=BOTH, expand=YES)

# --- Menu --- #
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="320x240", command=set_res_320)
file_menu.add_command(label="640x480", command=set_res_640)
file_menu.add_command(label="800x600", command=set_res_800)

camera_menu = Menu(menu_bar, tearoff=0)
for i in range(camera_num):
    item_label = f"Camera {i + 1}"
    camera_menu.add_command(label=item_label, command=lambda i=i: cycle_cameras(i))

menu_bar.add_cascade(label="Resolution", menu=file_menu)
menu_bar.add_cascade(label="Cameras", menu=camera_menu)
root.config(menu=menu_bar)

gui_update() 
root.mainloop()