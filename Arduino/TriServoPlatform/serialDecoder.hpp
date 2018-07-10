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

#ifndef SERIAL_DECODER_HPP
#define SERIAL_DECODER_HPP

#include <Arduino.h>

#include "triServoPlatform.hpp"

/**
 * @brief Takes serial commands and turns them into actions
 * 
 * @details
 * Takes serial commands and turns them into actions. This is done by
 * constantly polling the provided stream by the constructor. The polling is
 * done by calling loop() frequently enough to read the stream's queue.
 * It decodes a servo id and angle and sends them to the TriServoPlatform
 * also provided by the constructor. The default constructor puts the stream
 * and triServoPlatform pointer to null.
 */
class SerialDecoder {
	Stream* stream;
	TriServoPlatform* triServoPlatform;

public:
	/**
	 * @brief Construct a nulled SerialDecoder
	 * 
	 * @details
	 * Constructs a SerialDecoder with all pointers set to nullptr
	 */
	SerialDecoder();

	/**
	 * @brief Construct a SerialDecoder with a Stream and TriServoPlatform
	 * 
	 * @param s Stream to decode serial data from
	 * @param triServoPlatform Actuator platform to decode data for
	 */
	SerialDecoder(Stream& s, TriServoPlatform& triServoPlatform);

	/**
	 * @brief Dequeues data from the stream, aught to be called in void loop()
	 * 
	 * @details
	 * Waits for start byte 0xAA and then for two data bytes. The first byte
	 * containing the selected servo on the TriServoPlatform and the second
	 * byte containing the desired angle to turn the selected servo towards.
	 */
	void loop();

	/**
	 * @brief Assignment operator for SerialDecoder
	 * 
	 * @param other SerialDecoder to copy the new references from
	 * @return SerialDecoder& SerialDecoder reference to 'this'
	 */
	SerialDecoder& operator= (const SerialDecoder& other);
};

#endif // SERIAL_DECODER_HPP