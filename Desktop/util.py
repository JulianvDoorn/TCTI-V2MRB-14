
from pylab import array, plot, show, axis, arange, figure, uint8 
from vector import Vector

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

def dotProductLinePoint(lineStart, lineEnd, point):
    return (point - lineStart).inner((lineEnd - lineStart).normalize())

def applyDotProductToLine(lineStart, lineEnd, dp):
    unitVector = (lineEnd - lineStart).normalize()
    v = Vector(unitVector[0] * dp, unitVector[1] * dp) + lineStart
    return Vector(int(v[0]), int(v[1]))