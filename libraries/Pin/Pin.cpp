#include "Pin.h"

Pin::Pin(uint8_t pinNum, bool sendMsg, String msg)
{
	pinNumber = pinNum;
    messageIndicator = sendMsg;
    message = msg;
}

uint8_t Pin::getPinNumber()
{
	return pinNumber;
}
    
bool Pin::needsToSendMessage()
{
	return messageIndicator;
}

String Pin::getMessage()
{
	return message;
}

void Pin::setMessageIndicator(bool messageMustBeSent)
{
	messageIndicator = messageMustBeSent;
}
