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