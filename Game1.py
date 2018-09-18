import random

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

class Game1():
    
    def __init__(self, serialPort, randomint):
        self.serial = serialPort
        self.randomInt = randomint

    def processInput(self, userResponse):
        #Take off newline and game indicator
        userResponse = int(userResponse[1])
        #process the answer
        print(userResponse)
        if(game1lookup[self.randomInt] == userResponse):
            print("Correct!")
            return True
        else:
            print("Incorrect")
            return False

        #generate new number and send to arduino
        self.randomInt = random.randint(1, 15)
        self.serial.write(('1' + str(self.randomInt)).encode())
