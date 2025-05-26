import numpy as np
import imutils
import cv2
from cv2 import imread

camera = cv2.VideoCapture(0)
green = (0, 255, 0)


#1200, 900

while True: 
    _, frame = camera.read()
    frame = imutils.resize(frame, width=600, height=600)
    cv2.circle(frame, (449, 449), 10, green, thickness= 10, lineType= 8, shift= 2)
    #color = print(frame[449, 449])
    #cv2.putText(frame, color, (int(300), int(300)),
    #            cv2.FONT_HERSHEY_SIMPLEX, 0.6, green, 2)
    print(frame[300, 300])

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
