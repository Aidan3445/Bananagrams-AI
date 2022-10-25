import sys
import random
import pygame as pg
import numpy as np
import words.twl as words

# pool of letters for this game
tilePool = {}

# an empty set of all letters
emptySet = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
            "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
            "W": 0, "X": 0, "Y": 0, "Z": 0}


# get the number of tiles in a dictionary params: dictionary to count
def countTiles(tiles):
    cnt = 0
    for letter in tiles:
        cnt += tiles[letter]  # add value
    return cnt


# pull a tile from the set params: dictionary to pull from, index to pull at
def pullTile(tiles, index):
    cnt = 0
    for letter in tiles:
        cnt += tiles[letter]
        if cnt > index:  # once count breaks index barrier letter has been found
            tiles[letter] -= 1  # decrease letter count
            return letter


# create a random starting hand params: size of hand, number of players
def startingHand(size=20, players=1):
    # official Bananagrams tile set
    tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
                "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
                "W": 3, "X": 2, "Y": 3, "Z": 2}
    hands = []
    player = 0
    for i in range(players):  # initialize hands to empty
        hands.append(emptySet.copy())
    for i in range(size * players):  # make random drawings in order
        index = random.randint(0, countTiles(tilePool) - 1)
        pick = pullTile(tilePool, index)
        hands[player][pick] += 1  # add to hand
        player = (player + 1) % players  # increment player
    return hands


# generating hand for 1 player
allHands = startingHand()


class SinglePlayer:
    # constructor for a single player's Bananagrams board params: number of players, screen size
    def __init__(self, player=0, screen=600):
        self.screen = screen  # screen size (square)
        self.scale = 8  # number of tiles across screen
        self.size = int(screen / self.scale)  # size of each tile
        self.board = {}  # dictionary representation of the board
        self.hand = allHands[player]  # dictionary representation of the player's hand
        self.center = (0, 0)  # coordinate of tile in center of screen (initial: origin)
        self.dir = (-1, 0)  # direction vector (initial: right)

        self.window = pg.display.set_mode((self.screen, self.screen + 50))  # board window

    # draw board view
    def drawBoard(self):
        self.window.fill("yellow")  # yellow background
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
        pg.draw.rect(self.window, color, pg.Rect(x, y, self.size, self.size), 2)
        tile = (self.center[0] + pos[0], self.center[1] + pos[1])
        if tile in self.board:  # check for tile value to draw in box
            letter = self.board[tile]
            font = pg.font.SysFont(None, self.size)
            text = font.render(letter, True, 'black')
            align = text.get_rect(center=(x + self.size / 2, y + self.size / 2))
            self.window.blit(text, align)

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
                l1 += letter + ": " + str(self.hand[letter]) + "  "
            else:
                l2 += letter + ": " + str(self.hand[letter]) + "  "
            count += 1
        pg.draw.rect(self.window, "white", pg.Rect(0, self.screen, self.screen, 50))
        font = pg.font.SysFont(None, 25)
        text = font.render(l1, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen + 12.5))
        self.window.blit(text, align)  # draw line 1
        text = font.render(l2, True, 'black')
        align = text.get_rect(center=(self.screen / 2, self.screen + 37.5))
        self.window.blit(text, align)  # draw line 2

    # change the view params: +/- change in scale, +/- x-shift, +/- y-shift
    def changeView(self, x=0, y=0, scale=0.):
        if scale == 0:  # only one type of change at a time
            self.center = self.center = (self.center[0] + x, self.center[1] + y)
        else:
            self.scale += scale
            self.scale = max(5, self.scale)  # min visible is 5 x 5
            self.size = int(self.screen / self.scale)

    # play a letter from your hand params: keycode of character to play
    def playLetter(self, key):
        letter = pg.key.name(key).capitalize()
        if self.hand[letter] > 0:  # check hand for typed letter
            if self.center in self.board:  # delete if space is currently used
                self.delete(self.center)
            self.board[self.center] = letter
            self.hand[letter] -= 1
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

    # do every frame
    def onTick(self):
        self.drawBoard()
        self.drawHand()

    # pygame run loop
    def play(self):
        pg.init()
        pg.font.init()
        while True:  # play loop
            for event in pg.event.get():  # input event handler
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    k = event.key
                    if k == pg.K_RIGHT:
                        self.changeView(x=-1)
                        self.dir = (-1, 0)
                    elif k == pg.K_DOWN:
                        self.changeView(y=-1)
                        self.dir = (0, -1)
                    elif k == pg.K_UP:
                        self.changeView(y=1)
                    elif k == pg.K_LEFT:
                        self.changeView(x=1)
                    elif 97 <= k <= 122:  # range of letter keys only
                        self.playLetter(k)
                    elif k == pg.K_BACKSPACE:
                        self.delete(self.center)
                    elif k == pg.K_RETURN:
                        self.check()
                    elif k == pg.K_SPACE:
                        self.hand = startingHand()[0]
                        self.board = {}
                elif event.type == pg.MOUSEWHEEL:
                    self.changeView(scale=1 * -np.sign(event.y))
                pg.display.update()

            self.onTick()
            pg.display.update()
            pg.time.Clock().tick(60)


game = SinglePlayer()
game.play()
