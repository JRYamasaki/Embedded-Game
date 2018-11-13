#include <Pin.h>
#include <LiquidCrystal.h>

// Constants
const uint16_t delayTimeInMs = 500;

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

//LCD Display Constants
//pin 1 to ground
//pin 2 to 5V
//pin 3 to 10K pot
const uint8_t rs =24;
const uint8_t en = 26;
const uint8_t d4 = 28;
const uint8_t d5 = 30;
const uint8_t d6 = 32;
const uint8_t d7 = 34;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

//Keypad Constants
const uint8_t starKey = 23;

// Global Variables
Pin inputPins[] = {Pin{btn1, "11\n"},
                   Pin{btn2, "12\n"},
                   Pin{btn3, "13\n"},
                   Pin{btn4, "14\n"},
                   Pin{timingButton, "2\n"},
                   Pin{starKey, "3*"}};
const uint8_t numOfInputs = sizeof(inputPins) / sizeof(inputPins[0]);

String serialInput = "";
uint8_t toggleCounter = 0;
long nextTimeToToggle = 0;
unsigned long timeLEDIsOnOrOffInMillis = 0;
boolean timingLEDIsAllowedToToggle = false;
boolean timingLEDState = true;

void setup()
{
  lcd.begin(16, 2); // number of rows and columns
  lcd.print("Code goes here");
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin8, OUTPUT);
  pinMode(timingLED, OUTPUT);
  Serial.begin(115200);
  Serial.setTimeout(10);
}

void loop()
{
  if(Serial.available())
  {
    allocateSerialData(Serial.readString());
  }
  checkForToggleEvent();
  readInputPins();
}

//Helper Functions

void allocateSerialData(const String& data)
{
  processGame1Data(data);
  processGame2Data(data);
}

void processGame1Data(String data)
{
  if(data.charAt(0) == '1')
  {
    setNumbers(data.substring(1, data.length()));
  }
}

void processGame2Data(String data)
{
  if(data.charAt(0) == '2')
  {
    timeLEDIsOnOrOffInMillis = data.substring(data.indexOf(',') + 1, data.length()).toInt();
    toggleLED(timingLED);
    timingLEDIsAllowedToToggle = true;
  }
}

void processGame3Data(String data)
{
  lcd.print(data);
}

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

void readInputPins()
{
  for(int i = 0; i < numOfInputs; i++)
  {
    if(digitalRead(inputPins[i].getPinNumber()))
    {
      Serial.print(inputPins[i].getMessage());
      delay(delayTimeInMs);
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

