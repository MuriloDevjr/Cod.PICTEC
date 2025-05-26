import numpy as np
import cv2

canvas = np.zeros((600, 600, 3), dtype="uint8")

green = (0, 255, 0)
cv2.circle(canvas, (150, 150), 100, green,thickness=200)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

red = (0, 0, 255)
cv2.circle(canvas, (150, 150),  100, red, -1)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

blue = (255, 0, 0)
cv2.circle(canvas, (150, 150), 100, blue,-1)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)