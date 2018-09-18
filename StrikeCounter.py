import constant

class StrikeCounter:

    def __init__(self):
        self.strikes = 0

    def checkForGameOver(self):
        if(self.strikes >= constant.MAXSTRIKES):
            print("GAME OVER")
            quit()

    def checkForStrikeIncrement(self, answerIsCorrect):
        if(answerIsCorrect is False):
            self.strikes += 1
            self.checkForGameOver()
