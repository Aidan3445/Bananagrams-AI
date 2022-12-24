from game.Util import BananagramsUtil as util
from game.Player import Player
import pygame as pg
import numpy as np
import time


# human player
class Human(Player):
    def __init__(self):
        super().__init__()
        self.playerID = -1  # unique negative ID

    # what should return when printed
    def __str__(self):
        return "Human"

    # check board for valid words
    def check(self):
        valid, invalid = util.check(self.board)
        display = []
        if invalid:
            print("Invalid Words:", invalid)  # print invalid words
            for i in invalid:
                display += [i]
            self.displayWords(display, prefix="Invalid Words: ")
        else:
            print("All", len(valid), "words are valid!")  # print number of valid words
            for i in valid:
                display += [i]
            self.displayWords(display, prefix="All Words Valid: ")
            if util.countTiles(self.hand) == 0:
                print("PEEL!")
                self.game.peel(self)  # peel and test for game over
                self.displayWords([], prefix="PEEL!", delay=1)

    # Display a list of words on the board for a given number of seconds
    # params: list of words to display, prefix to put before the first line, time to display
    def displayWords(self, display, prefix="", delay=2):
        lines = [""] * 3
        lines[0] += prefix
        charLimit = 30
        lineCounter = 0
        for word in display:
            if len(lines[lineCounter]) > charLimit:
                lineCounter += 1
            else:
                lines[lineCounter] += " "
            lines[lineCounter] += word.title()
        l1, l2, l3 = lines
        fontSize = int(self.screen / 20)
        pg.draw.rect(self.boardScreen, "grey", pg.Rect(0, self.screen / 5, self.screen, fontSize * 3))
        font = pg.font.SysFont(None, fontSize)
        text = font.render(l1, True, "black")
        align = text.get_rect(center=(self.screen / 2, self.screen / 5 + fontSize * 0.5))
        self.boardScreen.blit(text, align)  # draw line 1
        font = pg.font.SysFont(None, fontSize)
        text = font.render(l2, True, "black")
        align = text.get_rect(center=(self.screen / 2, self.screen / 5 + fontSize * 1.5))
        self.boardScreen.blit(text, align)  # draw line 2
        font = pg.font.SysFont(None, fontSize)
        text = font.render(l3, True, "black")
        align = text.get_rect(center=(self.screen / 2, self.screen / 5 + fontSize * 2.5))
        self.boardScreen.blit(text, align)  # draw line 3
        self.game.drawPlayer(self)
        self.game.update()
        time.sleep(delay)

    # display instructions to play
    def instructions(self):
        self.displayWords(["Type/Delete to play,  ", "Arrows to move,  ", "Scroll to zoom,  ",
                           "Return to check,  ", "Space to dump selection,  ", "Tab to show instructions"], delay=5)

    # play a letter from your hand
    # params: letter to play
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
            deleteDir = abs(self.dir[0]), abs(self.dir[1])  # if tile not in board check tile in reverse of self.dir
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

    # shift the view params: OPT +/- x-shift, OPT +/- y-shift
    def shiftView(self, x=0, y=0):
        self.center = (self.center[0] + x, self.center[1] + y)

    # take user input for play
    def play(self, moves=None):
        for event in pg.event.get():  # input event handler
            if event.type == pg.QUIT:
                util.quit()
            if event.type == pg.KEYDOWN:
                k = event.key
                if k == pg.K_RIGHT:
                    self.shiftView(x=-1)
                    self.dir = (-1, 0)
                elif k == pg.K_DOWN:
                    self.shiftView(y=-1)
                    self.dir = (0, -1)
                elif k == pg.K_LEFT:
                    self.shiftView(x=1)
                    self.dir = (-1, 0)
                elif k == pg.K_UP:
                    self.shiftView(y=1)
                    self.dir = (0, -1)
                elif 97 <= k <= 122:  # range of letter keys only
                    letter = pg.key.name(k).capitalize()
                    self.playLetter(letter)
                elif k == pg.K_BACKSPACE:
                    self.delete()
                elif k == pg.K_SPACE:
                    if self.center in self.board:
                        letter = self.delete()
                        if letter is not None:
                            self.dump(letter)
                elif k == pg.K_RETURN:
                    self.check()
                elif k == pg.K_TAB:
                    self.instructions()
            elif event.type == pg.MOUSEWHEEL:
                self.scaleView(1 * -np.sign(event.y))
            pg.display.update()
