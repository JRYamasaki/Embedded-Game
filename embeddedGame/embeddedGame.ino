#include <Pin.h>

const int btn1 = 2;
const int btn2 = 3;
const int btn3 = 4;
const int btn4 = 5;
const int ledPin = 13;

String serialInput = "";

Pin inputPins[] = {Pin{btn1, 0, "btn1\n"},
                   Pin{btn2, 0, "btn2\n"},
                   Pin{btn3, 0, "btn3\n"},
                   Pin{btn4, 0, "btn4\n"}};
                   
uint8_t numOfInputs = sizeof(inputPins) / sizeof(inputPins[0]);

int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;

void setup()
{
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  readInputPins();
  processInputs();
}

//Helper Functions

void readInputPins()
{
  for(int i = 0; i < numOfInputs; i++)
  {
    inputPins[i].setMessageIndicator(digitalRead(inputPins[i].getPinNumber()));
  }
}

void processInputs()
{
  for(int i = 0; i < numOfInputs; i++)
  {
    if(inputPins[i].needsToSendMessage())
    {
      Serial.print(inputPins[i].getMessage());
      delay(1000);
      Serial.flush();
    }
  }
}

void signalTo(int pin, int delayTime)
{
  digitalWrite(pin, HIGH);
  delay(delayTime);
  digitalWrite(pin, LOW);
}

