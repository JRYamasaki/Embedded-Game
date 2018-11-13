import constant

sequencePairs = { "1" : "######" }

class SequenceAnalyzer:

    def __init__(self):
        self.userSequence = ""
        self.currentSequence = ""

    def addCharacter(self, char):
        if len(self.userSequence) < constant.KEYPADSEQUENCELENGTH:
            self.userSequence += char

    def setSequence(self, sequenceString):
        self.currentSequence = sequenceString

    def processSequence(self):
        return sequencePairs[self.currentSequence] == self.userSequence
        
