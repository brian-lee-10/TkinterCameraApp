import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FPS, 30)
key_num = 0


while True:
	if not cam.isOpened():
		print("Error opening camera")
		break
	
	# read frame
	ret, frame = cam.read()

	#frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
	frame = np.rot90(frame, key_num)
	
	cv2.imshow('Video', frame)
	
	if cv2.waitKey(1) == ord('r'):
		key_num=key_num+1
		if key_num >= 4:
			key_num = 0

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
