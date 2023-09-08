# Webcam Application

This is a simple webcam application built with Tkinter and OpenCV in Python.

## Requirements
* Python 3
* OpenCV
* Tkinter
* PIL

## Usage
* Run "python cameraApp.py" to start the application on the command line
* Click the "Rotate" button to rotate the video feed by 90 degrees
* Use the "Resolution" menu to select from preset resolutions
* Switch to different webcams using the "Cameras" menu
* Press Esc or the "Exit App" button to exit the application

## Webcam Setup

The application will automatically detect available webcams on your system. Make sure you have at least one webacam connected and working before running the app. 

## Customization

* Adjust the cur_res variable to set a default resolution
* Add or remove resolutions in the file_menu options
* Modify the cv2.VideoCapture() settings for custom parameters
* Adjust the queue size to control video buffering