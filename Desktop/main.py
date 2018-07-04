#!/usr/bin/python3

import cv2
from vision import Vision
from focusedVideoCapture import FocusedVideoCapture
from vector import Vector

def mouseCallback(event, x, y, flags, param):
    global vision

    if event == cv2.EVENT_LBUTTONDOWN:
        vision.setSetPoint(Vector(x, y))

if __name__ == "__main__":
    cv2.namedWindow("App", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("App", mouseCallback)

    x = 118
    y = 30
    h = 400
    w = 400

    cap = cv2.VideoCapture(1)
    vision = Vision(FocusedVideoCapture(cap, x, y, h, w))

    vision.calibrateCamera()

    while True:
        vision.getBallPoint()
        vision.calculateError()
        vision.showMotorImage(vision.lastCapture)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()