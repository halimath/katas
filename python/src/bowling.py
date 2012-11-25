"""
    A kata to improve an iterative design using test driven development.
    
    Write a software component (class etc.) that models a bowling game for 
    a single player. A Bowling game has some simple rules for counting a
    player's score in normal situations. But under some circumstances, things
    get a little more complicated.
    
    You can find an introduction here: 
        http://en.wikipedia.org/wiki/Bowling#Scoring
"""
import unittest

class Frame (object):
    def __init__(self, frameNumber):
        self._frameNumber = frameNumber
        self.pinsFirstRoll = -1
        self.pinsSecondRoll = -1
        
    def hitPins (self, pins = 0):
        if self.new:
            self.pinsFirstRoll = pins
            if pins == 10:
                self.pinsSecondRoll = 0
        else:
            self.pinsSecondRoll = pins
            
    @property
    def roll (self):
        if self.pinsFirstRoll == -1:
            return 1
        return 2
    
    @property
    def frameNumber (self):
        return self._frameNumber
    
    @property
    def new (self):
        return self.pinsFirstRoll == -1
    
    @property
    def running (self):
        return not self.new and self.pinsSecondRoll == -1 
    
    @property
    def spare (self):
        return not self.new and \
            not self.running and \
            self.pinsFirstRoll < 10 and \
            self.pinsFirstRoll + self.pinsSecondRoll == 10

    @property
    def strike (self):
        return not self.new and \
            not self.running and \
            self.pinsFirstRoll == 10
            
    def calculateScore (self, framePlusOne = None, framePlusTwo = None):
        if self.new or self.running:
            return 0
        
        if self.strike:
            if not framePlusOne or framePlusOne.new or framePlusOne.running:
                return 0
            
            if framePlusOne.strike:
                if not framePlusTwo or framePlusTwo.new:
                    return 0
                else:
                    return 20 + framePlusTwo.pinsFirstRoll
    
            else:
                return 10 + \
                       framePlusOne.pinsFirstRoll + \
                       framePlusOne.pinsSecondRoll
            
        if self.spare:
            if framePlusOne and not framePlusOne.new:
                return 10 + framePlusOne.pinsFirstRoll
            return 0

        return self.pinsFirstRoll + self.pinsSecondRoll

    
class LastFrame (Frame):
    def __init__ (self, frameNumber):
        Frame.__init__(self, frameNumber)
        self.pinsThirdRoll = -1
        
    def hitPins (self, pins = 0):
        if self.pinsFirstRoll == -1:
            self.pinsFirstRoll = pins
            return
        if self.pinsSecondRoll == -1:
            self.pinsSecondRoll = pins
            return
        self.pinsThirdRoll = pins
        
    def calculateScore (self, framePlusOne = None, framePlusTwo = None):
        if self.running:
            return 0
        if not self.hasThirdRoll:
            return Frame.calculateScore(self, None, None) 
        
        result = self.pinsFirstRoll
        if self.pinsFirstRoll == 10:
            result += self.pinsSecondRoll + self.pinsThirdRoll
        result += self.pinsSecondRoll
        if self.pinsSecondRoll == 10:
            result += self.pinsThirdRoll
        result += self.pinsThirdRoll
        return result
    
    @property
    def roll (self):
        if self.pinsFirstRoll == -1:
            return 1
        if self.pinsSecondRoll == -1:
            return 2
        return 3
    
    @property
    def running (self):
        if self.new:
            return True
        if self.hasThirdRoll:
            return self.pinsThirdRoll == -1
        return self.pinsSecondRoll == -1
    
    @property
    def hasThirdRoll (self):
        return self.pinsFirstRoll == 10 or \
            self.pinsFirstRoll + self.pinsSecondRoll == 10    

class BowlingGame (object):
    def __init__(self):
        self._frames = [Frame(1)]
    
    def hitPins (self, pins = 0):
        self._frames[-1].hitPins(pins)
        if not self._frames[-1].running:
            if len(self._frames) < 9:
                self._frames.append(Frame(len(self._frames) + 1))
            else:
                self._frames.append(LastFrame(10))
    
    @property
    def score (self):
        score = 0
        for i in range(0, len(self._frames)):
            frame = self._frames[i]
            framePlusOne = \
                self._frames[i + 1] if i < len(self._frames) - 1 else None
            framePlusTwo = \
                self._frames[i + 2] if i < len(self._frames) - 2 else None
            
            score += frame.calculateScore(framePlusOne, framePlusTwo)

        return score
    
    @property
    def frame (self):
        return self._frames[-1].frameNumber
    
    @property
    def roll (self):
        return self._frames[-1].roll

