
from pylab import array, plot, show, axis, arange, figure, uint8 
from vector import Vector

## Increases constrasts in the given image
# @details
# Uses a couple of techniques to increase the constrast.
# First it increases the intensity in a way that bright
# pixels become slightly brighter and dark pixels much
# brighter. Then int decreases the intensity in a way
# that dark pixes become slightly darker and bright
# pixels become much darker. Then the generated image
# is returned. This image is ought to be high contrast.
# @params image Image to increase the constast of
# @return HighConstrast image
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

## Calculates a dot product of a line and a point
# @details
# The dot product usually is done on two vectors
# with the same origin. But this dot product
# also provides an option to displace the origin
# from (0, 0) to somewhere else. This allows for
# much easier calculations of projections in 2d
# space. Using this function you can project point1
# onto the line going through origin and point0.
# @param origin Origin of point0 and point1
# @param point0 Point0 of the dot product
# @param point1 Point1 of the dot product
def dotProductLinePoint(origin, point0, point1):
    return (point1 - origin).inner((point0 - origin).normalize())

## Projects a dot product directly onto a line
# @details
# This function is used after calculating the dot product.
# It projects the dot product onto a given line. This 
# function is often postceeded by dotProductLinePoint
# @param linePoint0 Point0 on the given line
# @param linePoint1 Point1 on the given line
# @param dp dot product to project on the line provided
def applyDotProductToLine(linePoint0, linePoint1, dp):
    unitVector = (linePoint1 - linePoint0).normalize()
    v = Vector(unitVector[0] * dp, unitVector[1] * dp) + linePoint0
    return Vector(int(v[0]), int(v[1]))