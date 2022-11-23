from OneLookPlayer import OneLook
from AStarPlayer import AStar
from SmartPlayer import SmartPlayer
from TrialPlayer import TrialPlayer
from Util import BananagramsUtil as util

scrabble = {"A": 1, "E": 1, "I": 1, "L": 1, "N": 1, "O": 1, "R": 1, "S": 1, "T": 1, "U": 1,
            "D": 2, "G": 2,
            "B": 3, "C": 3, "M": 3, "P": 3,
            "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
            "K": 5,
            "J": 8, "X": 8,
            "Q": 10, "Z": 10}


def scrabbleScore(letters):
    points = 0
    for letter in letters:
        points += scrabble[letter.upper()]  # add scrabble tile value
    return points


# one look player that plays the highest scoring scrabble word available
class ScrabbleOneLook(OneLook):
    def __str__(self):
        return "Scrabble One Look"

    def heuristic(self, play):
        word = play[0]
        return scrabbleScore(word)


# A* player that uses words with high scrabble scores first
class ScrabbleAStar(AStar):
    def __str__(self):
        return "Scrabble A*"

    def heuristic(self, state):
        return scrabbleScore(util.handToString(state.hand))


class ScrabbleOneLookTrial(TrialPlayer, ScrabbleOneLook):
    def __init__(self, sampleNumber):
        super().__init__(sampleNumber)

    def sampleHeuristic(self, board):
        words = util.check(board)[0]
        wordCount = len(words)
        total = 0
        for w in words:
            total += len(w)
        return total / wordCount

    def __str__(self):
        return "Scrabble One Look Trial: Sample Number %s" % self.sampleNumber


class ScrabbleAStarTrial(TrialPlayer, ScrabbleAStar):
    def __init__(self, sampleNumber):
        super().__init__(sampleNumber)

    def __str__(self):
        return "Scrabble One Look Trial: Sample Number %s" % self.sampleNumber

    def sampleHeuristic(self, board):
        words = util.check(board)[0]
        wordCount = len(words)
        total = 0
        for w in words:
            total += scrabbleScore(w)
        return total / wordCount


class ScrabbleOneLookSmarty(SmartPlayer, ScrabbleOneLookTrial):
    def __init__(self, sampleNumber, planAt):
        super().__init__(sampleNumber, planAt)

    def __str__(self):
        if self.planAt == 1:
            return "Scrabble One Look Smarty: Sample Number %s, Plan at 1 tile" % self.sampleNumber
        return "Scrabble One Look Smarty: Sample Number %s, Plan at %s tile" % (self.sampleNumber, self.planAt)


class ScrabbleAStarSmarty(SmartPlayer, ScrabbleAStarTrial):
    def __init__(self, sampleNumber, planAt):
        super().__init__(sampleNumber, planAt)

    def __str__(self):
        if self.planAt == 1:
            return "Scrabble AStar Smarty: Sample Number %s, Plan at 1 tile" % self.sampleNumber
        return "Scrabble AStar Smarty: Sample Number %s, Plan at %s tile" % (self.sampleNumber, self.planAt)
