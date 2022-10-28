from Player import Player


class DoNothing(Player):
    # what should return when printed
    def __str__(self):
        return "Do Nothing Bot"

    # a player that does nothing
    def play(self):
        pass
