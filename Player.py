from abc import ABC, abstractmethod
import random

import pygame as pg
from Util import BananagramsUtil as util


class Player(ABC):
    # constructor for an abstract player's Bananagrams board
    def __init__(self):
        self.screen = 500  # screen width
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

    def __hash__(self):
        return hash(self.playerID)

    @abstractmethod
    # what should return when printed
    def __str__(self):
        pass

    @abstractmethod
    # make next move
    def play(self):
        pass

    # play a letter from your hand params: letter to play
    def playLetter(self, letter):
        if self.hand[letter] > 0:  # check hand for typed letter
            if self.center in self.board:  # delete if space is currently used
                self.delete()
            self.board[self.center] = letter
            self.hand[letter] -= 1
            self.shiftView(x=self.dir[0], y=self.dir[1])
        elif self.center in self.board:  # typed same as center
            if self.board[self.center] == letter:
                self.shiftView(x=self.dir[0], y=self.dir[1])

    # delete tile
    def delete(self):
        if self.center not in self.board:
            deleteDir = (abs(self.dir[0]), abs(self.dir[1]))  # if tile not in board check tile in reverse of self.dir
            back = (self.center[0] + deleteDir[0], self.center[1] + deleteDir[1])
            if back in self.board:
                letter = self.board[back]
                self.board.pop(back)
                self.hand[letter] += 1
                self.shiftView(x=deleteDir[0], y=deleteDir[1])
                return letter
        else:
            letter = self.board[self.center]  # if tile is occupied, delete it
            self.board.pop(self.center)
            self.hand[letter] += 1
            return letter

    # dump board and get new tiles params: letter to dump from hand
    def dump(self, letter):
        if self.hand[letter] > 0:
            self.hand[letter] -= 1  # decrease count
            for i in range(2):
                if util.countTiles(self.game.tilePool) > 0:
                    self.hand[util.pullTile(self.game.tilePool)] += 1  # pick random tile
            self.game.tilePool[letter] += 1  # add tile back to pool

    # do every frame params: pos to place in the window
    def onTick(self, pos=None):
        self.play()  # make move
        if pos is not None:
            self.draw(pos)
            pg.display.update()
            pg.time.Clock().tick(60)

    # add the player to the game window
    def draw(self, pos):
        self.drawBoard()  # update board image
        self.drawHand()
        pg.draw.rect(self.boardScreen, "grey", self.boardScreen.get_rect(), 5)  # make frame
        align = self.boardScreen.get_rect(topleft=pos)
        self.game.gameScreen.blit(self.boardScreen, align)

    # draw board view
    def drawBoard(self):
        self.boardScreen.fill("yellow")  # yellow background
        scale = int(self.scale + 1)
        for i in range(-scale, scale):  # show tiles in scale x scale grid
            for j in range(-scale, scale):
                self.placeTile((i, j))  # draw the tile

    # place tile params: tile position (x, y) on screen
    def placeTile(self, pos):
        origin = self.screen / 2  # center pixel of board
        x = origin - self.size * (pos[0] + 1 / 2)  # x val of top left corner of tile to draw
        y = origin - self.size * (pos[1] + 1 / 2)  # y val of top left corner of tile to draw
        color = "black"
        if pos == (0, 0):  # box is red for center
            color = "red"
        pg.draw.rect(self.boardScreen, color, pg.Rect(x, y, self.size, self.size), 2)
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
        pg.draw.rect(self.boardScreen, "white", pg.Rect(0, self.screen - 50, self.screen, 50))
        font = pg.font.SysFont(None, 24)
        text = font.render(l1, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen - 37.5))
        self.boardScreen.blit(text, align)  # draw line 1
        text = font.render(l2, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen - 12.5))
        self.boardScreen.blit(text, align)  # draw line 2

    # shift the view params: OPT +/- x-shift, OPT +/- y-shift
    def shiftView(self, x=0, y=0):
        self.center = (self.center[0] + x, self.center[1] + y)

    # scale the view to show more/less of the board params: +/- change in scale
    def scaleView(self, scale=0):
        self.scale += scale
        self.scale = max(5, self.scale)  # min visible is 5 x 4
        self.scale = min(25, self.scale)  # max visible is 25 x 20
        self.size = int(self.screen / self.scale)
