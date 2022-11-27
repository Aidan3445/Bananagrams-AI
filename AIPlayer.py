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
    # params: state or play to evaluate
    def heuristic(self, toEval):
        pass

    @abstractmethod
    # nextMove algorithm to choose move
    # params: board to play on, hand to play from
    def nextMoves(self, board, hand):
        pass

    # behaviour when no moves are found
    def noMoves(self):
        if util.countTiles(self.hand) == 0:
            self.game.peel(self)
        else:
            self.dumpLogic()

    # default is dump a random letter
    def dumpLogic(self):
        letter = util.getRandomTile(self.hand)
        self.dump(letter)

    # evaluate and make next move
    def play(self):
        moves = self.nextMoves(self.board, self.hand)  # tile to connect to, play to make off that tile
        for move in moves:
            if None in move:
                self.noMoves()
                return  # no plays left
            self.wordCount += 1
            self.board, self.hand = util.makeMove(move, self.board, self.hand)
        self.resetView()

    def resetView(self):
        left, right, top, bottom = util.getBoardArea(self.board)  # set view
        self.center = (int((left + right) / 2), int((top + bottom) / 2))
        self.scale = 1.5 * max(left - right, top - bottom)
        self.scaleView()
