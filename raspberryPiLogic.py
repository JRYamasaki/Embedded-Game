import serial
import random
arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)

randomInt = random.randint(1, 15)

arduinoSerialData.write(str(randomInt).encode())

while 1:
    if(arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        print(myData)
        randomInt = random.randint(1, 15)
        arduinoSerialData.write(str(randomInt).encode())
        print(randomInt)
