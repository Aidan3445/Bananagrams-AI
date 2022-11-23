from abc import ABC

from AIPlayer import AIPlayer
from TrialPlayer import TrialPlayer
from Util import BananagramsUtil as util


# abstract class for all ThinkAhead players
class SmartPlayer(TrialPlayer, ABC):
    # params: number of samples to take for peel/dump, number of tiles in hand to sample at
    def __init__(self, sampleNumber, planAt):
        super().__init__(sampleNumber)
        self.planAt = planAt

    # play quickly until down to few tiles and then think real hard
    def play(self):
        if util.countTiles(self.hand) <= self.planAt:
            super().play()
        else:
            super(TrialPlayer, self).play()
            self.resetView()
        if util.countTiles(self.hand) == 0:
            self.game.peel(self)

