from tkinter import *
from PIL import Image, ImageTk
from queue import Queue
import numpy as np
import cv2
import threading 

# --- VARIABLES --- #
cur_res = (320, 240)  # Initial resolution
new_res = (320, 240) # Changed resolution
available_cam = []  # List of available cameras
camera_index = 0  # Index of the currently selected camera
camera_num = 0  # Number of available cameras
new_camera = 0 # Index of newly selected camera
key_num = 0  # Key number for rotation
thread_running = True # Camera thread flag

# Initialize Camera
cam = cv2.VideoCapture(camera_index)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, cur_res[0])
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cur_res[1])

# Create a queue to store frames
frame_queue = Queue(maxsize=1)

# --- FUNCTIONS --- # 

# Camera thread
def camera_thread():
    global thread_running, new_camera, cam, camera_index, cur_res, new_res
    while thread_running:
        ret, frame = cam.read() 

        # Check if selected camera changed
        if new_camera != camera_index:
            camera_index = new_camera
            cam.release()

            cam = cv2.VideoCapture(camera_index)
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, cur_res[0])
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cur_res[1])

        # Check if resolution is changed
        if new_res != cur_res:
            cur_res = new_res
            cam.release

            cam.set(cv2.CAP_PROP_FRAME_WIDTH, cur_res[0])
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, cur_res[1])

            if key_num == 0 or key_num == 2:
                root.geometry(f"{cur_res[0]}x{cur_res[1]}")
            if key_num == 1 or key_num == 3:
                root.geometry(f"{cur_res[1]}x{cur_res[0]}")

        # Check if frame is loaded
        if ret:
            frame = np.rot90(frame, key_num)
            
            # Add frame to queue
            if not frame_queue.full():
                frame_queue.put(frame)
            else:
                pass

# Function to cycle through available cameras
def cycle_cameras(num):
    global new_camera
    new_camera = num

# Function to set the camera resolution
def set_res(res):
    global new_res
    new_res = res

# GUI update function
def gui_update():  
    if not frame_queue.empty():
        frame = frame_queue.get()

        # Convert the OpenCV frame to a Tkinter image
        opencvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(opencvImage)
        imgtk = ImageTk.PhotoImage(image=img) 
        
        label_widget.imgtk = imgtk
        label_widget.configure(image=imgtk)
      
    label_widget.after(10, gui_update)

# Function to list available cameras
def list_cams():
    is_working = True
    index = 0
    global available_cam
    while is_working:
        camera = cv2.VideoCapture(index)
        if not camera.isOpened():
            is_working = False
        else:
            is_reading, frame = camera.read()
            if is_reading:
                available_cam.append(index)
        index += 1
    camera.release()

# Function to resize the window based on the rotation
def resize_window():
    if key_num == 0 or key_num == 2:
        root.geometry(f"{cur_res[0]}x{cur_res[1]}")
    if key_num == 1 or key_num == 3:
        root.geometry(f"{cur_res[1]}x{cur_res[0]}")  

# Function to rotate the camera view
def rotate_cam():
    global key_num
    key_num = key_num + 1
    if key_num >= 4:
        key_num = 0
    resize_window()  
    
# Functions to set specific resolutions
def set_res_320():
    set_res((320, 240))

def set_res_640():
    set_res((640, 480))

def set_res_800():
    set_res((800, 600))

# Function to exit the application
def exit_app():
    global thread_running
    thread_running = False

    camera_thread.join()
    cam.release()

    frame_queue.queue.clear()
    frame_queue.put(None)

    root.quit()
    root.destroy()
    print("App Exited")

# --- Main --- #

# Find Number of Cameras
list_cams()
camera_num = len(available_cam)

# Start Camera Thread
camera_thread = threading.Thread(target=camera_thread)
camera_thread.start()

# Create Tkinter application
root = Tk()
root.title("Webcam")
root.geometry(f"{cur_res[0]}x{cur_res[1]}")
root.bind('<Escape>', lambda e: exit_app()) 

# Rotate Button
button1 = Button(root, text="Rotate", command=rotate_cam)
button1.pack()
button1.config(font=("Helvetica", 16))

# Exit Button
exit_button = Button(root, text="Exit App", command=exit_app)
exit_button.pack()
exit_button.config(font=("Helvetica", 16))

# Label
label_widget = Label(root)
label_widget.pack(fill=BOTH, expand=YES)

# Menu
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

# Start app
gui_update() 
root.mainloop()