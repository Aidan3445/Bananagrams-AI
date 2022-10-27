import sys
import random
import pygame as pg
import tkinter as tk


class BananagramsUtil:
    # quit game
    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    # get the number of tiles in a dictionary params: dictionary to count
    @staticmethod
    def countTiles(tileSet):
        cnt = 0
        for letter in tileSet:
            cnt += tileSet[letter]  # add value
        return cnt

    # pull a tile from the set params: dictionary to pull from
    @staticmethod
    def pullTile(tileSet):
        cnt = 0
        index = random.randint(0, BananagramsUtil.countTiles(tileSet) - 1)
        for letter in tileSet:
            cnt += tileSet[letter]
            if cnt > index:  # once count breaks index barrier letter has been found
                tileSet[letter] -= 1  # decrease letter count
                return letter
