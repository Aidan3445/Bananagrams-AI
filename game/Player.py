from abc import ABC, abstractmethod
import random

import pygame as pg
from game.Util import BananagramsUtil as util


class Player(ABC):
    # constructor for an abstract player's Bananagrams board
    def __init__(self):
        self.screen = 1000  # screen width
        self.scale = 8  # number of tiles across screen
        self.size = int(self.screen / self.scale)  # size of each tile
        self.board = {}  # dictionary representation of the board -- (x, y): "letter"
        self.hand = {}  # dictionary representation of the player's hand -- "letter": count
        self.center = (0, 0)  # coordinate of tile in center of screen (initial: origin)
        self.dir = (-1, 0)  # direction vector (initial: right)
        self.game = None
        self.boardScreen = pg.Surface((self.screen, self.screen))  # board image
        self.playerID = random.random()

    # override equals
    def __eq__(self, other):
        if type(other) == type(self):
            return other.playerID == self.playerID
        return False

    # override hash
    def __hash__(self):
        return hash(self.playerID)

    @abstractmethod
    # what should return when printed
    def __str__(self):
        pass

    @abstractmethod
    # make next move
    # params: OPT moves to make
    def play(self, moves=None):
        pass

    # dump board and get new tiles
    # params: letter to dump from hand
    def dump(self, letter):
        if self.hand[letter] > 0 and util.countTiles(self.game.tilePool) > 1:
            self.hand[letter] -= 1  # decrease count
            for i in range(2):
                self.hand[util.pullTile(self.game.tilePool)] += 1  # pick random tile
            self.game.tilePool[letter] += 1  # add tile back to pool

    # do every frame
    # params: pos to place in the window
    def onTick(self):
        self.play()  # make move
        self.draw()
        pg.display.update()
        pg.time.Clock().tick(60)

    # add the player to the game window
    # params: position within game screen
    def draw(self):
        self.drawBoard()  # update board image
        self.drawHand()
        pg.draw.rect(self.boardScreen, "grey", self.boardScreen.get_rect(), 5)  # make frame

    # draw board view
    def drawBoard(self):
        self.boardScreen.fill("yellow")  # yellow background
        scale = int(self.scale + 1)
        for i in range(-scale, scale):  # show tiles in grid
            for j in range(-scale, scale):
                self.placeTile((i, j))  # draw the tile

    # place tile
    # params: tile position (x, y) on screen
    def placeTile(self, pos):
        origin = self.screen / 2  # center pixel of board
        x = origin - self.size * (pos[0] + 1 / 2)  # x val of top left corner of tile to draw
        y = origin - self.size * (pos[1] + 1 / 2)  # y val of top left corner of tile to draw
        color = "black"
        frame = 3
        if pos == (0, 0):  # box is red for center
            color = "red"
            frame = 0
        pg.draw.rect(self.boardScreen, color, pg.Rect(x, y, self.size, self.size), frame)
        tile = (self.center[0] + pos[0], self.center[1] + pos[1])
        if tile in self.board:  # check for tile value to draw in box
            letter = self.board[tile]
            font = pg.font.SysFont(None, self.size)
            text = font.render(letter, True, 'black')
            align = text.get_rect(center=(x + self.size / 2, y + self.size / 2))
            self.boardScreen.blit(text, align)

    # show tiles in player's hand
    def drawHand(self):
        l1 = ""
        l2 = ""
        nonZero = []
        for letter in self.hand:  # get letters in hand
            if self.hand[letter] > 0:
                nonZero.append(letter)
        count = 0
        for letter in nonZero:  # split letters and amounts in hand into two lines
            if count < len(nonZero) / 2:
                l1 += letter + ":" + str(self.hand[letter]) + "  "
            else:
                l2 += letter + ":" + str(self.hand[letter]) + "  "
            count += 1
        pg.draw.rect(self.boardScreen, "white", pg.Rect(0, self.screen * 0.9, self.screen, self.screen * 0.1))
        fontSize = int(self.screen / 20)
        font = pg.font.SysFont(None, fontSize)
        text = font.render(l1, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen - fontSize * 0.5))
        self.boardScreen.blit(text, align)  # draw line 1
        text = font.render(l2, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen - fontSize * 1.5))
        self.boardScreen.blit(text, align)  # draw line 2

    # scale the view to show more/less of the board params: +/- change in scale
    def scaleView(self, scale=0):
        self.scale += scale
        self.scale = max(5, self.scale)  # min visible is 5 x 4
        self.scale = min(25, self.scale)  # max visible is 25 x 20
        self.size = int(self.screen / self.scale)

    # what to display when the game is over
    # params: OPT true if this player won the game
    def gameOver(self, winner=False):
        if winner:
            color = "green"
        else:
            color = "black"
        fontSize = int(self.screen / 20)
        pg.draw.rect(self.boardScreen, "grey", pg.Rect(0, self.screen / 5 - fontSize, self.screen, fontSize * 2))
        font = pg.font.SysFont(None, fontSize)
        text = font.render(str(self), True, color)
        align = text.get_rect(center=(self.screen / 2, self.screen / 5))
        self.boardScreen.blit(text, align)
