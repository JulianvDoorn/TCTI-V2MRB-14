// Copyright 2018 Julian van Doorn
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
// to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: 
// 
// The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

#include <Arduino.h>
#include <Servo.h>

#include "triServoPlatform.hpp"
#include "serialDecoder.hpp"

const uint8_t servoLowerBound = 10;
const uint8_t servoUpperBound = 45;
const uint8_t servoNullPosition = 20;

SerialDecoder serialDecoder;
Servo servo0;
Servo servo1;
Servo servo2;
TriServoPlatform triServoPlatform(servo0, servo1, servo2);

void setup() {
	Serial.begin(115200);
	serialDecoder = SerialDecoder(Serial, triServoPlatform);

	servo0.attach(9, servoLowerBound, servoUpperBound);
	servo1.attach(10, servoLowerBound, servoUpperBound);
	servo2.attach(11, servoLowerBound, servoUpperBound);

	delay(200);

	triServoPlatform.setAngle<0>(servoNullPosition);
	triServoPlatform.setAngle<1>(servoNullPosition);
	triServoPlatform.setAngle<2>(servoNullPosition);
}

void loop() {
	serialDecoder.loop();
}
