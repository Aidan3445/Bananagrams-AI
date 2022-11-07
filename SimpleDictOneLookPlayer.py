from abc import abstractmethod, ABC
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util
import words.twlsimple as simplewords


# abstract class for a player that only looks one move at a time (max depth = 1)
class SimpleDictOneLook(AIPlayer, ABC):
    @abstractmethod
    # heuristic for to evaluate plays
    def heuristic(self, play):
        pass

    # nextMove algorithm to choose move
    def nextMoves(self):
        allPlays = util.getAllPlays(self.board, self.hand, simplewords)
        bestH = float("-inf")
        bestPlay = None
        bestTile = None
        for tile in allPlays:
            for play in allPlays[tile]:
                h = self.heuristic(play)
                if h > bestH:  # store play info if better score
                    bestH = h
                    bestPlay = play
                    bestTile = tile
        return [(bestTile, bestPlay)]

