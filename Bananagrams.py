import random
import pygame as pg

from HumanPlayer import Human
from LongestWordPlayer import *
from ScrabblePlayer import *


class Bananagrams:
    # constructor for a game of bananagrams params: list of players, OPT random seed
    def __init__(self, listOfPlayers, handSize=21, seed=None, screenSize=800):
        if len(listOfPlayers) < 1 or len(listOfPlayers) > 4:
            raise Exception("1 - 4 players")
        self.players = listOfPlayers  # list of players in the game
        self.tilePool = {}  # pool of tiles left
        self.handSize = handSize
        self.timer = 0  # timer for game to compare players
        self.size = screenSize
        self.gameScreen = pg.Surface((1000, 1000))
        self.window = pg.display.set_mode((screenSize, screenSize))  # board window
        self.gameOver = False
        if seed is not None:
            random.seed(seed)  # random seed for consistent play

    # make a new game
    def newGame(self):
        self.gameOver = False
        # initial tile pool
        self.tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
                         "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
                         "W": 3, "X": 2, "Y": 3, "Z": 2}
        self.resetPlayers()
        pg.init()  # pygame setup
        pg.font.init()
        for i, p in enumerate(self.players):
            x = 500 * (i % 2)  # place board in 2x2 grid of boards in game
            y = 500 * int(i / 2)
            p.draw((x, y))
            self.window.blit(pg.transform.scale(self.gameScreen, (self.size, self.size)), (0, 0))
            pg.display.update()
        self.play()

    # play current game
    def play(self):
        order = list(range(len(self.players)))
        while not self.gameOver:  # play loop
            random.shuffle(order)
            for i in order:
                p = self.players[i]
                x = 500 * (i % 2)  # place board in 2x2 grid of boards in game
                y = 500 * int(i / 2)
                squareSize = self.size/2
                pg.draw.rect(self.window, "green",
                             pg.Rect(squareSize * (i % 2), squareSize * int(i / 2), squareSize, squareSize), 5)
                pg.display.update()
                p.onTick((x, y))  # update board
                if self.gameOver:
                    break
                self.window.blit(pg.transform.scale(self.gameScreen, (self.size, self.size)), (0, 0))
                pg.display.update()
            self.timer += 1
        while True:  # game over loop
            for event in pg.event.get():  # input event handler
                if event.type == pg.QUIT:
                    util.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.newGame()
                        pg.display.update()

    # draw one tile for all players
    def peel(self, player=None):
        for p in self.players:
            if util.countTiles(self.tilePool) < len(self.players):
                if util.countTiles(player.hand) == 0:
                    valid, invalid = util.check(player.board)
                    if not invalid:
                        print("Player", self.players.index(player) + 1, player, "Wins!")
                        print(valid)
                    else:
                        print("Player", self.players.index(player) + 1, player, "Cheated!")
                        print(invalid)
                    self.gameOver = True
                pg.display.update()
                return
            pick = util.pullTile(self.tilePool)
            p.hand[pick] += 1

    # create a random starting hand params: size of hand, number of players
    def resetPlayers(self):
        # an empty set of all letters
        emptySet = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
                    "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
                    "W": 0, "X": 0, "Y": 0, "Z": 0}
        for p in self.players:  # initialize hands and boards to empty and set player game to this game
            p.hand = emptySet.copy()
            p.board = {}
            p.game = self
        for i in range(self.handSize):  # make random drawings in order
            self.peel()


game = Bananagrams([ScrabbleOneLook(), ScrabbleAStar()])
game.newGame()
