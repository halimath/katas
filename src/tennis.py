"""
    Another slightly more complex kata that focusses on
    - test driven development
    - baby steps

    Create a component that models a single game of tennis. Scoring in tennis
    is somewhat more complicated than in other games (such as soccer); see
        http://en.wikipedia.org/wiki/Tennis_score
    for a good introduction.
"""

import unittest;

class Score (object):
    """
        Class which instances represent the score for a single player.         
    """
    SELF = "self"
    
    def __init__(self, label, nextScore, nextScoreWhenEqual=None):
        """
            Initializes this score. 
            
            Label is used as a textual representation of the score.
            nextScore is a score object to be returned when this score is 
            incremented.
            nextScoreWhenEqual will be used when incrementing this score and
            the opponent's score has the same value. When given Score.SELF
            this instance is used as the score to return when opponents score
            and this score are equal.
        """
        self._label = label
        self._nextScore = nextScore
        if nextScoreWhenEqual:
            if nextScoreWhenEqual == Score.SELF:
                self._nextScoreWhenEven = self
            else:
                self._nextScoreWhenEven = nextScoreWhenEqual
        else:
            self._nextScoreWhenEven = nextScore
    
    def increment (self, opponentsScore):
        """
            Increments this score after the owning player scores on point.
            opponentsScores is the score of the opponents (the player not
            scoring the point).
            Returns a tuple of two scores: (newScore, opponentsNewScore).
        """
        if opponentsScore == self._nextScore:
            return (self._nextScoreWhenEven, self._nextScoreWhenEven)
        return (self._nextScore, opponentsScore)
        
    def __str__ (self):
        return self._label

    def __repr__ (self):
        return self._label


class Game (object):
    """
        Represents a single game in tennis.
    """
    GAME = Score('game', None)
    ADVANTAGE = Score('advantage', GAME)
    DEUCE = Score('deuce', ADVANTAGE, Score.SELF)
    FOURTY = Score('fourty', GAME)    
    THIRTY = Score('thirty', FOURTY, DEUCE)
    FIFTEEN = Score('fifteen', THIRTY)
    LOVE = Score('love', FIFTEEN)
    
    def __init__(self):
        self._currentScorePlayerOne = Game.LOVE
        self._currentScorePlayerTwo = Game.LOVE
        
    def scorePlayerOne (self):
        (self._currentScorePlayerOne, self._currentScorePlayerTwo) = self._currentScorePlayerOne.increment(self._currentScorePlayerTwo)
            
    def scorePlayerTwo (self):
        (self._currentScorePlayerTwo, self._currentScorePlayerOne) = self._currentScorePlayerTwo.increment(self._currentScorePlayerOne)
        
    @property
    def currentScorePlayerOne (self):
        return self._currentScorePlayerOne

    @property
    def currentScorePlayerTwo (self):
        return self._currentScorePlayerTwo

class TennisGameTest (unittest.TestCase):
    def setUp (self):
        self.game = Game()
    
    def test_shouldHaveInitialScoreOfLoveAll (self):
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerTwo)

    def test_shouldHaveScoreOfFifteenLoveWhenFirstPlayerScores (self):
        self.game.scorePlayerOne()
        
        self.assertEquals(Game.FIFTEEN, self.game.currentScorePlayerOne)
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerTwo)

    def test_shouldHaveScoreOfThirtyLoveWhenFirstPlayerScoresTwoTimes (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.assertEquals(Game.THIRTY, self.game.currentScorePlayerOne)
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerTwo)

    def test_shouldHaveScoreOfFourtyLoveWhenFirstPlayerScoresThreeTimes (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.assertEquals(Game.FOURTY, self.game.currentScorePlayerOne)
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerTwo)

    def test_shouldHaveScoreOfGameLoveWhenFirstPlayerScoresFourTimes (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.assertEquals(Game.GAME, self.game.currentScorePlayerOne)
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerTwo)

    def test_shouldHaveScoreOfFifteenAllWhenBothPlayerScoreOnePoint (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerTwo()
        
        self.assertEquals(Game.FIFTEEN, self.game.currentScorePlayerOne)
        self.assertEquals(Game.FIFTEEN, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfLoveThirtyWhenPlayerTwoScoresTwoTimes (self):
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.THIRTY, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfLoveFourtyWhenPlayerTwoScoresThreeTimes (self):
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.FOURTY, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfLoveGameWhenPlayerTwoScoresFourTimes (self):
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.assertEquals(Game.LOVE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.GAME, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfDeuceWhenBothPlayersScoresThreeTimes (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfAdvantageForPlayerOneWhenBothPlayersScoresThreeTimesAndPlayerOneScoresAnotherTime (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.game.scorePlayerOne()

        self.assertEquals(Game.ADVANTAGE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfGameForPlayerOneWhenBothPlayersScoresThreeTimesAndPlayerOneScoresAnotherTwoTimes (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()

        self.assertEquals(Game.GAME, self.game.currentScorePlayerOne)
        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerTwo)        

    def test_shouldHaveScoreOfDeuceWhenBothPlayersScoresThreeTimesAndPlayerOneScoresAnotherTimeAndPlayerTwoScoresAnotherTime (self):
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        self.game.scorePlayerOne()
        
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        self.game.scorePlayerTwo()
        
        self.game.scorePlayerOne()
        
        self.game.scorePlayerTwo()

        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerOne)
        self.assertEquals(Game.DEUCE, self.game.currentScorePlayerTwo)        
