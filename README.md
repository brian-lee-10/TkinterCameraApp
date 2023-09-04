# TkinterCameraApp

This repository contains three Python scripts that use OpenCV to adjust camera frames.

## Required Libraries
* OpenCV
* Numpy
* Tkinter
* PIL
* Threading
* Queue

mirror.py: only needs OpenCV

rotate.py: only needs OpenCV and Numpy


### mirror.py

This script opens the default webcam and displays the video feed in an OpenCV window. It allows mirroring the frame horizontally on keypress 'm'.

### rotate.py 

This script opens the default webcam and displays the video feed in an OpenCV window. It allows rotating the frame 90 degrees clockwise on keypress 'r'. Rotations are done incrementally.

### rotateGUI.py

This program displays a live video feed from a webcam in a graphical user interface (GUI) and allow the user to interact with the video.

Specifically, it enables:

* Displaying the real-time webcam video feed in a Tkinter window
* Rotating the video feed by 90 degrees on demand via a button click
* Changing the resolution/size of the video frames via menu options