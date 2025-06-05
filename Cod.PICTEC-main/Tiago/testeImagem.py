# import the necessary packages
import numpy as np
import cv2
import time
from cv2 import cvtColor, COLOR_BGR2RGB
from cv2 import imread

img = imread('verde.png')

print(img[0, 0])

green = (0, 255, 0)
#cv2.circle(img, (0, 0), 10, green, thickness= 50, lineType= 8, shift= 2)
cv2.imshow("Canvas", img)
cv2.waitKey(0)