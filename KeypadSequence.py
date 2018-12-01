import constant
import time

def printSequenceResult(seqIsCorrect, serialInterface):
    if(seqIsCorrect):
        serialInterface.write(str("3CORRECT2").encode())
    else:
        serialInterface.write(str("3INCORRECT2").encode())

class SequenceAnalyzer:

    def __init__(self):
        self.userSequence = ""
        self.currentSequence = ""

    def addCharacter(self, char):
        if len(self.userSequence) < constant.KEYPADSEQUENCELENGTH:
            self.userSequence += char

    def setSequence(self, sequenceString, serialInterface):
        self.currentSequence = sequenceString
        self.userSequence = ""
        serialInterface.write(('3' + sequenceString + '0').encode())

    def processSequence(self):
        return constant.SEQUENCEPAIRS[self.currentSequence] == self.userSequence

    def checkIfSequenceNeedsProcessing(self, serialInterface):
        startTime = 0
        if(len(self.userSequence) == constant.KEYPADSEQUENCELENGTH):
            sequenceIsCorrect = self.processSequence()
            printSequenceResult(sequenceIsCorrect, serialInterface)
            startTime = time.time() * 1000.0
        else:
            serialInterface.write(("3" + self.userSequence + "1").encode())
        return startTime
        
