#include <Pin.h>

const uint8_t btn1 = 2;
const uint8_t btn2 = 3;
const uint8_t btn3 = 4;
const uint8_t btn4 = 5;
const uint8_t ledPin1 = 13;
const uint8_t ledPin2 = 12;
const uint8_t ledPin4 = 11;
const uint8_t ledPin8 = 10;

const uint8_t timeBeforeFlushInms = 125;

String serialInput = "";

Pin inputPins[] = {Pin{btn1, 0, "g1btn1\n"},
                   Pin{btn2, 0, "g1btn2\n"},
                   Pin{btn3, 0, "g1btn3\n"},
                   Pin{btn4, 0, "g1btn4\n"}};
                   
uint8_t numOfInputs = sizeof(inputPins) / sizeof(inputPins[0]);

uint8_t buttonState1 = 0;
uint8_t buttonState2 = 0;
uint8_t buttonState3 = 0;
uint8_t buttonState4 = 0;

void setup()
{
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin4, OUTPUT);
  pinMode(ledPin8, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available())
  {
    serialInput = Serial.readString();
    processGame1Data(serialInput);
  }
  readInputPins();
  processInputs();
}

//Helper Functions

void processGame1Data(String data)
{
  if(data.substring(0,2).equals("g1"))
  {
    setNumbers(data.substring(2, data.length())); 
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

void signalTo(int pin, int delayTime)
{
  digitalWrite(pin, HIGH);
  delay(delayTime);
  digitalWrite(pin, LOW);
}

