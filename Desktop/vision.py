import cv2
import numpy as np
import util
from calibration import Calibration
from pylab import array, plot, show, axis, arange, figure, uint8 
from vector import Vector

## Vision class with routines for initiating a calibration and detecting a ball
# @details
# Vision class with routines for initiating
# a calibration and detecting a ball. This
# class also projects the ballPoint and setPoint onto the
# axises of the motors in order to calculate an error.
# This error can be used by PID systems to approriately
# handle ball movements.
class Vision:
    ## Vision constructor
    # @details
    # Initiates all member attriutes and
    # adds a reference to the provided
    # videoCapture class.
    # @param videoCapture OpenCV VideoCapture to read frames from
    def __init__(self, videoCapture):
        self.videoCapture = videoCapture
        self.redError = 0
        self.greenError = 0
        self.blueError = 0
        self.calibration = None
        self.lastCapture = None
        self.setPoint = Vector(0, 0)
        self.ballPoint = None

    ## Sets the setPoint to calculate errors for
    # @param v Vector to set as setpoint
    def setSetPoint(self, v):
        self.setPoint = v

    ## Initiate the calibration routine
    def calibrateCamera(self):
        self.calibration = Calibration(self.videoCapture)
        self.calibration.calibrateCamera()
        self.setPoint = self.calibration.center

    ## Writes the errors to the provided frame at the calibrated motor positions
    def putErrorText(self, frame):
        cv2.putText(frame, str(int(self.blueError)), (self.calibration.blueMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
        cv2.putText(frame, str(int(self.redError)), (self.calibration.redMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
        cv2.putText(frame, str(int(self.greenError)), (self.calibration.greenMotor + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 

    ## Calculates the ballPoint from a frame provided by videoCapture
    def getBallPoint(self):
        ret, self.lastCapture = self.videoCapture.read()

        thresholdedFrame = util.preprocessImage(self.lastCapture)
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

    ## Takes information from the ballPoint and setPoint and calculates an error
    def calculateError(self):
        self.getBallPoint()

        self.redSetPointDotProduct = util.dotProductLinePoint(self.calibration.redMotor, self.calibration.center, self.setPoint)
        self.greenSetPointDotProduct = util.dotProductLinePoint(self.calibration.greenMotor, self.calibration.center, self.setPoint)
        self.blueSetPointDotProduct = util.dotProductLinePoint(self.calibration.blueMotor, self.calibration.center, self.setPoint)

        if self.ballPoint is not None:
            self.redBallDotProduct = util.dotProductLinePoint(self.calibration.redMotor, self.calibration.center, self.ballPoint)
            self.greenBallDotProduct = util.dotProductLinePoint(self.calibration.greenMotor, self.calibration.center, self.ballPoint)
            self.blueBallDotProduct = util.dotProductLinePoint(self.calibration.blueMotor, self.calibration.center, self.ballPoint)

            self.redError = self.redSetPointDotProduct - self.redBallDotProduct
            self.greenError = self.greenSetPointDotProduct - self.greenBallDotProduct
            self.blueError = self.blueSetPointDotProduct - self.blueBallDotProduct

    ## Renders information about the scene on top of referenceFrame
    # @details
    # Renders infromation about the scene on top of the referenceFrame.
    # if the referenceFrame is None, a white image is used.
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

            cv2.line(frame, self.ballPoint.values, util.applyDotProductToLine(self.calibration.blueMotor, self.calibration.center, self.blueBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)
            cv2.line(frame, self.ballPoint.values, util.applyDotProductToLine(self.calibration.redMotor, self.calibration.center, self.redBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)
            cv2.line(frame, self.ballPoint.values, util.applyDotProductToLine(self.calibration.greenMotor, self.calibration.center, self.greenBallDotProduct).values, (255,0,255), 1, cv2.LINE_AA)

        cv2.line(frame, self.setPoint.values, util.applyDotProductToLine(self.calibration.blueMotor, self.calibration.center, self.blueSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)
        cv2.line(frame, self.setPoint.values, util.applyDotProductToLine(self.calibration.redMotor, self.calibration.center, self.redSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)
        cv2.line(frame, self.setPoint.values, util.applyDotProductToLine(self.calibration.greenMotor, self.calibration.center, self.greenSetPointDotProduct).values, (0, 128, 255), 1, cv2.LINE_AA)

        cv2.imshow("App", frame)

    ## Displays debug information
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

    ## Returns redError, greenError and blueError in a tuple
    # @return (redError, greenError, blueError)
    def getErrors(self):
        return self.redError, self.greenError, self.blueError
    