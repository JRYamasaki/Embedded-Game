import time
import random
import constant

def calculateTimeButtonShouldBePushed(timeBetweenBlinksInMillis):
        return (8 * timeBetweenBlinksInMillis / 1000)

class Timer:

    def __init__(self, serialPort):
        self.serial = serialPort
        self.timeBetweenBlinksInMillis = 100
        self.startTime = 0
        self.endTime = 0
        self.totalTime = 0

    def start(self):
        self.timeBetweenBlinksInMillis = random.randint(constant.LOWERBOUNDINMS, constant.UPPERBOUNDINMS);
        self.startTime = time.time()
        self.serial.write(('2,' + str(self.timeBetweenBlinksInMillis)).encode())

    def stop(self):
        self.endTime = time.time()
        self.totalTime = self.endTime - self.startTime
        print(self.totalTime)
        timeBtnShouldBePushed = calculateTimeButtonShouldBePushed(self.timeBetweenBlinksInMillis)
        lowerBound = timeBtnShouldBePushed - constant.TOLERANCEINSEC
        upperBound = timeBtnShouldBePushed + constant.TOLERANCEINSEC
        if self.totalTime > lowerBound and self.totalTime < upperBound:
            print('Button press was correct!')
            return True
        else:
            print('Button press incorrect')
            print('timeBtnShouldBePushed: ' + str(timeBtnShouldBePushed))
            print('Lower Bound: ' + str(lowerBound))
            print('Upper Bound: ' + str(upperBound))
            print('You pressed the button at: ' + str(self.totalTime))
            return False
