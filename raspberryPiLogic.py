import serial
import random
import time
from Timer import Timer

arduinoSerialData = serial.Serial('/dev/ttyACM0', 115200)
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
cycleLimit = 250000 * 2
timeIntervalLowerBound = 300
timeIntervalUpperBound = 999
toleranceForTiming = 3

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
cycles = 0
timer = Timer()
timeBetweenBlinks = 0
toleranceLateOrEarly = 0

while True:
    cycles += 1
    #If this print statement is taken away, cycles becomes 100
    if (cycles == cycleLimit):
        #Divide by 100 to convert back to seconds
        timeBetweenBlinks = random.randint(timeIntervalLowerBound, timeIntervalUpperBound);
        toleranceLateOrEarly = (toleranceForTiming / 2)
        timer.start()
        arduinoSerialData.write(('g2,' + str(timeBetweenBlinks)).encode())
        print('num was ' + str(timeBetweenBlinks))
        cycles = 0
    if arduinoSerialData.inWaiting() > 0:
        myData = arduinoSerialData.readline().decode("utf-8")
        if(myData[:2] == "g2"):
            timer.stop()
            cycles = 0
            timer.calculateIfCorrectTime(timeBetweenBlinks / 1000, toleranceLateOrEarly)
        #If the data being sent was meant for game 1
        if(myData[:2] == "g1"):
            processGame1Input(myData)
        else:
            print(myData)
