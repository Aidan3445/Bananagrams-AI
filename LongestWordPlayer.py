from OneLookPlayer import OneLook
from AStarPlayer import AStar
from ThinkAheadPlayer import ThinkAheadPlayer
from Util import BananagramsUtil as util


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
    def __init__(self, maxDepth=0):
        super().__init__()
        self.maxDepth = maxDepth

    def __str__(self):
        return "Longest Word A*"

    # A* heuristics take in states, not plays params: state to evaluate
    def heuristic(self, state):  # this should guess the number of words left
        return util.countTiles(state.hand)


class LongestOneLookThinker(ThinkAheadPlayer, LongestOneLook):
    def __init__(self, sampleNumber):
        super().__init__()
        self.sampleNumber = sampleNumber

    def sampleHeuristic(self, board):
        print(util.boardToString(board), "evaluating...", end="   ")
        words = util.check(board)[0]
        wordCount = len(words)
        total = 0
        for w in words:
            total += len(w)
        print("done evaluating:", total / wordCount)
        return total / wordCount

    def __str__(self):
        return "Longest One-Look Thinker"
