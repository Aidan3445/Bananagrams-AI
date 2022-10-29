from abc import abstractmethod, ABC
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util


# abstract class for a player that only looks one move at a time (max depth = 1)
class OneLook(AIPlayer, ABC):
    @abstractmethod
    # heuristic for to evaluate states
    def heuristic(self, play):
        pass

    # nextMove algorithm to choose move
    def nextMove(self):
        allPlays = util.getAllPlays(self.board, self.hand)
        bestH = float("-inf")
        bestPlay = None
        bestTile = None
        for tile in allPlays:
            for play in allPlays[tile]:
                h = self.heuristic(play)
                if h > bestH:
                    bestH = h
                    bestPlay = play
                    bestTile = tile
        return bestTile, bestPlay
