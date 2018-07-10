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

#ifndef TRI_SERVO_PLATFORM_HPP
#define TRI_SERVO_PLATFORM_HPP

#include <Servo.h>

class TriServoPlatform {
	Servo& servo0;
	Servo& servo1;
	Servo& servo2;

public:
	TriServoPlatform(Servo& s0, Servo& s1, Servo& s2);

	template<uint32_t SERVO_ID>
	void setAngle(const uint8_t angle) {
		if (SERVO_ID == 0) {
			servo0.write(angle);
		} else if (SERVO_ID == 1) {
			servo1.write(angle);
		} else if (SERVO_ID == 2) {
			servo2.write(angle);
		}
	}

	TriServoPlatform& operator= (const TriServoPlatform& other);
};

#endif // TRI_SERVO_PLATFORM_HPP