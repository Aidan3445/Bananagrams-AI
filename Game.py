import random
import sys
import pygame as pg

from HumanPlayer import Human
from PeelPlayer import Peel
from DoNothingPlayer import DoNothing


class Bananagrams:
    # constructor for a game of bananagrams params: list of players, OPT:random seed
    def __init__(self, listOfPlayers, seed=None):
        if len(listOfPlayers) < 1 or len(listOfPlayers) > 4:
            raise Exception("1 - 4 players")
        self.players = listOfPlayers  # list of players in the game
        self.tilePool = {}  # pool of tiles left
        self.tileCount = 0  # number of tiles in tilePool
        self.timer = 0  # timer for game to compare players
        self.window = pg.display.set_mode((1000, 900))  # board window
        if seed is not None:
            random.seed(seed)  # random seed for consistent play

    # make a new game
    def newGame(self):
        # initial tile pool
        self.tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
                         "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
                         "W": 3, "X": 2, "Y": 3, "Z": 2}
        self.tileCount = self.countTiles()
        self.resetPlayers()

    # play current game
    def play(self):
        self.newGame()
        pg.fastevent.init()
        pg.font.init()
        while True:
            for i, p in enumerate(self.players):
                x = 500 * (i % 2)
                y = 450 * int(i / 2)
                p.onTick((x, y))
                pg.display.update()
            self.timer += 1

    # draw one tile for all players
    def peel(self):
        if self.tileCount == 0:
            return True
        for p in self.players:
            pick = self.pullTile()
            p.hand[pick] += 1
        return False

    # get the number of tiles in a dictionary params: dictionary to count
    def countTiles(self):
        cnt = 0
        for letter in self.tilePool:
            cnt += self.tilePool[letter]  # add value
        return cnt

    # pull a tile from the set params: dictionary to pull from, index to pull at
    def pullTile(self):
        cnt = 0
        index = random.randint(0, self.tileCount - 1)
        for letter in self.tilePool:
            cnt += self.tilePool[letter]
            if cnt > index:  # once count breaks index barrier letter has been found
                self.tilePool[letter] -= 1  # decrease letter count
                self.tileCount -= 1
                return letter

    # create a random starting hand params: size of hand, number of players
    def resetPlayers(self, size=20):
        # official Bananagrams tile set
        self.tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
                         "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
                         "W": 3, "X": 2, "Y": 3, "Z": 2}
        # an empty set of all letters
        emptySet = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
                    "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
                    "W": 0, "X": 0, "Y": 0, "Z": 0}
        for p in self.players:  # initialize hands and boards to empty and set player game to this game
            p.hand = emptySet.copy()
            p.board = {}
            p.game = self
        for i in range(size):  # make random drawings in order
            self.peel()

    # quit game
    @staticmethod
    def quit():
        pg.quit()
        sys.exit()


game = Bananagrams([Human(), DoNothing(), Peel()])
game.play()


