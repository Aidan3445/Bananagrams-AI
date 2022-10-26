import sys
from Player import Player
import pygame as pg
import numpy as np


class Human(Player):
    # take user input for play
    def play(self):
        for event in pg.fastevent.get():  # input event handler
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                k = event.key
                if k == pg.K_RIGHT:
                    self.changeView(x=-1)
                    self.dir = (-1, 0)
                elif k == pg.K_DOWN:
                    self.changeView(y=-1)
                    self.dir = (0, -1)
                elif k == pg.K_LEFT:
                    self.changeView(x=1)
                    self.dir = (-1, 0)
                elif k == pg.K_UP:
                    self.changeView(y=1)
                    self.dir = (0, -1)
                elif 97 <= k <= 122:  # range of letter keys only
                    self.playLetter(k)
                elif k == pg.K_BACKSPACE:
                    self.delete(self.center)
                elif k == pg.K_SPACE:
                    if self.game.peel():
                        print(self, "wins")
                elif k == pg.K_RETURN:
                    self.check()
            elif event.type == pg.MOUSEWHEEL:
                self.changeView(scale=1 * -np.sign(event.y))
            pg.display.update()
