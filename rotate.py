import cv2
import numpy as np

# Initialize video capture
cam = cv2.VideoCapture(0)

# Set frame rate to 30
cam.set(cv2.CAP_PROP_FPS, 30)

# Declare necessary variables
key_num = 0

while True:
	# Check to see if the camera is open
	if not cam.isOpened():
		print("Error opening camera")
		break
	
	# read frame
	ret, frame = cam.read()


	# Rotate frame by key_num increments
	frame = np.rot90(frame, key_num)
	#frame = cv2.rotate(frame, key_num)
	
	# Display camera frame
	cv2.imshow('Video', frame)
	
	# Increment rotation angle on 'r' keypress
	if cv2.waitKey(1) == ord('r'):
		key_num=key_num+1
		print(key_num)
		if key_num >= 4:
			key_num = 0

	# Break loop on 'q' keypress
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release camera and destroy opened windows
cam.release()
cv2.destroyAllWindows()
