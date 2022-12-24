from abc import abstractmethod, ABC
from game.AIPlayer import AIPlayer
from game.Util import BananagramsUtil as util


# abstract class for a player that only looks one move at a time (max depth = 1)
class OneLook(AIPlayer, ABC):
    @abstractmethod
    # heuristic for to evaluate plays
    # params: play to evaluate
    def heuristic(self, play):
        pass

    # nextMove algorithm to choose move
    # params: board to play on, hand to play from
    def nextMoves(self, board, hand):
        allPlays = util.getAllPlays(board, hand)
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

