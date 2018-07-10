#!/usr/bin/python3

# Copyright 2018 Julian van Doorn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

from serial import *

from subprocess import call
from sys import platform

import os.path as path
import sys

import time

VERSION = "0.0.1"

BANNER = """
Python CLI Interface for Balancing Bot v%s
""" % VERSION

class Controller(CementBaseController):
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

    class Meta:
        label = "base"
        description = "Python CLI Interface for Balancing Bot"
        arguments = [
            (["--port"], dict(help="Set the port for serial connection")),
            #(["--conf"], dict(help="Allow for reading .conf files for bulk operations. Usage: cli encode --conf videos.conf \n cli face-recognition-test --conf faces.conf")),
            (['args'], dict(action='store', nargs='*'))
        ]

    @expose(hide=True)
    def default(self):
        print("No command specified")

    @expose()
    def set_degrees_incremental(self):
        if len(self.app.pargs.args) != 1:
            print("Incorrect argument count")
            exit(1)
        
        motor = int(self.app.pargs.args[0])

        self.initSerial()
        self.serial.setDTR(True)

        #time.sleep(1)

        for i in range(150, 70, -1):
            time.sleep(0.1)
            self.setAngle(motor, i)


    @expose()
    def set_degrees(self):
        if len(self.app.pargs.args) != 2:
            print("Incorrect argument count")
            exit(1)

        self.initSerial()

        motor = int(self.app.pargs.args[0])
        angle = int(self.app.pargs.args[1])

        self.setAngle(motor, angle)

class App(CementApp):
    class Meta:
        label = "R2D2-Encoder-CLI-Tool"
        base_controller = Controller


with App() as app:
    app.run()