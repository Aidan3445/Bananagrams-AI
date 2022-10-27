from abc import ABC, abstractmethod
import pygame as pg
import words.twl as words
from Util import BananagramsUtil as util


class Player(ABC):
    # constructor for an abstract player's Bananagrams board
    def __init__(self):
        self.screenW = 500  # screen width
        self.screenH = 450  # screen height
        self.scale = 8  # number of tiles across screen
        self.size = int(self.screenW / self.scale)  # size of each tile
        self.board = {}  # dictionary representation of the board
        self.hand = {}  # dictionary representation of the player's hand
        self.center = (0, 0)  # coordinate of tile in center of screen (initial: origin)
        self.dir = (-1, 0)  # direction vector (initial: right)
        self.game = None
        self.boardScreen = pg.Surface((self.screenW, self.screenH))  # board image

    # what should return when printed
    def __str__(self):
        return "USER"

    # draw board view
    def drawBoard(self):
        self.boardScreen.fill("yellow")  # yellow background
        scale = int(self.scale + 1)
        for i in range(-scale, scale):  # show tiles in scale x scale grid
            for j in range(-scale, scale):
                self.placeTile((i, j))  # draw the tile

    # place tile params: tile position (x, y) on screen
    def placeTile(self, pos):
        origin = self.screenW / 2  # center pixel of board
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
        pg.draw.rect(self.boardScreen, "white", pg.Rect(0, self.screenH - 50, self.screenW, 50))
        font = pg.font.SysFont(None, 24)
        text = font.render(l1, True, 'black')
        align = text.get_rect(center=(self.screenW / 2, self.screenH - 37.5))
        self.boardScreen.blit(text, align)  # draw line 1
        text = font.render(l2, True, 'black')
        align = text.get_rect(center=(self.screenW / 2, self.screenH - 12.5))
        self.boardScreen.blit(text, align)  # draw line 2

    # change the view params: +/- change in scale, +/- x-shift, +/- y-shift
    def changeView(self, x=0, y=0, scale=0.):
        if scale == 0:  # only one type of change at a time
            self.center = self.center = (self.center[0] + x, self.center[1] + y)
        else:
            self.scale += scale
            self.scale = max(5, self.scale)  # min visible is 5 x 4
            self.scale = min(25, self.scale)  # max visible is 25 x 20
            self.size = int(self.screenW / self.scale)

    # play a letter from your hand params: keycode of character to play
    def playLetter(self, key):
        letter = pg.key.name(key).capitalize()
        if self.hand[letter] > 0:  # check hand for typed letter
            if self.center in self.board:  # delete if space is currently used
                self.delete(self.center)
            self.board[self.center] = letter
            self.hand[letter] -= 1
            self.changeView(x=self.dir[0], y=self.dir[1])
        elif self.center in self.board:  # typed same as center
            if self.board[self.center] == letter:
                self.changeView(x=self.dir[0], y=self.dir[1])

    # delete tile params: tile (x, y) to delete
    def delete(self, tile):
        if tile not in self.board:
            deleteDir = (abs(self.dir[0]), abs(self.dir[1]))
            back = (tile[0] + deleteDir[0], tile[1] + deleteDir[1])
            if back in self.board:  # if tile not in board check tile in reverse of self.dir
                letter = self.board[back]
                self.board.pop(back)
                self.hand[letter] += 1
                self.changeView(x=deleteDir[0], y=deleteDir[1])
        else:
            letter = self.board[tile]
            self.board.pop(tile)
            self.hand[letter] += 1

    # dump board and get new tiles
    def dump(self):
        # TODO: add dump per bananagrams rules
        pass

    # check board for valid words
    def check(self):
        # TODO: add check for islands
        invalid = []
        valid = []
        firstTiles = self.getFirstTiles()
        for tile in firstTiles:  # check each word starting from the found firstTiles
            x, y = firstTiles[tile]
            if x == 1:  # check across word
                word = self.board[tile]
                nextTile = (tile[0] - 1, tile[1])
                while nextTile in self.board:  # build word
                    word += self.board[nextTile]
                    nextTile = (nextTile[0] - 1, nextTile[1])
                if words.check(word.lower()):
                    valid.append(word)
                else:
                    invalid.append(word)
            if y == 1:  # check down word
                word = self.board[tile]
                nextTile = (tile[0], tile[1] - 1)
                while nextTile in self.board:  # build word
                    word += self.board[nextTile]
                    nextTile = (nextTile[0], nextTile[1] - 1)
                if words.check(word.lower()):
                    valid.append(word)
                else:
                    invalid.append(word)
        if invalid:
            print("Invalid Words:", invalid)
        else:
            print("All", len(valid), "words are valid!")
            if util.countTiles(self.hand) == 0:
                print("PEEL!")
                self.game.peel()

    # get a dictionary of the tiles that are the first letter of each word and the direction
    def getFirstTiles(self):
        firstTiles = {}
        for tile in self.board:
            x, y = tile
            isH = 0  # is the start of a word that goes horizontally
            isV = 0  # is the start of a word that goes vertically
            if not (x + 1, y) in self.board and (x - 1, y) in self.board:
                isH = 1
            if not (x, y + 1) in self.board and (x, y - 1) in self.board:
                isV = 1
            directions = (isH, isV)
            if directions != (0, 0):
                firstTiles[tile] = directions
        return firstTiles

    # do every frame params: pos to place in the window
    def onTick(self, pos):
        self.play()
        self.drawBoard()
        self.drawHand()
        pg.draw.rect(self.boardScreen, "grey", self.boardScreen.get_rect(), 5)  # frame
        align = self.boardScreen.get_rect(topleft=pos)
        self.game.gameScreen.blit(self.boardScreen, align)
        pg.display.update()
        pg.time.Clock().tick(60)

    # player game logic
    @abstractmethod
    def play(self):
        pass


