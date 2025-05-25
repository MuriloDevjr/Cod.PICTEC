# import the necessary packages
import numpy as np
import cv2
import time
# initialize our canvas as a 300x300 pixel image with 3 channels
# (Red, Green, and Blue) with a black background
canvas = np.zeros((300, 300, 3), dtype="uint8")
# draw a green line from the top-left corner of our canvas to the
# bottom-right
green = (0, 255, 0)
cv2.circle(canvas, (600, 600), 200, green, thickness= 100, lineType= 8, shift= 2)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

# draw a 3 pixel thick red line from the top-right corner to the
# bottom-left
red = (0, 0, 255)
cv2.line(canvas, (300, 0), (0, 300), red, 3)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)

blue = (255, 0, 0)
cv2.line(canvas, (150, 150), (0, 0), blue, 3)
cv2.imshow("Canvas", canvas)
cv2.waitKey(0)