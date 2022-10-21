import sys
import pygame as pg
import numpy as np
import words.twl as words

tilePool = {"A": 13, "B": 3, "C": 3, "D": 6, "E": 18, "F": 3, "G": 4, "H": 3, "I": 12, "J": 2, "K": 2,
            "L": 5, "M": 3, "N": 8, "O": 11, "P": 3, "Q": 2, "R": 9, "S": 6, "T": 9, "U": 6, "V": 3,
            "W": 3, "X": 2, "Y": 3, "Z": 2}


class Bananagrams:
    # constructor params: number of players, screen size
    def __init__(self, players=1, screen=600):
        self.p = players  # number of players
        self.screen = screen  # screen size (square)
        self.scale = 8  # number of tiles across screen
        self.size = int(screen / self.scale)  # size of each tile
        self.board = {}  # dictionary representation of the board
        self.hand = tilePool  # dictionary representation of the player's hand
        self.center = (0, 0)  # coordinate of tile in center of screen (initial: origin)
        self.dir = (-1, 0)  # direction vector (initial: right)

        self.window = pg.display.set_mode((self.screen, self.screen))  # board window

    # draw board view
    def draw(self):
        self.scale = max(5, self.scale)
        self.size = int(self.screen / self.scale)
        self.window.fill("white")
        scale = int(self.scale + 1)
        x0 = self.center[0]
        y0 = self.center[1]
        for i in range(-scale, scale):
            for j in range(-scale, scale):
                self.placeTile((i, j))

    # place tile params: tile position (x, y) on screen
    def placeTile(self, pos):
        origin = self.screen / 2
        x = origin - self.size * (pos[0] + 1 / 2)
        y = origin - self.size * (pos[1] + 1 / 2)
        color = "black"
        if pos == (0, 0):
            color = "yellow"
        pg.draw.rect(self.window, color, pg.Rect(x, y, self.size, self.size), 1)
        tile = (self.center[0] + pos[0], self.center[1] + pos[1])
        if tile in self.board:
            letter = self.board[tile]
            font = pg.font.SysFont(None, self.size)
            text = font.render(letter, True, 'black')
            align = text.get_rect(center=(x + self.size / 2, y + self.size / 2))
            self.window.blit(text, align)

    # change the view params: +/- change in scale, +/- x-shift, +/- y-shift
    def changeView(self, scale=0., x=0, y=0):
        self.scale += scale
        if scale == 0:
            self.center = self.center = (self.center[0] + x, self.center[1] + y)

    # play a letter from your hand params: keycode of character to play
    def playLetter(self, key):
        letter = pg.key.name(key).capitalize()
        if self.hand[letter] > 0:
            self.board[self.center] = letter
            self.hand[letter] -= 1
            self.changeView(x=self.dir[0], y=self.dir[1])

    # delete tile params: tile (x, y) to delete
    def delete(self, tile):
        if tile not in self.board:
            deleteDir = (abs(self.dir[0]), abs(self.dir[1]))
            back = (tile[0] + deleteDir[0], tile[1] + deleteDir[1])
            if back in self.board:
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
        return

    # do every frame
    def onTick(self):
        self.draw()

    # pygame run loop
    def play(self):
        pg.init()
        pg.font.init()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    k = event.key
                    if k == pg.K_RIGHT:
                        self.changeView(x=-1)
                        self.dir = (-1, 0)
                    elif k == pg.K_UP:
                        self.changeView(y=1)
                    elif k == pg.K_LEFT:
                        self.changeView(x=1)
                    elif k == pg.K_DOWN:
                        self.changeView(y=-1)
                        self.dir = (0, -1)
                    elif 97 <= k <= 122:
                        self.playLetter(k)
                    elif k == pg.K_BACKSPACE:
                        self.delete(self.center)
                    elif k == pg.K_RETURN:
                        self.check()
                elif event.type == pg.MOUSEWHEEL:
                    self.changeView(scale=1 * -np.sign(event.y))

                pg.display.update()

            self.onTick()
            pg.display.update()
            pg.time.Clock().tick(60)


game = Bananagrams()
game.play()
