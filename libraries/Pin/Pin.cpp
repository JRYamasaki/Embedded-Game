#include "Pin.h"

Pin::Pin(uint8_t pinNum, String msg)
{
	pinNumber = pinNum;
    message = msg;
}

uint8_t Pin::getPinNumber()
{
	return pinNumber;
}

String Pin::getMessage()
{
	return message;
}
