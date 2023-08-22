import cv2

cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_FPS, 30)
mirror = False

while True:
	if not cam.isOpened():
		print("Error opening camera")
		break
	
	# read frame
	ret, frame = cam.read()

	if mirror:
		frame = cv2.flip(frame, 1)
	
	cv2.imshow('Video', frame)

	if cv2.waitKey(1) == ord('m'):
		mirror = not mirror

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()
