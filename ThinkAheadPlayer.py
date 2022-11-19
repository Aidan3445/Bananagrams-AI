from abc import abstractmethod, ABC
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util


# abstract class for all ThinkAhead players
class ThinkAheadPlayer(AIPlayer, ABC):

    def __int__(self, sampleNumber):
        super().__init__()
        self.sampleNumber = sampleNumber

    @abstractmethod
    def sampleHeuristic(self, board):
        pass

    # make a move on a given board and evaluate resulting board
    def sampleMove(self, board, hand):
        sampleMoves = self.nextMoves()

        for move in sampleMoves:
            connect, _ = move
            if connect is None:
                self.noMoves()
                return  # no plays left
            self.wordCount += 1
            board, hand = util.makeMove(move, board, hand)

        return self.sampleHeuristic(board), board, hand  # ThinkAheadPlayers use board to evaluate heuristic

    # peels on a copy of the state and finds average evaluation over given sample size
    def samplePeel(self):
        if self.sampleNumber == 0:
            return float("-inf")
        peelOdds = self.game.calcPeelOdds()
        total = 0

        for s in range(self.sampleNumber):
            sampleHand = self.hand
            sampleBoard = self.board.copy()

            peel = util.getRandomTile(self.game.tilePool)
            if peel in self.hand:
                self.hand[peel] += 1
            else:
                self.hand[peel] = 1

            total += self.sampleMove(sampleBoard, sampleHand)[0]

        return (total / self.sampleNumber) * peelOdds

    # dumps on copy of the state and finds average evaluation over given sample size
    def sampleDump(self):
        if self.sampleNumber == 0:
            return float("-inf")
        total = 0

        for s in range(self.sampleNumber):
            sampleHand = self.hand
            sampleBoard = self.board.copy()

            tilePoolCopy = self.game.tilePool.copy()

            draw1, draw2 = util.pullTile(tilePoolCopy), util.pullTile(tilePoolCopy)
            util.pullTile(sampleHand)

            for d in [draw1, draw2]:
                if d in sampleHand:
                    sampleHand[d] += 1
                else:
                    sampleHand[d] = 1

            total += self.sampleMove(sampleBoard, sampleHand)[0]

        return total / self.sampleNumber

    # play move on a copy of the state and evaluate
    def testPlay(self):
        sampleHand = self.hand.copy()
        sampleBoard = self.board.copy()

        return self.sampleMove(sampleBoard, sampleHand)

    # evaluates all possible moves by sampling and makes optimal play
    def play(self):
        peelEval = self.samplePeel()
        dumpEval = self.sampleDump()
        playEval, newBoard, newHand = self.testPlay()

        # print(playEval, dumpEval, peelEval)
        if playEval >= max(dumpEval, peelEval):  # if playing is the most optimal play
            self.board = newBoard
            self.hand = newHand
            self.resetView()
            print("chose play")

        elif dumpEval >= peelEval:  # elif dumping is the most optimal play
            self.randomDump()
            print("chose dump")

        else:
            print("chose pass")

        print()
        # otherwise, "pass" is the most optimal play
