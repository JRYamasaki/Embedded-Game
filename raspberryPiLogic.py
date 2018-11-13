import serial
import random
import time
import constant
from Game1 import Game1
from Timer import Timer
from StrikeCounter import StrikeCounter

arduinoSerialData = serial.Serial('/dev/ttyACM0', 115200)
randomInt = random.randint(1, 15)
strikes = 0

#Functions
def gameInit():
    #Send initial random number to game 1
    time.sleep(1)
    arduinoSerialData.write(('1' + str(randomInt)).encode())
    time.sleep(0.125)
    arduinoSerialData.write(('3' + str(random.choice(list(constant.SEQUENCEPAIRS.keys()))) + '0').encode())

def checkForGameOver():
    if (strikes >= constant.MAXSTRIKES):
        print("GAME OVER")
        quit()
        
def main():
    LEDGame = Game1(arduinoSerialData, randomInt)
    timer = Timer(arduinoSerialData)
    strikes = StrikeCounter()
    gameInit()
    cycles = 0

    while True:
        cycles += 1
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
            if(myData[:1] == "3"):
                print(myData[1])
            else:
                print(myData)
        checkForGameOver()

if __name__ == '__main__':
    main()
