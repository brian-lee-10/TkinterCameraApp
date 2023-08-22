# TkinterCameraApp

This repository contains three Python scripts that use OpenCV to adjust camera frames.

## Required Libraries
* OpenCV
* Numpy
* Tkinter
* PIL

mirror.py: only needs OpenCV
rotate.py: only needs OpenCV and Numpy


**mirror.py**:
This script opens the default webcam and displays the video feed in an OpenCV window. It allows mirroring the frame horizontally on keypress 'm'.

**rotate.py**: 
This script opens the default webcam and displays the video feed in an OpenCV window. It allows rotating the frame 90 degrees clockwise on keypress 'r'. Rotations are done incrementally.

**rotateGUI.py**: 
This script creates a camera app GUI using Tkinter where the user can interact with buttons to rotate the frame. The frame is displayed in a Tkinter label. 
