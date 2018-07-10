#!/usr/bin/python3

# Copyright 2018 Julian van Doorn and Kiet van Osnabrugge
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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