class BowlingGameTest (unittest.TestCase):
    def setUp (self):
        self.game = BowlingGame()
    
    def testShouldHaveInitialScoreOfZero (self):
        self.assertEquals(0, self.game.score)

    def testShouldReturnFrameOneRollOneAfterInitializingGame (self):
        self.assertEquals(1, self.game.frame)
        self.assertEquals(1, self.game.roll)

    def testShouldReturnFrameOneRollTwoAndScoreZeroAfterMakingFirstRoll (self):
        self.game.hitPins()
        
        self.assertEquals(1, self.game.frame)
        self.assertEquals(2, self.game.roll)

        self.assertEquals(0, self.game.score)

    def testShouldReturnFrameTwoRollOneAndScoreEightAfterMakingTwoRollsTotalingEightPins (self):
        self.game.hitPins(5)
        self.game.hitPins(3)
        
        self.assertEquals(2, self.game.frame)
        self.assertEquals(1, self.game.roll)

        self.assertEquals(8, self.game.score)

    def testShouldReturnFrameTwoRollTwoAndScoreEightAfterMakingThreeRolls (self):
        self.game.hitPins(5)
        self.game.hitPins(3)

        self.game.hitPins(8)
        
        self.assertEquals(2, self.game.frame)
        self.assertEquals(2, self.game.roll)

        self.assertEquals(8, self.game.score)

    def testShouldReturnFrameTwoRollOneAndScoreZeroAfterRollingASpare (self):
        self.game.hitPins(5)
        self.game.hitPins(5)

        self.assertEquals(2, self.game.frame)
        self.assertEquals(1, self.game.roll)

        self.assertEquals(0, self.game.score)

    def testShouldReturnFrameTwoRollTwoAndScore15AfterRollingASpareAndAnotherFivePins (self):
        self.game.hitPins(5)
        self.game.hitPins(5)
        self.game.hitPins(5)

        self.assertEquals(2, self.game.frame)
        self.assertEquals(2, self.game.roll)

        self.assertEquals(15, self.game.score)

    def testShouldReturnFrameTwoRollOneWhenRollingAStrike (self):
        self.game.hitPins(10)

        self.assertEquals(2, self.game.frame)
        self.assertEquals(1, self.game.roll)

    def testShouldReturnScoreZeroWhenRollingAStrike (self):
        self.game.hitPins(10)

        self.assertEquals(0, self.game.score)

    def testShouldScoreZeroWhenRollingAStrikeAndHittingAnotherFivePins (self):
        self.game.hitPins(10)
        self.game.hitPins(5)

        self.assertEquals(0, self.game.score)

    def testShouldScoreTwentySixWhenRollingAStrikeAndHittingAnotherFivePins (self):
        self.game.hitPins(10)
        self.game.hitPins(5)
        self.game.hitPins(3)

        self.assertEquals(26, self.game.score)
        
    def testShouldScore51WhenRollingTwoStrikesAndHittingAnotherFiveAndThreePins (self):
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(5)
        self.game.hitPins(3)

        self.assertEquals(51, self.game.score)
        
    def testShouldScore30WhenRollingThreeStrikesInARow (self):
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)

        self.assertEquals(30, self.game.score)

    def testShouldScore239WhenRollingEightStrikesAndTwoOpenFrames (self):
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)

        self.game.hitPins(5)
        self.game.hitPins(4)

        self.game.hitPins(3)
        self.game.hitPins(3)

        self.assertEquals(239, self.game.score)

    def testShouldAllowThirdRollInLastFrameWhenRollingASpare (self):
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)

        self.game.hitPins(5)
        self.game.hitPins(5)

        self.assertEquals(10, self.game.frame)
        self.assertEquals(3, self.game.roll)

    def testShouldHaveScoreOfThreeHundredWhenPlayingAPerfectGame (self):
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)

        self.game.hitPins(10)
        self.game.hitPins(10)
        self.game.hitPins(10)

        self.assertEquals(300, self.game.score)