from OneLookPlayer import OneLook
from AStarPlayer import AStar
from TrialPlayer import TrialPlayer
from Util import BananagramsUtil as util


# one look player that plays the shortest word available
class ShortestOneLook(OneLook):
    # what should return when printed
    def __str__(self):
        return "Shortest Word One Look"

    # evaluate play/state
    def heuristic(self, play):
        return -len(play[0])  # return length of word

# a shortest A* or Thinker would be trivial because
# it would always opt to do nothing over playing.
