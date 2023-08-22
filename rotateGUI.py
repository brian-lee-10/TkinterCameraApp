from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np

# Function to open camera
def open_camera():
    # Capture the video frame by frame
    global frame
    ret, frame = cam.read()

    frame = np.rot90(frame, key_num)
    
    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
  
    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)
  
    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)
  
    # Displaying photoimage in the label
    label_widget.photo_image = photo_image
  
    # Configure image in the label
    label_widget.configure(image=photo_image)
  
    # Repeat the same process after every 10 seconds
    label_widget.after(10, open_camera)

# Create a function to rotate camera view
def rotate():
    global key_num
    key_num = key_num+1
    if key_num >= 4:
        key_num = 0


cam = cv2.VideoCapture(0)

width, height = 1280, 720
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create a GUI app
tk = Tk()
tk.title("Webcam")

# quit app whenever "Escape" is pressed
tk.bind('<Escape>', lambda e: tk.quit())

# Create a button to rotate camera
button1 = Button(tk, text="Rotate Camera", command=rotate)
button1.pack()
button1.config(font=("Helvetica", 20))

# Create a label and display it on app
label_widget = Label(tk)
label_widget.pack(fill=BOTH, expand=YES) 

# Declare global variable
key_num = 0



# Open the Camera
open_camera()

# Create an infinite loop for displaying app on screen
tk.mainloop()
