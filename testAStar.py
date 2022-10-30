from AStarPlayer import AStar
from Util import BananagramsUtil as util


# AI players that use A* to make moves
class TestAStar(AStar):
    def __init__(self, maxDepth=0):
        super().__init__()
        self.maxDepth = maxDepth

    def __str__(self):
        return "TEST ASTAR"

    def noMoves(self):
        print("no moves")

    # A* heuristics take in states, not plays
    def heuristic(self, state):
        return len(state.board)

    # whether to terminate a search at a state
    def terminateSearch(self, state):
        return len(self.hand) - util.countTiles(state.hand) >= 10
