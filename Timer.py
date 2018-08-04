import time

class Timer:
    startTime = 0
    endTime = 0

    def start(self):
        self.startTime = time.time()
        print(self.startTime)

    def stop(self):
        self.endTime = time.time()
        print(self.endTime)
        return self.endTime - self.startTime

    def calculateIfCorrectTime(self, timeBetweenBlinks, toleranceLateOrEarly):
        timeBtnShouldBePushed = (8 * timeBetweenBlinks) + self.startTime
        lowerBound = timeBtnShouldBePushed - toleranceLateOrEarly
        upperBound = timeBtnShouldBePushed + toleranceLateOrEarly
        if self.endTime > lowerBound and self.endTime < upperBound:
            print('Button press was correct!')
        else:
            print('Button press incorrect')
            print('timeBtnShouldBePushed: ' + str(timeBtnShouldBePushed))
            print('Lower Bound: ' + str(lowerBound))
            print('Upper Bound: ' + str(upperBound))
            print('You pressed the button at: ' + str(self.endTime))
