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
    def __init__(self, videoCapture, x, y, w, h):
        self.videoCapture = videoCapture
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    ## Calls VideoCapture.read() and crops the returned frame
    # @details
    # Calls VideoCapture.read and crops the returned frame. Both the
    # frame and the returned return status is returned to the caller
    # of this method.
    def read(self):
        ret, frame = self.videoCapture.read()
        frame = frame[self.y:self.y+self.h, self.x:self.x+self.w]
        return ret, frame