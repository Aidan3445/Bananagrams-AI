from Util import BananagramsUtil
from Player import Player
import pygame as pg
import numpy as np


class Human(Player):
    # what should return when printed
    def __str__(self):
        return "Human"

    # take user input for play
    def play(self):
        for event in pg.fastevent.get():  # input event handler
            if event.type == pg.QUIT:
                BananagramsUtil.quit()
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
                    # print(BananagramsUtil.getWordPlays(self.board))
                    self.check()
            elif event.type == pg.MOUSEWHEEL:
                self.scaleView(1 * -np.sign(event.y))
            pg.display.update()
