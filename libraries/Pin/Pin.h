#ifndef Pin_h
#define Pin_h

#include "Arduino.h"

class Pin
{
  public:
    Pin(uint8_t pinNum, String msg);
    uint8_t getPinNumber();
    String getMessage();
  private:
    uint8_t pinNumber;
    String message;
};

#endif
