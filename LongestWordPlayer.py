from OneLookPlayer import OneLook
from HumanPlayer import Human
from Util import BananagramsUtil as util


# one look player that plays the longest word available
class LongestWord(OneLook):
    # what should return when printed
    def __str__(self):
        return "Longest Word Bot"

    # evaluate play/state
    def heuristic(self, play):
        return len(play[0])

    # behaviour when no moves are found
    def noMoves(self):
        if util.countTiles(self.hand) == 0:
            self.game.peel(self)
        else:
            for letter in self.hand:
                if self.hand[letter] > 0:
                    self.dump(letter)
                    break
