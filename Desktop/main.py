#!/usr/bin/python3

import cv2
from vision import Vision
from servo import Servo
from focusedVideoCapture import FocusedVideoCapture
from vector import Vector
from pid import PID
import time

def mouseCallback(event, x, y, flags, param):
    global vision

    if event == cv2.EVENT_LBUTTONDOWN:
        vision.setSetPoint(Vector(x, y))

if __name__ == "__main__":
    cv2.namedWindow("App", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("App", mouseCallback)

    servo1 = Servo(1, None) # green
    servo2 = Servo(2, None, 7) # blue
    servo3 = Servo(3, None, 4) # red

    servo1.setAngle(20)
    servo2.setAngle(20)
    servo3.setAngle(20)

    cap = cv2.VideoCapture(1)
    focusedVideoCapture = FocusedVideoCapture(cap)
    focusedVideoCapture.calibrateFocus()

    vision = Vision(focusedVideoCapture)

    vision.calibrateCamera()

    pid = PID(servo1, servo2, servo3, 45, 10)

    while True:
        vision.getBallPoint()
        vision.calculateError()
        vision.showMotorImage(vision.lastCapture)

        redError, greenError, blueError = vision.getErrors()

        pid.update(redError, greenError, blueError)

        # time.sleep(0.01)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()