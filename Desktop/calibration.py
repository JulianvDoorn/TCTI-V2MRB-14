import cv2
import numpy as np
from vector import Vector
from pylab import array, plot, show, axis, arange, figure, uint8 
import util

class CalibrationData:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return str(self.red) + " " + str(self.green) + " " + str(self.blue)

class Calibration:
    def __init__(self, videoCapture):
        self.videoCapture = videoCapture
        self.redMotor = None
        self.greenMotor = None
        self.blueMotor = None
        self.center = None

    def getServoPoints(self, thresholdedFrame):
        thresholdedFrameHSV = cv2.cvtColor(thresholdedFrame, cv2.COLOR_BGR2HSV)

        redMask = cv2.inRange(thresholdedFrameHSV, np.array([-20, 125, 0]), np.array([20, 255, 255]))
        greenMask = cv2.inRange(thresholdedFrameHSV, np.array([50, 0, 0]), np.array([75, 255, 255]))
        blueMask = cv2.inRange(thresholdedFrameHSV, np.array([100, 0, 0]), np.array([200, 255, 255]))

        blueCx = 0
        blueCy = 0
        greenCx = 0
        greenCy = 0
        redCx = 0
        redCy = 0

        M = cv2.moments(redMask)
        if M['m00'] > 0:
            redCx = int(M['m10']/M['m00'])
            redCy = int(M['m01']/M['m00'])

        M = cv2.moments(greenMask)
        if M['m00'] > 0:
            greenCx = int(M['m10']/M['m00'])
            greenCy = int(M['m01']/M['m00'])

        M = cv2.moments(blueMask)
        if M['m00'] > 0:
            blueCx = int(M['m10']/M['m00'])
            blueCy = int(M['m01']/M['m00'])
        
        return Vector(redCx, redCy), Vector(greenCx, greenCy), Vector(blueCx, blueCy)

    def calibrateCamera(self):
        red = None
        green = None
        blue = None
        vals = []

        for i in range(100):
            valid, data = self.getCalibrationFrameData()

            if valid:
                vals.append(data)

        red = vals[0].red
        green = vals[0].green
        blue = vals[0].blue

        for v in vals:
            red += v.red
            green += v.green
            blue += v.blue

        red = Vector(int(red.values[0] / len(vals)), int(red.values[1] / len(vals)))
        green = Vector(int(green.values[0] / len(vals)), int(green.values[1] / len(vals)))
        blue = Vector(int(blue.values[0] / len(vals)), int(blue.values[1] / len(vals)))

        self.redMotor = red
        self.greenMotor = green
        self.blueMotor = blue
        self.center = self.redMotor + self.greenMotor + self.blueMotor
        self.center = Vector(int(self.center.values[0] / 3), int(self.center.values[1] / 3))
        
    def getCalibrationFrameData(self):
        ret, frame = self.videoCapture.read()

        thresholdedFrame = util.preprocessImage(frame)
        ret, thresholdedFrame =  cv2.threshold(thresholdedFrame,64,255,cv2.THRESH_BINARY)

        red, green, blue = self.getServoPoints(thresholdedFrame)

        thresholdedFrameGray = cv2.cvtColor(thresholdedFrame, cv2.COLOR_RGB2GRAY)
        ret, thresholdedFrameGray = cv2.threshold(thresholdedFrameGray,200,255,cv2.THRESH_BINARY)

        kernel = np.ones((5,5),np.uint8)
        dilation = cv2.dilate(thresholdedFrameGray,kernel,iterations = 1)
        erosion = cv2.erode(thresholdedFrameGray,kernel,iterations = 1)

        circles = cv2.HoughCircles(thresholdedFrameGray, cv2.HOUGH_GRADIENT,4,50,
                                    param1=50,param2=30,minRadius=0,maxRadius=30)

        if len(circles[0]) == 3:
            red = Calibration.bindHoughCirclesToColorEstimation(circles, red)
            green = Calibration.bindHoughCirclesToColorEstimation(circles, green)
            blue = Calibration.bindHoughCirclesToColorEstimation(circles, blue)

        calibration = CalibrationData(red, green, blue)

        return len(circles[0]) == 3, calibration

    @staticmethod
    def bindHoughCirclesToColorEstimation(houghCircles, estimatedColorPosition):
        closestHoughCircle = None

        if houghCircles is not None:
            houghCircles = np.uint16(np.around(houghCircles))

            for circle in houghCircles[0,:]:
                coords = Vector(circle[0], circle[1])
                rad = circle[2]

                if closestHoughCircle is None:
                    closestHoughCircle = (coords, rad)
                else:
                    if (estimatedColorPosition - coords).norm() < (estimatedColorPosition - closestHoughCircle[0]).norm():
                        closestHoughCircle = (coords, rad)

        if closestHoughCircle is not None:
            return closestHoughCircle[0]
        else:
            return estimatedColorPosition