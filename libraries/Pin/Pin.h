#ifndef Pin_h
#define Pin_h

#include "Arduino.h"

class Pin
{
  public:
    Pin(uint8_t pinNum, bool sendMsg, String msg);
    uint8_t getPinNumber();
    bool needsToSendMessage();
    String getMessage();
    void setMessageIndicator(bool messageMustBeSent);
  private:
    uint8_t pinNumber;
    bool messageIndicator;
    String message;
};

#endif
