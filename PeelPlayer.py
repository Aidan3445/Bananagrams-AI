from Player import Player


class Peel(Player):
    # a player that peels
    def play(self):
        self.game.peel()
