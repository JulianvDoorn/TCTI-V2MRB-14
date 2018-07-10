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

#include "serialDecoder.hpp"

SerialDecoder::SerialDecoder() : stream(nullptr), triServoPlatform(nullptr) { }

SerialDecoder::SerialDecoder(Stream& s, TriServoPlatform& triServoPlatform) : stream(&s), triServoPlatform(&triServoPlatform) { }

void SerialDecoder::loop() {
    if (stream->available() > 0) {
        uint8_t startByte = stream->read();
        
        if (startByte != 0xAA) {
            return;
        }

        while (stream->available() < 2);

        uint8_t selectedServo = stream->read();
        uint8_t angle = stream->read();

        if (selectedServo == 0x0A) {
            triServoPlatform->setAngle<0>(angle);
        } else if (selectedServo == 0x0B) {
            triServoPlatform->setAngle<1>(angle);
        } else if (selectedServo == 0x0C) {
            triServoPlatform->setAngle<2>(angle);
        }
    }
}

SerialDecoder& SerialDecoder::operator= (const SerialDecoder& other) {
    stream = other.stream;
    triServoPlatform = other.triServoPlatform;

    return *this;
}