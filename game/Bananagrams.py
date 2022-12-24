import random
import time
import pygame as pg
from players.HumanPlayer import Human
from game.Util import BananagramsUtil as util


class Bananagrams:
    # constructor for a game of bananagrams
    # params: OPT list of AI players, OPT size of each starting hand, OPT random seed, OPT size of screen in pixels
    def __init__(self, listOfPlayers=None, runCount=0, handSize=21, seed=None, screenSize=800):
        if listOfPlayers is None or len(listOfPlayers) < 1:
            listOfPlayers = [Human()]
            self.onlyHuman = True
        else:
            self.onlyHuman = False
        if len(listOfPlayers) < 1 or len(listOfPlayers) > 4:
            raise Exception("1 - 4 players")
        # base game
        self.players = listOfPlayers  # list of players in the game
        self.order = list(range(len(self.players)))  # the order of players to play and peel for randomization
        self.tilePool = {}  # pool of tiles left
        self.handSize = handSize
        self.gameOver = False

        # lock prevention
        self.noPeelCounter = 0

        # pygame setup
        pg.init()
        pg.font.init()
        self.size = screenSize
        if len(self.players) > 1:
            gameSize = 2000
        else:
            gameSize = 1000
        self.gameScreen = pg.Surface((gameSize, gameSize))
        self.window = pg.display.set_mode((screenSize, screenSize))  # board window

        # randomization
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 100000)
        random.seed(self.seed)  # random seed for consistent play

        # stats
        self.startTime = time.time()
        self.count = 0
        self.runs = runCount
        self.stats = {}  # TODO: replace with writing to file
        for p in self.players:
            self.stats[p] = 0  # initialize stats dictionary
        self.stats["No Winner"] = 0  # for games with no winners

    # draw a given player on the game screen
    # params: player to draw
    def drawPlayer(self, p):
        i = self.players.index(p)
        x = 1000 * (i % 2)  # place board in 2x2 grid of boards in game
        y = 1000 * int(i / 2)
        align = p.boardScreen.get_rect(topleft=(x, y))
        self.gameScreen.blit(p.boardScreen, align)

    # make a new game
    def newGame(self):
        self.gameOver = False
        if self.runs > 0:
            print("Game %s/%s:" % (self.count + 1, self.runs))
        # initial tile pool
        self.tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
                         "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
                         "W": 3, "X": 2, "Y": 3, "Z": 2}
        self.resetPlayers()
        for i, p in enumerate(self.players):
            p.draw()
            self.drawPlayer(p)
            if self.onlyHuman and self.count == 0:
                p.instructions()
            self.update()
        self.play()

    # play current game
    def play(self):
        while not self.gameOver:  # play loop
            if not self.onlyHuman:
                for event in pg.event.get():  # input event handler
                    if event.type == pg.QUIT:
                        self.quit()
            random.shuffle(self.order)  # randomize play order for this turn
            self.noPeelCounter += 1  # increase counter for no peels to end stalemate
            for i in self.order:  # loop through play order
                p = self.players[i]
                if len(self.players) > 1:  # draw green board to show which player's turn it is
                    squareSize = self.size / 2
                    pg.draw.rect(self.window, "green",
                                 pg.Rect(squareSize * (i % 2), squareSize * int(i / 2), squareSize, squareSize), 5)
                    pg.display.update()
                p.onTick()  # update board
                self.drawPlayer(p)
                if self.gameOver:
                    break
                self.update()
            # if no peels are called in the at most, the number of tiles in starting pool
            if not self.onlyHuman and self.noPeelCounter > 144 - len(self.players) * self.handSize:
                self.stats["No Winner"] += 1
                for p in self.players:
                    print(util.boardToString(p.board))
                    print("Valid: %s\nInvalid: %s" % util.check(p.board))
                print("Stalemate, No Winner")
                self.gameOver = True
        if self.runs == 0:
            while True:  # game over loop
                for event in pg.event.get():  # input event handler
                    if event.type == pg.QUIT:
                        self.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            self.newGame()
                        else:
                            for p in self.players:
                                p.draw()
                                self.drawPlayer(p)
                            self.update()
        else:
            if self.count < self.runs:
                self.newGame()
            else:
                self.quit(time.time())

    # draw one tile for all players
    # params: OPT player that called peel
    def peel(self, player=None):
        self.noPeelCounter = 0  # PEEL! reset counter
        peelOrder = self.order.copy()
        if player is not None:  # set peel order to random order with peel caller first
            if util.countTiles(self.tilePool) < len(self.players):
                if util.countTiles(player.hand) == 0:
                    valid, invalid = util.check(player.board)
                    if not invalid:
                        print("Player", self.players.index(player) + 1, player, "Wins!")
                        print(util.boardToString(player.board))
                        self.stats[player] += 1
                        print(valid)
                        self.gameOver = True
                        self.count += 1
                    else:
                        print("Player", self.players.index(player) + 1, player, "Cheated!")
                        print(util.boardToString(player.board))
                        print(invalid)
                self.drawPlayer(player)
                if self.gameOver:
                    for p in self.players:
                        p.draw()
                        if p is player:
                            p.gameOver(True)
                        else:
                            p.gameOver()
                        self.drawPlayer(p)
                    self.update()
                    return
            playerIndex = self.players.index(player)
            peelOrder.remove(playerIndex)
            peelOrder = [playerIndex] + peelOrder
        for i in peelOrder:
            p = self.players[i]
            pick = util.pullTile(self.tilePool)
            if pick in p.hand:
                p.hand[pick] += 1
            else:
                p.hand[pick] = 1
            p.drawHand()
            self.drawPlayer(p)
        self.update()

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

    # calculates odds of a peel happening based on player's hands
    def calcPeelOdds(self):
        total = 0
        for p in self.players:
            count = util.countTiles(p.hand)
            if count <= 1:
                total += 1
            else:
                total += 1 / count
        return total / len(self.players)
    
    # pygame display update
    def update(self):
        self.window.blit(pg.transform.scale(self.gameScreen, (self.size, self.size)), (0, 0))
        pg.display.update()

    # print out the recorded stats from the runs
    def quit(self, endTime=None):
        print("--------------------PLAY ENDED--------------------")
        for p in self.stats:
            print(p, "-->", self.stats[p])
        util.quit(startTime=self.startTime, endTime=endTime)
