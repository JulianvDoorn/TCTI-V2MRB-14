#!/usr/bin/python3

import numpy as np
import math
import cv2
from pylab import array, plot, show, axis, arange, figure, uint8 
import time


setPoint = (0, 0)


cap = cv2.VideoCapture(1)
port = "/dev/ttyACM0"

def initSerial(self):
    if self.app.pargs.port != None:
        self.port = self.app.pargs.port

    self.serial = Serial(
        port=self.port,
        baudrate=115200,
        bytesize=EIGHTBITS,
        parity=PARITY_NONE,
        stopbits=STOPBITS_ONE,
        xonxoff=True,
        rtscts=True,
        dsrdtr=False
    )

    if platform == "linux" or platform == "linux2":
        # prevent port from closing every time serial connection is opened
        call(["stty", "-F", self.port, "-hupcl"])
    elif platform == "darwin":
        pass
        # OS X
    elif platform == "win32":
        pass
        # Windows...

def setAngle(self, motor, angle):
    data = [0xAA, 0x01, 0x00, 0x00]

    if motor == 1:
        data[2] = 0x0A
    elif motor == 2:
        data[2] = 0x0B
    elif motor == 3:
        data[2] = 0x0C

    data[3] = angle

    self.serial.write(data)

def updatePID(error):
    Kp=2.0
    Ki=0.0
    Kd=1.0
    Integrator_max = 5
    Integrator_min = 1

    P_value = Kp * error
    D_value = Kd * ( error - Kd)
    Derivator = error

    Integrator = Ki + error

    if Integrator > Integrator_max:
        Integrator = Integrator_max
    elif Integrator < Integrator_min:
        Integrator = Integrator_min

    I_value = Integrator * Ki

    PID = P_value + I_value + D_value

    return PID

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

def thresholdImage(image):
    import cv2 as cv
    import numpy as np
    ret,thresh1 = cv.threshold(image,64,255,cv.THRESH_BINARY)
    return thresh1

def multiplyVectorAndInt(l, r):
    return (l[0] * r, l[1] * r)

def divideVectorAndInt(l, r):
    if r == 0:
        return (math.inf, math.inf)
    return (l[0] / r, l[1] / r)

def addVectors(l, r):
    return (l[0] + r[0], l[1] + r[1])

def subtractVectors(l, r):
    return (l[0] - r[0], l[1] - r[1])

def multiplyVectors(l, r):
    return (l[0] * r[0], l[1] * r[1])

def divideVectors(l, r):
    return (l[0] / r[0], l[1] / r[1])

def magnitudeVector(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)

def unitVector(v):
    m = magnitudeVector(v)
    if m == 0:
        return (0,0)
    return divideVectorAndInt(v, m)

def floatToIntVector(v):
    return (int(v[0]), int(v[1]))

def dotProduct(lineStart, lineEnd, point):
    return np.dot(subtractVectors(point, lineStart), unitVector(subtractVectors(lineEnd, lineStart)))

def interpolatePoint(start, end, alpha):
    return addVectors(multiplyVectorAndInt(subtractVectors(end, start), alpha), start)

def applyDotProductToLine(lineStart, lineEnd, dp):
    return addVectors(floatToIntVector(multiplyVectorAndInt(unitVector(subtractVectors(lineEnd, lineStart)), dp)), lineStart)

def ProjectPointOnVector(lineStart, lineEnd, point):
    dp = dotProduct(lineStart, lineEnd, point)
    return applyDotProductToLine(lineStart, lineEnd, dp)

def getServoPoints(blueMask, greenMask, redMask):
    M = cv2.moments(blueMask)

    blueCx = 0
    blueCy = 0
    greenCx = 0
    greenCy = 0
    redCx = 0
    redCy = 0

    if M['m00'] > 0:
        blueCx = int(M['m10']/M['m00'])
        blueCy = int(M['m01']/M['m00'])

    M = cv2.moments(greenMask)
    if M['m00'] > 0:
        greenCx = int(M['m10']/M['m00'])
        greenCy = int(M['m01']/M['m00'])

    M = cv2.moments(redMask)
    if M['m00'] > 0:
        redCx = int(M['m10']/M['m00'])
        redCy = int(M['m01']/M['m00'])
    
    return (blueCx, blueCy), (greenCx, greenCy), (redCx, redCy)

def getBallPoint(blackMask):
    M = cv2.moments(blackMask)

    cx = 0
    cy = 0

    if M['m00'] > 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    return (cx, cy)

def mouseCallback(event, x, y, flags, param):
    global setPoint

    if event == cv2.EVENT_LBUTTONDOWN:
        setPoint = (x, y)

