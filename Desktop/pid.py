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

import time

class PID:
    def __init__(self, servo1, servo2, servo3, maxAngle, minAngle):
        self.servo1 = servo1
        self.servo2 = servo2
        self.servo3 = servo3
        self.maxAngle = maxAngle
        self.minAngle = minAngle
        self.lastTime = time.time()
        self.servo1.lastError = 0
        self.servo1.ITerm = 0
        self.servo2.lastError = 0
        self.servo2.ITerm = 0
        self.servo3.lastError = 0
        self.servo3.ITerm = 0
    
    def applyPID(self, servo, error):
        nullAngle = 20

        Kp=8.0
        Ki=3.0
        Kd=14.0
        windupGuard = 8

        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - servo.lastError

        PTerm = Kp * error
        servo.ITerm += error * deltaTime

        if (servo.ITerm < -windupGuard):
            servo.ITerm = -windupGuard
        elif (servo.ITerm > windupGuard):
            servo.ITerm = windupGuard

        DTerm = 0.0
        if deltaTime > 0:
            DTerm = deltaError / deltaTime

        servo.lastError = error

        newAngle = nullAngle - (PTerm + (Ki * servo.ITerm) + (Kd * DTerm))

        servo.setAngle(max(10, min(45, int(newAngle))))

    def update(self, redError, greenError, blueError):
        # servo1 green
        # servo2 blue
        # servo3 red

        

        self.applyPID(self.servo1, greenError / 100)
        self.applyPID(self.servo2, blueError / 100)
        self.applyPID(self.servo3, redError / 100)

        self.lastTime = self.currentTime