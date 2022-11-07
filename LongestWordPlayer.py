from OneLookPlayer import OneLook
from AStarPlayer import AStar
from Util import BananagramsUtil as util
from SimpleDictOneLookPlayer import SimpleDictOneLook


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


# one look player using simple dictionary that finds the longest word available
class LongestSimpleDictOneLook(SimpleDictOneLook):
    # what should return when printed
    def __str__(self):
        return "Longest Word One Look"

    # evaluate play/state
    def heuristic(self, play):
        return len(play[0])  # return length of word