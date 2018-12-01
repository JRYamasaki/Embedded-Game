import serial
import random
import time
import constant
from Game1 import Game1
from Timer import Timer
from StrikeCounter import StrikeCounter
from KeypadSequence import SequenceAnalyzer

arduinoSerialData = serial.Serial('/dev/ttyACM0', 115200)
randomInt = random.randint(1, 15)
strikes = 0

#Functions
def gameInit(seqAnalyzer):
    #Send initial random number to game 1
    time.sleep(1)
    arduinoSerialData.write(('1' + str(randomInt)).encode())
    time.sleep(0.01) # necessary for sequence analyzer to write to the arduino
    seqAnalyzer.setSequence(str(random.choice(list(constant.SEQUENCEPAIRS.keys()))), arduinoSerialData)

def checkForGameOver():
    if(strikes >= constant.MAXSTRIKES):
        print("GAME OVER")
        quit()

def main():
    LEDGame = Game1(arduinoSerialData, randomInt)
    timer = Timer(arduinoSerialData)
    strikes = StrikeCounter()
    seqAnalyzer = SequenceAnalyzer()
    gameInit(seqAnalyzer)
    cycles = 0
    startTime = 0
    currentTime = 0
    processingSequence = False

    while True:
        cycles += 1
        if(startTime != 0):
            currentTime = time.time() * 1000.0
            processingSequence = True
        if (currentTime - startTime > 2000.0):
            seqAnalyzer.setSequence(str(random.choice(list(constant.SEQUENCEPAIRS.keys()))), arduinoSerialData)
            startTime = 0
            currentTime = 0
            processingSequence = False
        if (cycles == constant.MAXCYCLES):
            cycles = 0
            timer.start()
        if arduinoSerialData.inWaiting() > 0:
            myData = arduinoSerialData.readline().decode("utf-8")
            if(myData[:1] == "2"):
                result = timer.stop()
                strikes.checkForStrikeIncrement(result)
                cycles = 0
            #If the data being sent was meant for game 1
            if(myData[:1] == "1"):
                result = LEDGame.processInput(myData)
                strikes.checkForStrikeIncrement(result)
            if(myData[:1] == "3" and processingSequence is False):
                seqAnalyzer.addCharacter(myData[1])
                startTime = seqAnalyzer.checkIfSequenceNeedsProcessing(arduinoSerialData)
            else:
                print(myData)
        checkForGameOver()

if __name__ == '__main__':
    main()