while True:
    ret, frame = cap.read()

    x = 118
    y = 30
    h = 400
    w = 400

    frame = frame[y:y+h, x:x+w]

    thresholdedFrame = thresholdImage(preprocessImage(frame))
    thresholdedFrameHSV = cv2.cvtColor(thresholdedFrame, cv2.COLOR_BGR2HSV)

    thresholdedFrameGray = cv2.cvtColor(thresholdedFrame, cv2.COLOR_RGB2GRAY)
    ret, thresholdedFrameGray = cv2.threshold(thresholdedFrameGray,200,255,cv2.THRESH_BINARY)

    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(thresholdedFrameGray,kernel,iterations = 1)
    erosion = cv2.erode(thresholdedFrameGray,kernel,iterations = 1)

    circles = cv2.HoughCircles(thresholdedFrameGray, cv2.HOUGH_GRADIENT,3,30,
                                param1=50,param2=30,minRadius=0,maxRadius=30)


    if circles is not None:
        print("FOUNND")
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(thresholdedFrame,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(thresholdedFrame,(i[0],i[1]),2,(0,0,255),3)

    cv2.imshow("Hough", erosion)

    blueMask = cv2.inRange(thresholdedFrameHSV, np.array([100, 0, 0]), np.array([200, 255, 255]))
    greenMask = cv2.inRange(thresholdedFrameHSV, np.array([50, 0, 0]), np.array([75, 255, 255]))
    redMask = cv2.inRange(thresholdedFrameHSV, np.array([-20, 125, 0]), np.array([20, 255, 255]))
    blackMask = cv2.inRange(thresholdedFrameHSV, np.array([0, 0, 0]), np.array([255, 255, 50]))

    blue, green, red = getServoPoints(blueMask, greenMask, redMask)
    ballPoint = getBallPoint(blackMask)

    cv2.circle(thresholdedFrame, blue, 4, (0,0,0), -1)
    cv2.circle(thresholdedFrame, green, 4, (0,0,0), -1)
    cv2.circle(thresholdedFrame, red, 4, (0,0,0), -1)
    cv2.circle(thresholdedFrame, ballPoint, 4, (255,255,0), -1)

    middlePoint = (int((blue[0] + green[0] + red[0]) / 3), int((blue[1] + green[1] + red[1]) / 3))

    cv2.circle(thresholdedFrame, middlePoint, 4, (0,0,255), -1)

    cv2.line(thresholdedFrame, blue, middlePoint, (255,0,0), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, red, middlePoint, (0,0,255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, green, middlePoint, (0,255,0), 1, cv2.LINE_AA)

    cv2.line(thresholdedFrame, blue, middlePoint, (255,0,0), 1, cv2.LINE_AA)

    blueBallDotProduct = dotProduct(blue, middlePoint, ballPoint)
    redBallDotProduct = dotProduct(red, middlePoint, ballPoint)
    greenBallDotProduct = dotProduct(green, middlePoint, ballPoint)

    blueSetPointDotProduct = dotProduct(blue, middlePoint, setPoint)
    redSetPointDotProduct = dotProduct(red, middlePoint, setPoint)
    greenSetPointDotProduct = dotProduct(green, middlePoint, setPoint)

    cv2.line(thresholdedFrame, ballPoint, applyDotProductToLine(blue, middlePoint, blueBallDotProduct), (255,0,255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, ballPoint, applyDotProductToLine(red, middlePoint, redBallDotProduct), (255,0,255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, ballPoint, applyDotProductToLine(green, middlePoint, greenBallDotProduct), (255,0,255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, setPoint, applyDotProductToLine(blue, middlePoint, blueSetPointDotProduct), (0, 128, 255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, setPoint, applyDotProductToLine(red, middlePoint, redSetPointDotProduct), (0, 128, 255), 1, cv2.LINE_AA)
    cv2.line(thresholdedFrame, setPoint, applyDotProductToLine(green, middlePoint, greenSetPointDotProduct), (0, 128, 255), 1, cv2.LINE_AA)

    cv2.circle(thresholdedFrame, setPoint, 3, (0, 128, 255), -1)

    blueError = blueSetPointDotProduct - blueBallDotProduct
    redError = redSetPointDotProduct - redBallDotProduct
    greenError = greenSetPointDotProduct - greenBallDotProduct

    # print(updatePID(blueError))
    # print(updatePID(redError))
    # print(updatePID(greenError))

    cv2.putText(thresholdedFrame, str(int(blueError)), addVectors(blue, (30, 0)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
    cv2.putText(thresholdedFrame, str(int(redError)), addVectors(red, (30, 0)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 
    cv2.putText(thresholdedFrame, str(int(greenError)), addVectors(green, (30, 0)), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.5, (0, 0, 0)) 

    cv2.imshow("Source", frame)
    cv2.imshow("Points", thresholdedFrame)

    cv2.setMouseCallback('Points', mouseCallback)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()