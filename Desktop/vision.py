import cv2
import numpy as np
from pylab import array, plot, show, axis, arange, figure, uint8 

from vector import Vector

class Vision:
    @staticmethod
    def dotProductLinePoint(lineStart, lineEnd, point):
        return (point - lineStart).inner((lineEnd - lineStart).normalize())

    @staticmethod
    def applyDotProductToLine(lineStart, lineEnd, dp):
        unitVector = (lineEnd - lineStart).normalize()
        v = Vector(unitVector[0] * dp, unitVector[1] * dp) + lineStart
        return Vector(int(v[0]), int(v[1]))

    @staticmethod
    def preprocessImage(image):
        # Image data
        maxIntensity = 255.0 # depends on dtype of image data
        x = arange(maxIntensity) 

        # Parameters for manipulating image data
        phi = 1
        theta = 1

        # Increase intensity such that
        # dark pixels become much brighter, 
        # bright pixels become slightly bright
        newImage0 = (maxIntensity/phi)*(image/(maxIntensity/theta))**0.5
        newImage0 = array(newImage0,dtype=uint8)

        y = (maxIntensity/phi)*(x/(maxIntensity/theta))**0.5

        # Decrease intensity such that
        # dark pixels become much darker, 
        # bright pixels become slightly dark 
        newImage1 = (maxIntensity/phi)*(image/(maxIntensity/theta))**2
        newImage1 = array(newImage1,dtype=uint8)

        z = (maxIntensity/phi)*(x/(maxIntensity/theta))**2

        return newImage1

    def __init__(self, videoCapture):
        self.videoCapture = videoCapture
        self.redError = 0
        self.greenError = 0
        self.blueError = 0
        self.calibration = None
        self.lastCapture = None
        self.setPoint = Vector(0, 0)
        self.ballPoint = None

    def setSetPoint(self, v):
        self.setPoint = v

    def calibrateCamera(self):
        self.calibration = Calibration(self.videoCapture)
        self.calibration.calibrateCamera()

    def putErrorText(self, frame):
        cv2.putText(frame, str(int(self.blueError)), (self.calibration.blueMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
        cv2.putText(frame, str(int(self.redError)), (self.calibration.redMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
        cv2.putText(frame, str(int(self.greenError)), (self.calibration.greenMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 

    def getBallPoint(self):
        ret, self.lastCapture = self.videoCapture.read()

        thresholdedFrame = Vision.preprocessImage(self.lastCapture)
        thresholdedFrameGray = cv2.cvtColor(thresholdedFrame, cv2.COLOR_RGB2GRAY)
        ret, thresholdedFrameGray = cv2.threshold(thresholdedFrameGray, 20, 255, cv2.THRESH_BINARY)

        thresholdedFrameGray = cv2.GaussianBlur(thresholdedFrameGray, (5,5), 10)

        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(thresholdedFrameGray, kernel, iterations = 1)
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(dilation)

        cv2.imshow("Ball blob detection", thresholdedFrameGray)

        if len(keypoints) > 0:
            self.ballPoint = Vector(int(keypoints[0].pt[0]), int(keypoints[0].pt[1]))
            return True, self.ballPoint
        else:
            return False, None

    def calculateError(self):
        self.getBallPoint()

        self.redSetPointDotProduct = Vision.dotProductLinePoint(self.calibration.redMotor, self.calibration.center, self.setPoint)
        self.greenSetPointDotProduct = Vision.dotProductLinePoint(self.calibration.greenMotor, self.calibration.center, self.setPoint)
        self.blueSetPointDotProduct = Vision.dotProductLinePoint(self.calibration.blueMotor, self.calibration.center, self.setPoint)

        if self.ballPoint is not None:
            self.redBallDotProduct = Vision.dotProductLinePoint(self.calibration.redMotor, self.calibration.center, self.ballPoint)
            self.greenBallDotProduct = Vision.dotProductLinePoint(self.calibration.greenMotor, self.calibration.center, self.ballPoint)
            self.blueBallDotProduct = Vision.dotProductLinePoint(self.calibration.blueMotor, self.calibration.center, self.ballPoint)

            self.redError = self.redSetPointDotProduct - self.redBallDotProduct
            self.greenError = self.greenSetPointDotProduct - self.greenBallDotProduct
            self.blueError = self.blueSetPointDotProduct - self.blueBallDotProduct

    def showMotorImage(self, referenceFrame=None):
        frame = None

        if referenceFrame is None:
            frame = np.zeros((self.videoCapture.h, self.videoCapture.w, 3), np.uint8)
            frame[:] = (255,255,255)
        else:
            frame = referenceFrame

        self.putErrorText(frame)

        cv2.circle(frame, self.calibration.blueMotor.values, 4, (0,0,0), -1)
        cv2.circle(frame, self.calibration.greenMotor.values, 4, (0,0,0), -1)
        cv2.circle(frame, self.calibration.redMotor.values, 4, (0,0,0), -1)

        middlePoint = self.calibration.redMotor + self.calibration.greenMotor + self.calibration.blueMotor
        middlePoint = Vector(int(middlePoint.values[0] / 3), int(middlePoint.values[1] / 3))

        cv2.circle(frame, middlePoint.values, 4, (0,0,255), -1)

        cv2.line(frame, self.calibration.blueMotor.values, middlePoint.values, (255,0,0), 1, cv2.LINE_AA)
        cv2.line(frame, self.calibration.redMotor.values, middlePoint.values, (0,0,255), 1, cv2.LINE_AA)
        cv2.line(frame, self.calibration.greenMotor.values, middlePoint.values, (0,255,0), 1, cv2.LINE_AA)

        if self.ballPoint is not None:
            cv2.circle(frame, self.ballPoint.values, 10, (255,255,0), -1)

            cv2.line(frame, self.ballPoint.values, self.applyDotProductToLine(self.calibration.blueMotor, self.calibration.center, self.blueBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)
            cv2.line(frame, self.ballPoint.values, self.applyDotProductToLine(self.calibration.redMotor, self.calibration.center, self.redBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)
            cv2.line(frame, self.ballPoint.values, self.applyDotProductToLine(self.calibration.greenMotor, self.calibration.center, self.greenBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)

        cv2.line(frame, self.setPoint.values, self.applyDotProductToLine(self.calibration.blueMotor, self.calibration.center, self.blueSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)
        cv2.line(frame, self.setPoint.values, self.applyDotProductToLine(self.calibration.redMotor, self.calibration.center, self.redSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)
        cv2.line(frame, self.setPoint.values, self.applyDotProductToLine(self.calibration.greenMotor, self.calibration.center, self.greenSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)

        cv2.imshow("App", frame)

    def showDebugImages(self, src, thresholdedFrame, calibration, circles):
        cv2.circle(thresholdedFrame, calibration.blue.values, 4, (0,0,0), -1)
        cv2.circle(thresholdedFrame, calibration.green.values, 4, (0,0,0), -1)
        cv2.circle(thresholdedFrame, calibration.red.values, 4, (0,0,0), -1)

        middlePoint = calibration.red + calibration.green + calibration.blue
        middlePoint = Vector(int(middlePoint.values[0] / 3), int(middlePoint.values[1] / 3))

        cv2.circle(thresholdedFrame, middlePoint.values, 4, (0,0,255), -1)

        cv2.line(thresholdedFrame, calibration.blue.values, middlePoint.values, (255,0,0), 1, cv2.LINE_AA)
        cv2.line(thresholdedFrame, calibration.red.values, middlePoint.values, (0,0,255), 1, cv2.LINE_AA)
        cv2.line(thresholdedFrame, calibration.green.values, middlePoint.values, (0,255,0), 1, cv2.LINE_AA)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(thresholdedFrame,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.circle(thresholdedFrame,(i[0],i[1]),2,(0,0,0),3)

        cv2.imshow("Source", src)
        cv2.imshow("Thresholded", thresholdedFrame)

    