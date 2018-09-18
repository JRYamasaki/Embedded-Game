import serial
import random
import time
import constant
from Game1 import Game1
from Timer import Timer

arduinoSerialData = serial.Serial('/dev/ttyACM0', 115200)
randomInt = random.randint(1, 15)
strikes = 0

#Functions
def gameInit():
    #Send initial random number to game 1
    time.sleep(1);
    arduinoSerialData.write(('1' + str(randomInt)).encode());

def checkForGameOver():
    if (strikes >= constant.MAXSTRIKES):
        print("GAME OVER")
        quit()
        
def main():
    LEDGame = Game1(arduinoSerialData, randomInt)
    timer = Timer(arduinoSerialData)
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
                timer.stop()
                cycles = 0
            #If the data being sent was meant for game 1
            if(myData[:1] == "1"):
                LEDGame.processInput(myData)
            else:
                print(myData)
        checkForGameOver()

if __name__ == '__main__':
    main()
