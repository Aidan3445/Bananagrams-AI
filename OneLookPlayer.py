from abc import abstractmethod, ABC
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util


# abstract class for a player that only looks one move at a time (max depth = 1)
class OneLook(AIPlayer, ABC):
    @abstractmethod
    # heuristic for to evaluate plays
    def heuristic(self, play):
        pass

    # nextMove algorithm to choose move
    def nextMoves(self):
        allPlays = util.getAllPlays(self.board, self.hand)
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

    # behaviour when no moves are found
    def noMoves(self):
        if util.countTiles(self.hand) == 0:
            self.game.peel(self)
        else:
            self.randomDump()
