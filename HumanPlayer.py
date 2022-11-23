from Util import BananagramsUtil as util
from Player import Player
import pygame as pg
import numpy as np


# human player
class Human(Player):
    # what should return when printed
    def __str__(self):
        return "Human"

    # check board for valid words
    def check(self):
        valid, invalid = util.check(self.board)
        if invalid:
            print("Invalid Words:", invalid)  # print invalid words
        else:
            print("All", len(valid), "words are valid!")  # print number of valid words
            if util.countTiles(self.hand) == 0:
                print("PEEL!")
                self.game.peel(self)  # peel and test for game over

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
    def play(self):
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
            elif event.type == pg.MOUSEWHEEL:
                self.scaleView(1 * -np.sign(event.y))
            pg.display.update()
