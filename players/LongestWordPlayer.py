from game.OneLookPlayer import OneLook
from game.AStarPlayer import AStar
from game.SmartPlayer import SmartPlayer
from game.TrialPlayer import TrialPlayer
from game.Util import BananagramsUtil as util


# one look player that plays the longest word available
class LongestOneLook(OneLook):
    # what should return when printed
    def __str__(self):
        return "Longest Word One Look"

    # evaluate play/state
    def heuristic(self, play):
        return len(play[0])  # return length of word


# A* player that plays the longest words available
class LongestAStar(AStar):
    def __str__(self):
        return "Longest Word A*"

    # A* heuristics take in states, not plays params: state to evaluate
    def heuristic(self, state):  # this should guess the number of words left
        return util.countTiles(state.hand)


class LongestOneLookTrial(TrialPlayer, LongestOneLook):
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
        return "Longest One Look Trial: Sample Number %s" % self.sampleNumber


class LongestAStarTrial(TrialPlayer, LongestAStar):
    def __init__(self, sampleNumber):
        super().__init__(sampleNumber)

    def __str__(self):
        return "Longest One Look Trial: Sample Number %s" % self.sampleNumber

    def sampleHeuristic(self, board):
        words = util.check(board)[0]
        wordCount = len(words)
        total = 0
        for w in words:
            total += len(w)
        return total / wordCount


class LongestOneLookSmarty(SmartPlayer, LongestOneLookTrial):
    def __init__(self, sampleNumber, planAt):
        super().__init__(sampleNumber, planAt)

    def __str__(self):
        if self.planAt == 1:
            return "Longest One Look Smarty: Sample Number %s, Plan at 1 tile" % self.sampleNumber
        return "Longest One Look Smarty: Sample Number %s, Plan at %s tile" % (self.sampleNumber, self.planAt)


class LongestAStarSmarty(SmartPlayer, LongestAStarTrial):
    def __init__(self, sampleNumber, planAt):
        super().__init__(sampleNumber, planAt)

    def __str__(self):
        if self.planAt == 1:
            return "Longest AStar Smarty: Sample Number %s, Plan at 1 tile" % self.sampleNumber
        return "Longest AStar Smarty: Sample Number %s, Plan at %s tile" % (self.sampleNumber, self.planAt)
