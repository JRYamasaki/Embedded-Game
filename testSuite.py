import serial
import constant
import time
from Game1 import Game1
from Timer import Timer
from StrikeCounter import StrikeCounter
from KeypadSequence import SequenceAnalyzer

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

def test_keypad_add_character():
    sequence = SequenceAnalyzer()
    sequence.addCharacter("1");
    assert len(sequence.userSequence) == 1, "addCharacter() did not properly add character to the sequence"

def test_keypad_add_character_too_many_characters():
    sequence = SequenceAnalyzer()
    for i in range(constant.KEYPADSEQUENCELENGTH + 1):
        sequence.addCharacter("1")
    assert len(sequence.userSequence) == constant.KEYPADSEQUENCELENGTH, "addCharacter() did not stop overflow of length"

def test_keypad_process_sequence_correct():
    sequence = SequenceAnalyzer()
    key = list(constant.SEQUENCEPAIRS.keys())[0]
    correctSequence = list(constant.SEQUENCEPAIRS.values())[0]
    sequence.setSequence(key)
    for char in correctSequence:
        sequence.addCharacter(char)
    assert sequence.processSequence() == True, "processSequence did not return True when user input was correct"

def test_keypad_process_sequence_incorrect():
    sequence = SequenceAnalyzer()
    key = list(constant.SEQUENCEPAIRS.keys())[0]
    correctSequence = list(constant.SEQUENCEPAIRS.values())[0]
    sequence.setSequence(key)
    sequence.addCharacter('?')
    for char in correctSequence:
        sequence.addCharacter(char)
    assert sequence.processSequence() == False, "processSequence did not return False when user input was incorrect"

if __name__ == '__main__':
    test_processInput_correct_value()
    test_processInput_incorrect_value()
    test_checkForStrikeIncrement_increment()
    test_checkForStrikeIncrement_no_increment()
    test_timer_early_stop()
    test_timer_late_stop()
    test_timer_correct_stop()
    test_keypad_add_character()
    test_keypad_add_character_too_many_characters()
    test_keypad_process_sequence_correct()
    test_keypad_process_sequence_incorrect()
        
