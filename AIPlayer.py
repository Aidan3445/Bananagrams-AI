from abc import abstractmethod, ABC
from Player import Player
from Util import BananagramsUtil as util
import pygame as pg


# abstract class for all AI players
class AIPlayer(Player, ABC):
    def __init__(self):
        super().__init__()
        self.wordCount = 0

    @abstractmethod
    # heuristic for to evaluate a state or a play
    def heuristic(self, toEval):
        pass

    @abstractmethod
    # nextMove algorithm to choose move
    def nextMoves(self):
        pass

    # behaviour when no moves are found
    def noMoves(self):
        if util.countTiles(self.hand) == 0:
            self.game.peel(self)
        else:
            self.randomDump()

    # dump a random letter
    def randomDump(self):
        letter = util.getRandomTile(self.hand)
        self.dump(letter)

    # evaluate and make next move
    def play(self):
        moves = self.nextMoves()  # tile to connect to, play to make off that tile
        for move in moves:
            connect, play = move
            if connect is None:
                self.noMoves()
                return  # no plays left
            self.wordCount += 1
            word, offset, direction = play
            self.center = (connect[0] - (offset * direction[0]), connect[1] - (offset * direction[1]))  # set center
            self.dir = direction  # set direction
            for letter in word:
                self.playLetter(letter)  # play word
        self.resetView()

    def resetView(self):
        left, right, top, bottom = util.getBoardArea(self.board)  # set view
        self.center = (int((left + right) / 2), int((top + bottom) / 2))
        self.scale = 1.5 * max(left - right, top - bottom)
        self.scaleView()
