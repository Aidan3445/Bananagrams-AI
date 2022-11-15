import heapq
import sys
import random
from pprint import pprint

import pygame as pg
import numpy as np
import words.twl as words


class BananagramsUtil:
    @staticmethod
    # quit game
    def quit():
        pg.quit()
        sys.exit()

    @staticmethod
    # convert hand tiles to single string
    def handToString(hand):
        handString = ""
        for letter in hand:
            handString += letter * hand[letter]  # add letters to string
        return handString

    @staticmethod
    # convert a board tiles into a string display of the board
    def printBoard(board):
        left, right, top, bottom = BananagramsUtil.getBoardArea(board)
        boardList = np.full(((top - bottom + 1), (left - right + 1)), "_").tolist()
        for x, y in board:
            boardList[top - y][left - x] = board[(x, y)]
        boardString = ""
        for line in boardList:
            for tile in line:
                boardString += tile + " "
            boardString += "\n"
        return boardString

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
        letter = BananagramsUtil.getRandomTile(tileSet)
        tileSet[letter] -= 1
        return letter

    @staticmethod
    # get random tile from tile set params: dictionary to pull from
    def getRandomTile(tileSet):
        cnt = 0
        index = random.randint(0, BananagramsUtil.countTiles(tileSet) - 1)
        for letter in tileSet:
            cnt += tileSet[letter]
            if cnt > index:  # once count breaks index barrier letter has been found
                return letter

    @staticmethod
    # play a word from a hand onto a board params: move to make, hand to play from, board to play on
    def makeMove(move, board, hand):
        connect, play = move
        word, offset, direction = play
        boardCopy = board.copy()  # make play on copy of current board and hand
        handCopy = hand.copy()
        nextTile = (connect[0] - (offset * direction[0]), connect[1] - (offset * direction[1]))
        for letter in word:
            boardCopy[nextTile] = letter
            handCopy[letter] -= 1
            nextTile = (nextTile[0] - 1, nextTile[1])
        return boardCopy, handCopy

    @staticmethod
    # check board for valid words params: board to check
    def check(board):
        valid = []
        invalid = []
        islands = BananagramsUtil.islandCheck(board)
        if islands:
            v, i = BananagramsUtil.check(islands)
            invalid += v
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
            if x == 0 and y == 0:  # if tile has no direction it is a single tile and is not valid
                invalid.append(board[tile])
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
            if not ((tile[0] - 1, tile[1]) in board or  # if single tile add with no direction
                    (tile[0] + 1, tile[1]) in board or
                    (tile[0], tile[1] - 1) in board or
                    (tile[0], tile[1] + 1) in board):
                firstTiles[tile] = (0, 0)
        return firstTiles

    @staticmethod
    # run bfs to check that all tiles are connected
    def islandCheck(board):
        if len(board) > 0:
            allTiles = list(board)
            frontier = list()
            explored = set()
            start = allTiles[0]
            frontier.insert(0, start)
            while len(frontier) > 0:
                current = frontier.pop()
                explored.add(current)
                for successor in BananagramsUtil.getSuccessors(board, current):
                    if successor not in explored:
                        if successor not in frontier:
                            frontier.insert(0, successor)
            island = set(allTiles) - explored
            islandTiles = {}
            for tile in island:
                islandTiles[tile] = board[tile]
            return islandTiles
        return {}

    @staticmethod
    def getSuccessors(board, current):
        successors = []
        possibleTiles = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]
        for t in possibleTiles:
            if t in board:
                successors.append(t)
        return successors

    @staticmethod
    # get the plays available params: board to play on, hand to play from
    def getAllPlays(board, hand):
        handString = BananagramsUtil.handToString(hand)
        allPlays = {}
        plays = BananagramsUtil.getBridgePlays(handString, board)
        for tile in plays:
            allPlays[tile] = plays[tile]
        for tile in board:
            if tile in allPlays:
                allPlays[tile] += BananagramsUtil.getTilePlays(handString, tile, board)
            else:
                allPlays[tile] = BananagramsUtil.getTilePlays(handString, tile, board)
        if not allPlays:
            allPlays[(0, 0)] = BananagramsUtil.getTilePlays(handString)
        return allPlays

    @staticmethod
    # get words to play off of letter params: letters in hand, letter to play off, boundaries for word length
    def getTilePlays(letters, tile=None, board=None):
        if tile is None or board is None:
            allWords = list(words.anagram(letters))  # empty board means all anagrams are valid
            playableWords = []
            for word in allWords:
                word = word.upper()
                playableWords.append((word, 0, (-1, 0)))  # all first plays go across
            return playableWords
        tileLetter = board[tile]
        restrictions = BananagramsUtil.getTileSpace(board, tile)
        allWords = list(words.anagram(letters + tileLetter))
        playableWords = []
        left, right, top, bottom = restrictions
        maxLength = max(left + right, top + bottom)
        for word in allWords:
            word = word.upper()
            wordLength = len(word)
            # remove word if too long or doesn't have tile letter
            if wordLength > maxLength or tileLetter not in word:
                continue
            before = word.index(tileLetter)  # letters before tile letter
            after = wordLength - before - 1  # letters after tile letter
            # across checks
            if before < left and after < right:
                test = board.copy()  # make play on copy of current board
                nextTile = (tile[0] + before, tile[1])
                for letter in word:
                    test[nextTile] = letter
                    nextTile = (nextTile[0] - 1, nextTile[1])
                _, invalid = BananagramsUtil.check(test)  # check for play validity
                if not invalid:
                    playableWords.append((word, before, (-1, 0)))
            # down checks
            if before < top and after < bottom:
                test = board.copy()  # make play on copy of current board
                nextTile = (tile[0], tile[1] + before)
                for letter in word:
                    test[nextTile] = letter
                    nextTile = (nextTile[0], nextTile[1] - 1)
                _, invalid = BananagramsUtil.check(test)  # check for play validity
                if not invalid:
                    playableWords.append((word, before, (0, -1)))
        return playableWords

    @staticmethod
    # get plays that bridge between two t or more tiles already on the board
    def getBridgePlays(letters, board):
        cols = {}
        rows = {}
        for tile in board:  # get all tiles in each row and column
            x, y = tile
            if x not in cols:  # if not already in cols add a priority queue to the dictionary
                colQ = PriorityQueue()
                cols[x] = colQ
            cols[x].update(tile, -y)
            if y not in rows:  # if not already in rows add a priority queue to the dictionary
                rowQ = PriorityQueue()
                rows[y] = rowQ
            rows[y].update(tile, -x)
        colWords = {}  # holds all the words that are playable vertically
        rowWords = {}  # holds all the words that are playable horizontally
        for col in cols:  # check all columns
            colQ = cols[col]
            tileLetters = ""
            for item in colQ.heap:  # add each tile's letter to string
                tileLetters += board[item[2]]
            colWords[col] = list(words.anagram(letters + tileLetters))  # find anagrams
        for row in rows:  # same as columns above
            rowQ = rows[row]
            tileLetters = ""
            for item in rowQ.heap:
                tileLetters += board[item[2]]
            rowWords[row] = list(words.anagram(letters + tileLetters))
        allPlays = {}
        for col in colWords:  # check for words that fit in board vertically
            colQ = cols[col]
            colString = ""  # string of letters in order top to bottom
            colTiles = []
            while not colQ.isEmpty():
                tile = colQ.pop()
                colString += board[tile].lower()
                colTiles.append(tile)
            wordList = colWords[col]
            for word in wordList:  # go through all words
                inOrder = True
                prevInBoard = -1
                prevInWord = -1
                startTile = None
                test = board.copy()
                for wordIndex, letter in enumerate(word):  # are letters from the column in the correct order
                    if letter in colString:  # is letter from board
                        boardIndex = colString.index(letter)
                        if prevInBoard == -1:  # set index of first tile from board
                            prevInBoard = boardIndex
                            prevInWord = wordIndex
                            startTile = (col, wordIndex + colTiles[boardIndex][1])
                        if prevInWord - wordIndex != colTiles[boardIndex][1] - colTiles[prevInBoard][1]:
                            inOrder = False  # if letters are not same distance apart as tiles in board, it is invalid
                            break
                        else:
                            prevInWord = wordIndex
                        if boardIndex >= prevInBoard:  # comes after previous letter
                            prevInBoard = boardIndex
                        else:  # letter was not in order, remove word and break loop
                            inOrder = False
                            break
                if startTile and inOrder:  # if passed checks above, play word onto copy of board
                    valid = True
                    for wordIndex, letter in enumerate(word):
                        nextTile = (startTile[0], startTile[1] - wordIndex)
                        if nextTile in test:
                            if letter.upper() != test[nextTile]:
                                valid = False
                                break
                        test[nextTile] = letter.upper()
                    if valid and not BananagramsUtil.check(test)[1]:  # check copy of board for valid
                        if startTile not in allPlays:
                            allPlays[startTile] = []
                        allPlays[startTile].append((word.upper(), 0, (0, -1)))
        for row in rowWords:  # same as cols above
            rowQ = rows[row]
            rowString = ""
            rowTiles = []
            while not rowQ.isEmpty():
                tile = rowQ.pop()
                rowString += board[tile].lower()
                rowTiles.append(tile)
            wordList = rowWords[row]
            for word in wordList:
                inOrder = True
                prevInBoard = -1
                prevInWord = -1
                startTile = None
                test = board.copy()
                for wordIndex, letter in enumerate(word):
                    if letter in rowString:
                        boardIndex = rowString.index(letter)
                        if prevInBoard == -1:
                            prevInBoard = boardIndex
                            prevInWord = wordIndex
                            startTile = (wordIndex + rowTiles[boardIndex][0], row)
                        if prevInWord - wordIndex != rowTiles[boardIndex][0] - rowTiles[prevInBoard][0]:
                            inOrder = False
                            break
                        else:
                            prevInWord = wordIndex
                        if boardIndex >= prevInBoard:
                            prevInBoard = boardIndex
                        else:
                            inOrder = False
                            break
                if startTile and inOrder:
                    valid = True
                    for wordIndex, letter in enumerate(word):
                        nextTile = (startTile[0] - wordIndex, startTile[1])
                        if nextTile in test:
                            if letter.upper() != test[nextTile]:
                                valid = False
                                break
                        test[nextTile] = letter.upper()
                    if valid and not BananagramsUtil.check(test)[1]:
                        if startTile not in allPlays:
                            allPlays[startTile] = []
                        allPlays[startTile].append((word.upper(), 0, (-1, 0)))
        return allPlays

    @staticmethod
    # get the space above, below, left, and right of a tile params: board to search, tile to check
    def getTileSpace(board, tile):
        left, right, top, bottom = BananagramsUtil.getBoardArea(board)
        x, y = tile
        posX = x
        negX = x
        posY = y
        negY = y
        while posX < left:  # positive x direction (left)
            if (posX + 1, y) in board:
                break
            posX += 1
        while negX > right:  # negative x direction (right)
            if (negX - 1, y) in board:
                break
            negX -= 1
        while posY < top:  # positive y direction (up)
            if (x, posY + 1) in board:
                break
            posY += 1
        while negY > bottom:  # negative y direction (down)
            if (x, negY - 1) in board:
                break
            negY -= 1
        if posX == left:  # reached boundary, no limit on word length in this direction
            posX = float('inf')
        if negX == right:
            negX = float('-inf')
        if posY == top:
            posY = float('inf')
        if negY == bottom:
            negY = float('-inf')
        return posX - x, x - negX, posY - y, y - negY

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
        return left, right, top, bottom


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

    def findItem(self, item):
        # if item is in heap, return priority
        # otherwise return None
        for p, c, v in self.heap:
            if v == item:
                return p
        return None


b = {(0, -4): "B", (-1, -4): "R", (-2, -4): "A", (-3, -4): "I", (-4, -4): "N", (0, 0): "C", (-4, 0): "D", (-2, 0): "O",
     (-4, -1): "R", (-4, -2): "A", (-4, -3): "I"}

print(BananagramsUtil.printBoard(b))
# print(BananagramsUtil.check(b))
print(BananagramsUtil.getBridgePlays("LU", b))
