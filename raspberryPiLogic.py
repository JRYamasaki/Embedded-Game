import serial
import random

arduinoSerialData = serial.Serial('/dev/ttyACM0', 9600)
randomInt = random.randint(1, 15)
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

#Functions
def gameInit():
    #Send initial random number to game 1
    arduinoSerialData.write(('g1' + str(randomInt)).encode()) 

def processGame1Input(userResponse):
    global randomInt
    #Take off newline and game indicator
    userResponse = userResponse[2:-1]
    #process the answer
    print(userResponse)
    processGame1Answer(randomInt, userResponse)

    #generate new number and send to arduino
    randomInt = random.randint(1, 15)
    arduinoSerialData.write(('g1' + str(randomInt)).encode())
    
def processGame1Answer(challengeNum, userResponse):
    numberResponse = int(userResponse[-1:])
    a = bool(challengeNum & 1)
    b = bool((challengeNum & 2) >> 1)
    c = bool((challengeNum & 4) >> 2)
    d = bool((challengeNum & 8) >> 3)

    if(game1lookup[challengeNum] == numberResponse):
        print("Correct!")
    else:
        print("Incorrect")
        
# -------------- Game start ----------------
gameInit()

while 1:
    if(arduinoSerialData.inWaiting()>0):
        myData = arduinoSerialData.readline().decode("utf-8")
        #If the data being sent was meant for game 1
        if(myData[:2] == "g1"):
            processGame1Input(myData)
