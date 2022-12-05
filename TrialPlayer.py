from abc import abstractmethod, ABC
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util


# abstract class for all ThinkAhead players
class TrialPlayer(AIPlayer, ABC):

    def __init__(self, sampleNumber):
        super().__init__()
        if sampleNumber == 0:
            raise Exception("Sample number of 0 is the same as a normal", self)
        if sampleNumber < 0:
            raise Exception("Sample number must be at least 1.")
        self.sampleNumber = sampleNumber

    @abstractmethod
    # heuristic for the sample play
    # params: board to evaluate heuristic on
    def sampleHeuristic(self, board):
        pass

    # make a move on a given board and evaluate resulting board
    # params: board and hand to make sample moves on
    def sampleMove(self, board, hand):
        sampleMoves = self.nextMoves(board, hand)

        for move in sampleMoves:
            if None in move:  # no plays
                return float("-inf"), board, hand
            board, hand = util.makeMove(move, board, hand)
        return self.sampleHeuristic(board), board, hand  # ThinkAheadPlayers use board to evaluate heuristic

    # peels on a copy of the state and finds average evaluation over given sample size
    def samplePeel(self):
        peelOdds = self.game.calcPeelOdds()
        total = 0
        samples = {}
        for s in range(self.sampleNumber):
            sampleHand = self.hand.copy()
            sampleBoard = self.board.copy()
            peel = util.getRandomTile(self.game.tilePool)
            if peel in samples:
                total += samples[peel]
            else:
                if peel in sampleHand:
                    sampleHand[peel] += 1
                else:
                    sampleHand[peel] = 1
                score, _, _ = self.sampleMove(sampleBoard, sampleHand)
                samples[peel] = score
                total += score
        return (total / self.sampleNumber) * peelOdds

    # dumps on copy of the state and finds average evaluation over given sample size
    def sampleDump(self):
        total = 0
        samples = {}
        for s in range(self.sampleNumber):
            sampleHand = self.hand.copy()
            sampleBoard = self.board.copy()
            tilePoolCopy = self.game.tilePool.copy()
            draw1, draw2 = util.pullTile(tilePoolCopy), util.pullTile(tilePoolCopy)
            dump = util.pullTile(sampleHand)
            sample = (dump, draw1, draw2)
            if sample in samples:
                total += samples[sample]
            else:
                for d in [draw1, draw2]:
                    if d in sampleHand:
                        sampleHand[d] += 1
                    else:
                        sampleHand[d] = 1
                score, _, sampleHand = self.sampleMove(sampleBoard, sampleHand)
                samples[sample] = score
                total += score
        return total / self.sampleNumber

    # play move on a copy of the state and evaluate
    def testPlay(self):
        sampleHand = self.hand.copy()
        sampleBoard = self.board.copy()
        score, sampleBoard, sampleHand = self.sampleMove(sampleBoard, sampleHand)
        if util.countTiles(sampleHand) + util.countTiles(self.game.tilePool) == 0:
            return float("inf"), sampleBoard, sampleHand
        return score, sampleBoard, sampleHand

    # evaluates all possible moves by sampling and makes optimal play
    def play(self):
        if len(self.game.players) > 1 and len(self.game.tilePool) > 0:
            peelEval = self.samplePeel()
        else:
            peelEval = float("-inf")
        if util.countTiles(self.hand) > 0 and util.countTiles(self.game.tilePool) > 1:
            dumpEval = self.sampleDump()
        else:
            dumpEval = float("-inf")
        playEval, newBoard, newHand = self.testPlay()
        if playEval >= max(dumpEval, peelEval):  # if playing is the most optimal play
            if playEval == float("-inf"):  # no moves found
                self.noMoves()
            else:
                self.board = newBoard
                self.hand = newHand
                self.resetView()
        elif dumpEval >= peelEval:  # elif dumping is the most optimal play
            self.noMoves()
            super().play()
        if util.countTiles(self.hand) == 0:
            self.noMoves()
        # otherwise, "pass" is the most optimal play
