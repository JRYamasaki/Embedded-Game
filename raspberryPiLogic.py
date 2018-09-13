import serial
import random
import time
import constant
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
strikes = 0

#Functions
def gameInit():
    #Send initial random number to game 1
    time.sleep(1);
    arduinoSerialData.write(('1' + str(randomInt)).encode());

def processGame1Input(userResponse):
    global randomInt
    #Take off newline and game indicator
    userResponse = int(userResponse[1])
    #process the answer
    print(userResponse)
    processGame1Answer(randomInt, userResponse)

    #generate new number and send to arduino
    randomInt = random.randint(1, 15)
    arduinoSerialData.write(('1' + str(randomInt)).encode())
    
def processGame1Answer(challengeNum, numberResponse):
    a = bool(challengeNum & 1)
    b = bool((challengeNum & 2) >> 1)
    c = bool((challengeNum & 4) >> 2)
    d = bool((challengeNum & 8) >> 3)

    if(game1lookup[challengeNum] == numberResponse):
        print("Correct!")
    else:
        print("Incorrect")
        global strikes
        strikes += 1;

def checkForGameOver():
    if (strikes >= constant.MAXSTRIKES):
        print("GAME OVER")
        exit()
        
def main():
    gameInit()
    global strikes
    cycles = 0
    timer = Timer()
    timeBetweenBlinksInMillis = 0

    while True:
        cycles += 1
        if (cycles == constant.MAXCYCLES):
            cycles = 0
            timeBetweenBlinksInMillis = random.randint(constant.LOWERBOUNDINMS, constant.UPPERBOUNDINMS);
            timer.start()
            arduinoSerialData.write(('2,' + str(timeBetweenBlinksInMillis)).encode())
        if arduinoSerialData.inWaiting() > 0:
            myData = arduinoSerialData.readline().decode("utf-8")
            if(myData[:1] == "2"):
                timer.stop()
                cycles = 0
                if(timer.buttonWasPushedAtCorrectTime(timeBetweenBlinksInMillis, constant.TOLERANCEINSEC) is False):
                    strikes += 1
            #If the data being sent was meant for game 1
            if(myData[:1] == "1"):
                processGame1Input(myData)
            else:
                print(myData)
        checkForGameOver()

if __name__ == '__main__':
    main()
