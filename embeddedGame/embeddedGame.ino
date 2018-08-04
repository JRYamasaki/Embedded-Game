#include <Pin.h>

// Constants
const uint8_t timeBeforeFlushInms = 125;

// Game 1 Constants
const uint8_t btn1 = 2;
const uint8_t btn2 = 3;
const uint8_t btn3 = 4;
const uint8_t btn4 = 5;
const uint8_t ledPin1 = 13;
const uint8_t ledPin2 = 12;
const uint8_t ledPin4 = 11;
const uint8_t ledPin8 = 10;

// Game 2 Constants
const uint8_t timingButton = 22;
const uint8_t timingLED = 9;
const uint8_t toggleMax = 8;

// Global Variables
Pin inputPins[] = {Pin{btn1, 0, "g1btn1\n"},
                   Pin{btn2, 0, "g1btn2\n"},
                   Pin{btn3, 0, "g1btn3\n"},
                   Pin{btn4, 0, "g1btn4\n"},
                   Pin{timingButton, 0, "g2\n"}};
const uint8_t numOfInputs = sizeof(inputPins) / sizeof(inputPins[0]);

String serialInput = "";
uint8_t toggleCounter = 0;
long nextTimeToToggle = 0;
unsigned long timeLEDIsOnOrOffInMillis = 0;
boolean timingLEDIsAllowedToToggle = false;
boolean timingLEDState = true;

void setup()
{
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin8, OUTPUT);
  pinMode(timingLED, OUTPUT);
  Serial.begin(115200);
}

void loop()
{
  if(Serial.available())
  {
    serialInput = Serial.readString();
    processGame1Data(serialInput);
    processToggleData(serialInput, timingLED);
  }
  checkForToggleEvent();
  readInputPins();
  processInputs();
}

//Helper Functions

void checkForToggleEvent()
{
  if(LEDShouldBeToggled())
  {
    toggleLED(timingLED);
  }
}

boolean LEDShouldBeToggled()
{
  return timingLEDIsAllowedToToggle && (millis() > nextTimeToToggle);
}

void processGame1Data(String data)
{
  if(data.substring(0,2).equals("g1"))
  {
    setNumbers(data.substring(2, data.length())); 
  }
}

void processToggleData(String data, int pin)
{
  if(data.substring(0,2).equals("g2"))
  {
    int commaPosition = data.indexOf(',');
    timeLEDIsOnOrOffInMillis = data.substring(commaPosition + 1, data.length()).toInt();
    toggleLED(pin);
    timingLEDIsAllowedToToggle = true;
  }
}

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
      delay(timeBeforeFlushInms);
      Serial.flush();
    }
  }
}

void setNumbers(String input)
{
  long randNumber = input.toInt();
  digitalWrite(ledPin1, (randNumber & 1) > 0);
  digitalWrite(ledPin2, (randNumber & 2) > 0);
  digitalWrite(ledPin4, (randNumber & 4) > 0);
  digitalWrite(ledPin8, (randNumber & 8) > 0);
}

void toggleLED(int pin)
{
  if(!timingLEDIsAllowedToToggle)
  {
    timingLEDIsAllowedToToggle = true;
  }
  if(toggleCounter == toggleMax)
  {
    timingLEDIsAllowedToToggle = false;
    toggleCounter = 0;
    return;
  }
  digitalWrite(pin, timingLEDState);
  timingLEDState = !timingLEDState;
  toggleCounter++;
  calculateNextToggleTime();
}

void calculateNextToggleTime()
{
  unsigned long temp = millis();
  nextTimeToToggle = temp + timeLEDIsOnOrOffInMillis;
}

