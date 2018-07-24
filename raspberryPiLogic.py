import serial
import random

game1lookup = { 1: 1,
                2: 4,
                3: 1,
                4: 2,
                5: 2,
                6: 3,
                7: 4,
                8: 4,
                9: 3,
                10: 1,
                11: 1,
                12: 2,
                13: 2,
                14: 4,
                15: 3 }

def processAnswer(challengeNum, userResponse):
    numberResponse = int(userResponse[-1:])
    a = bool(challengeNum & 1)
    b = bool((challengeNum & 2) >> 1)
    c = bool((challengeNum & 4) >> 2)
    d = bool((challengeNum & 8) >> 3)

    if(game1lookup[challengeNum] == numberResponse):
        print("Correct!")
    else:
        print("Incorrect")

arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)

randomInt = random.randint(1, 15)

arduinoSerialData.write(str(randomInt).encode())

while 1:
    if(arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline()
        #Take off newline
        myData = myData[:-1]
        #process the answer
        print(myData)
        processAnswer(randomInt, myData)

        #generate new number and send to arduino
        randomInt = random.randint(1, 15)
        arduinoSerialData.write(str(randomInt).encode())
        print(randomInt)
