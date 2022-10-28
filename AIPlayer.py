from abc import abstractmethod, ABC

from Player import Player
import words.twl as words


class AIPlayer(Player, ABC):
    # convert board tiles to single string
    def handToString(self):
        handString = ""
        for letter in self.hand:
            letter.lower() * self.hand[letter]  # add letters to string
        return handString

    @abstractmethod
    # heuristic for to evaluate states
    def heuristic(self):
        pass

    # aStar algorithm to choose move
    def aStar(self):
        return (0, 0), (1, 0), ""

    # evaluate and make next move
    def play(self):
        self.center, self.dir, word = self.aStar()
        for letter in word:
            self.playLetter(letter)


