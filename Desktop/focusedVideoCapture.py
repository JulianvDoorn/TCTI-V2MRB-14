import cv2
import util
import numpy as np
from vector import Vector

## OpenCV's VideoCapture class-like with a cropped view
# @details
# Implements a read method which calls the read method of
# the provided OpenCV VideoCapture instance with post-processing
class FocusedVideoCapture:
    ## Constructs a FocusedVideoCapture instance
    # @details
    # Takes all the provided arguments and stores them
    # @param videoCapture OpenCV VideoCapture instance to use as image source
    # @param x X position to crop the frame at
    # @param x Y position to crop the frame at
    # @param w Width of the cropped frame
    # @param h Height of the cropped frame
    def __init__(self, videoCapture, x=None, y=None, w=None, h=None):
        self.videoCapture = videoCapture
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def calibrateFocus(self):
        frameSizeFound = False
        while not frameSizeFound:
            ret, frame = self.videoCapture.read()

            thresholdedFrame = util.preprocessImage(frame)
            ret, thresholdedFrame =  cv2.threshold(thresholdedFrame,100,255,cv2.THRESH_BINARY)

            thresholdedFrameHSV = cv2.cvtColor(thresholdedFrame, cv2.COLOR_BGR2HSV)

            greenMask = cv2.inRange(thresholdedFrameHSV, np.array([25, 0, 0]), np.array([50, 255, 255]))

            greenMask = cv2.GaussianBlur(greenMask, (5,5), 10)

            kernel = np.ones((5,5),np.uint8)
            erosion = cv2.erode(greenMask, kernel, iterations = 3)
            dilation = cv2.dilate(erosion, kernel, iterations = 3)

            ret, thresholdedFrame = cv2.threshold(dilation, 100, 255, cv2.THRESH_BINARY_INV)

            detector = cv2.SimpleBlobDetector_create()
            keypoints = detector.detect(thresholdedFrame)
            if len(keypoints) == 2:
                point0 = Vector(int(keypoints[0].pt[0]), int(keypoints[0].pt[1]))
                point1 = Vector(int(keypoints[1].pt[0]), int(keypoints[1].pt[1]))
                if point0.values[0] > point1.values[0]:
                    frameSize = point0 - point1
                    self.x = point1.values[0]
                    self.y = point1.values[1]
                else:
                    frameSize = point1 - point0
                    self.x = point0.values[0]
                    self.y = point0.values[1]
                self.w = frameSize.values[0]
                self.h = frameSize.values[1]

                cv2.line(thresholdedFrame, point0.values, point1.values, (0,0,255),1, cv2.LINE_AA)
                cv2.putText(thresholdedFrame, str(frameSize), (point0 + Vector(30, 0)).values, cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0))

                frameSizeFound = True
            
            for k in keypoints:
                sticker = Vector(int(k.pt[0]), int(k.pt[1]))
                cv2.circle(thresholdedFrame, sticker.values, 100, (0,0,255), 2)
            
            cv2.imshow("Focus calibration", thresholdedFrame)
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    ## Calls VideoCapture.read() and crops the returned frame
    # @details
    # Calls VideoCapture.read and crops the returned frame. Both the
    # frame and the returned return status is returned to the caller
    # of this method.
    def read(self):
        ret, frame = self.videoCapture.read()
        frame = frame[self.y:self.y+self.h, self.x:self.x+self.w]
        return ret, frame