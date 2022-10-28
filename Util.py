import sys
import random
import pygame as pg
import words.twl as words


class BananagramsUtil:
    @staticmethod
    # quit game
    def quit():
        pg.quit()
        sys.exit()

    @staticmethod
    # get the number of tiles in a dictionary params: dictionary to count
    def countTiles(tileSet):
        cnt = 0
        for letter in tileSet:
            cnt += tileSet[letter]  # add value
        return cnt

    @staticmethod
    # pull a tile from the set params: dictionary to pull from
    def pullTile(tileSet):
        cnt = 0
        index = random.randint(0, BananagramsUtil.countTiles(tileSet) - 1)
        for letter in tileSet:
            cnt += tileSet[letter]
            if cnt > index:  # once count breaks index barrier letter has been found
                tileSet[letter] -= 1  # decrease letter count
                return letter

    @staticmethod
    # check board for valid words params: board to check
    def check(board):
        # TODO: add check for islands
        invalid = []
        valid = []
        firstTiles = BananagramsUtil.getFirstTiles(board)
        for tile in firstTiles:  # check each word starting from the found firstTiles
            x, y = firstTiles[tile]
            if x == 1:  # check across word
                word = board[tile]
                nextTile = (tile[0] - 1, tile[1])
                while nextTile in board:  # build word
                    word += board[nextTile]
                    nextTile = (nextTile[0] - 1, nextTile[1])
                if words.check(word.lower()):
                    valid.append(word)
                else:
                    invalid.append(word)
            if y == 1:  # check down word
                word = board[tile]
                nextTile = (tile[0], tile[1] - 1)
                while nextTile in board:  # build word
                    word += board[nextTile]
                    nextTile = (nextTile[0], nextTile[1] - 1)
                if words.check(word.lower()):
                    valid.append(word)
                else:
                    invalid.append(word)
        return valid, invalid

    @staticmethod
    # get a dictionary of the tiles that are the first letter of each word and the direction params: board to search
    def getFirstTiles(board):
        firstTiles = {}
        for tile in board:
            x, y = tile
            isH = 0  # is the start of a word that goes horizontally
            isV = 0  # is the start of a word that goes vertically
            if not (x + 1, y) in board and (x - 1, y) in board:
                isH = 1
            if not (x, y + 1) in board and (x, y - 1) in board:
                isV = 1
            directions = (isH, isV)
            if directions != (0, 0):
                firstTiles[tile] = directions
        return firstTiles

    @staticmethod
    # get the playable spots for a board params: board to search
    def getPlayableSpots(board):
        across = {}
        down = {}
        firstTiles = BananagramsUtil.getFirstTiles(board)
        for tile in firstTiles:
            x, y = firstTiles[tile]
            if x == 1:  # is across
                word = ""
                nextTile = tile
                while nextTile in board:  # build word
                    nextX, nextY = nextTile
                    if (nextX, nextY + 1) not in board and (nextX, nextY - 1) not in board:
                        down[(nextTile, nextTile)] = board[nextTile]  # is it playable vertically
                    word += board[nextTile]
                    nextTile = (nextTile[0] - 1, nextTile[1])
                last = (tile[0] - len(word) + 1, tile[1])
                across[(tile, last)] = word  # add word to horizontal plays
            if y == 1:  # is down
                word = ""
                nextTile = tile
                while nextTile in board:  # build word
                    nextX, nextY = nextTile
                    if (nextX + 1, nextY) not in board and (nextX - 1, nextY) not in board:
                        across[(nextTile, nextTile)] = board[nextTile]  # is it playable horizontally
                    word += board[nextTile]
                    nextTile = (nextTile[0], nextTile[1] - 1)
                last = (tile[0], tile[1] - len(word) + 1)
                down[(tile, last)] = word  # add word to horizontal plays
        return across, down

    @staticmethod
    # get the plays available
    def getWordPlays(board):
        # TODO: add "bridge" plays that span 2 or more separated tiles
        across, down = BananagramsUtil.getPlayableSpots(board)
        pass

    @staticmethod
    # get the space above, below, left, and right of a tile params: board to search, tile to check
    def getTileSpace(board, tile):
        left, top, right, bottom = BananagramsUtil.getBoardArea(board)
        pass

    @staticmethod
    # get the boundaries of used the board (left, top, right, bottom) params: board to check
    def getBoardArea(board):
        left = 0  # running left edge value
        top = 0  # running top edge value
        right = 0  # running right edge value
        bottom = 0  # running bottom edge value
        for tile in board:
            x, y = tile
            if x > left:
                left = x  # beyond running left
            elif x < right:
                right = x  # beyond running right
            if y > top:
                top = y  # beyond running top
            elif y < bottom:
                bottom = y  # beyond running bottom
        return left, top, right, bottom


