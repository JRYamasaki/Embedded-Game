import serial
import constant
import time
from Game1 import Game1
from Timer import Timer
from StrikeCounter import StrikeCounter

arduinoSerialData = serial.Serial('/dev/ttyACM0', 115200)

timer = Timer(arduinoSerialData)

def test_processInput_correct_value():
    numberBeingDisplayed = 1
    game = Game1(arduinoSerialData, numberBeingDisplayed)
    userAnswer = "11"
    assert game.processInput(userAnswer) == True, "Correct Input returned False - Game 1"

def test_processInput_incorrect_value():
    numberBeingDisplayed = 13
    game = Game1(arduinoSerialData, numberBeingDisplayed)
    userAnswer = "11"
    assert game.processInput(userAnswer) == False, "Incorrect Input returned True - Game 1"

def test_checkForStrikeIncrement_increment():
    counter = StrikeCounter()
    counter.checkForStrikeIncrement(False)
    assert counter.strikes == 1, "Strike Counter did not increment"

def test_checkForStrikeIncrement_no_increment():
    counter = StrikeCounter()
    counter.checkForStrikeIncrement(True)
    assert counter.strikes == 0, "Strike Counter did increment"

def test_timer_early_stop():
    timer.start()
    timeToWait = (8 * timer.timeBetweenBlinksInMillis / 1000) - constant.TOLERANCEINSEC - (constant.TOLERANCEINSEC / 10)
    time.sleep(timeToWait)
    assert timer.stop() == False, "Stop() returned true even though the button was pushed too early"

def test_timer_late_stop():
    timer.start()
    timeToWait = (8 * timer.timeBetweenBlinksInMillis / 1000) + constant.TOLERANCEINSEC + (constant.TOLERANCEINSEC / 10)
    time.sleep(timeToWait)
    assert timer.stop() == False, "Stop() returned true even though the button was pushed too late"

def test_timer_correct_stop():
    timer.start()
    timeToWait = (8 * timer.timeBetweenBlinksInMillis / 1000)
    time.sleep(timeToWait)
    assert timer.stop() == True, "Stop() returned False even though the button was pushed at the correct time"
    
if __name__ == '__main__':
    test_processInput_correct_value()
    test_processInput_incorrect_value()
    test_checkForStrikeIncrement_increment()
    test_checkForStrikeIncrement_no_increment()
    test_timer_early_stop()
    test_timer_late_stop()
    test_timer_correct_stop()
        
