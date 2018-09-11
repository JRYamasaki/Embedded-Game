import time

class Timer:
    startTime = 0
    endTime = 0
    totalTime = 0

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.endTime = time.time()
        self.totalTime = self.endTime - self.startTime
        print(self.totalTime)

    def buttonWasPushedAtCorrectTime(self, timeBetweenBlinksInMillis, toleranceLateOrEarly):
        timeBtnShouldBePushed = (8 * timeBetweenBlinksInMillis / 1000)
        lowerBound = timeBtnShouldBePushed - toleranceLateOrEarly
        upperBound = timeBtnShouldBePushed + toleranceLateOrEarly
        if self.totalTime > lowerBound and self.totalTime < upperBound:
            print('Button press was correct!')
            return true
        else:
            print('Button press incorrect')
            print('timeBtnShouldBePushed: ' + str(timeBtnShouldBePushed))
            print('Lower Bound: ' + str(lowerBound))
            print('Upper Bound: ' + str(upperBound))
            print('You pressed the button at: ' + str(self.totalTime))
            return false
