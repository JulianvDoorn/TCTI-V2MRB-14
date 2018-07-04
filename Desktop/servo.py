from serial import *

from subprocess import call
from sys import platform

## Servo class to control multiple servos using the same serial connection
# @details
# Contains all functionality for opening a serial connection and sending
# commands to the motor controller. Allows for shared serial connections
# among instances. So one Servo instance represents only one servo and it
# does not represent a motor controller hosting multiple servos of any kind
class Servo:
    ## Default serial connection opened by the Serial.__init__ when no serial connection was provided
    defaultSerial = None

    ## Opens a serial connection using the provided port
    # @details
    # This method should be used for opening a serial connection
    # for multiple servo instances to use.
    # @param port Port to use; tty-like for Unix, COM* for Windows
    @staticmethod
    def openSerial(port=None):
        if port is None:
            if platform == "linux" or platform == "linux2":
                port = "/dev/ttyACM0"
            elif platform == "darwin":
                port = "/dev/ttyACM0" # Untested
            elif platform == "win32":
                port = "COM3" # Untested

        serial = Serial(
            port=port,
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
            call(["stty", "-F", port, "-hupcl"])
        elif platform == "darwin":
            pass
            # OS X
            # Undefined behavior for this OS; port may stay open, port may close, should stay open
        elif platform == "win32":
            pass
            # Windows...
            # Undefined behavior for this OS; port may stay open, port may close, should stay open

        return serial

    ## Servo constructor
    # @param motorId Id of the servo motor to control via serial connection
    # @param serial Optional, serial connection to send bytes over, when none provided, a default is used
    def __init__(self, motorId, serial=None):
        self.motorId = motorId

        if serial is None:
            if Servo.defaultSerial:
                Servo.defaultSerial = Servo.openSerial()
            
            self.serial = Servo.defaultSerial
        else:
            self.serial = serial

    ## Sets the angle of the servo with motorId
    # @details
    # Uses the provided serial connection and motorId to communicate with the 
    # servo controlling hardware. The controlling hardware has built-in bounds
    # check so that check is not executed by this function.
    # @param angle Angle to set the servo to
    def setAngle(self, angle):
        data = [0xAA, 0x01, 0x00, 0x00]

        if self.motorId == 1:
            data[2] = 0x0A
        elif self.motorId == 2:
            data[2] = 0x0B
        elif self.motorId == 3:
            data[2] = 0x0C

        data[3] = angle

        self.serial.write(data)