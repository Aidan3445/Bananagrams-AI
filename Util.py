import heapq
import sys
import random
import time

import pygame as pg
import numpy as np
import words.twl as words

nullHand = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0,
            "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0,
            "W": 0, "X": 0, "Y": 0, "Z": 0}


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
    def boardToString(board):
        left, right, top, bottom = BananagramsUtil.getBoardArea(board)
        boardList = np.full(((top - bottom + 1), (left - right + 1)), "_").tolist()
        for x, y in board:
            boardList[top - y][left - x] = board[(x, y)]
        boardString = ""
        for line in boardList:
            for tile in line:
                boardString += tile + " "
            boardString += "\n"
        boardString += "↑\n" + str((left, bottom))
        return boardString

    @staticmethod
    # get the number of tiles in a dictionary
    # params: dictionary to count
    def countTiles(tileSet):
        cnt = 0
        for letter in tileSet:
            cnt += tileSet[letter]  # add value
        return cnt

    @staticmethod
    # pull a tile from the set
    # params: dictionary to pull from
    def pullTile(tileSet):
        letter = BananagramsUtil.getRandomTile(tileSet)
        tileSet[letter] -= 1
        return letter

    @staticmethod
    # get random tile from tile set
    # params: dictionary to pull from
    def getRandomTile(tileSet):
        cnt = 0
        index = random.randint(0, BananagramsUtil.countTiles(tileSet))
        for letter in tileSet:
            cnt += tileSet[letter]
            if cnt >= index:  # once count breaks index barrier letter has been found
                return letter

    @staticmethod
    # play a word from a hand onto a board
    # params: move to make, board to play on, OPT hand to play from,
    def makeMove(move, board, hand=None):
        if hand is None:
            hand = nullHand
        connect, play = move
        word, offset, direction = play
        boardCopy = board.copy()  # make play on copy of current board and hand
        handCopy = hand.copy()
        nextTile = (connect[0] - (offset * direction[0]), connect[1] - (offset * direction[1]))
        for letter in word:
            if nextTile not in boardCopy:
                boardCopy[nextTile] = letter
                handCopy[letter] -= 1
            nextTile = (nextTile[0] + direction[0], nextTile[1] + direction[1])
        return boardCopy, handCopy

    @staticmethod
    # check board for valid words
    # params: board to check
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
    # get a dictionary of the tiles that are the first letter of each word and the direction
    # params: board to search
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
                for successor in BananagramsUtil.getNextSearchTiles(board, current):
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
    # get the next tiles in the search
    # params: board to search, current tile in search
    def getNextSearchTiles(board, current):
        successors = []
        possibleTiles = [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                         (current[0], current[1] + 1), (current[0], current[1] - 1)]
        for t in possibleTiles:
            if t in board:
                successors.append(t)
        return successors

    @staticmethod
    # get the plays available
    # params: board to play on, hand to play from
    def getAllPlays(board, hand):
        handString = BananagramsUtil.handToString(hand)
        allPlays = {}
        bridgePlays = BananagramsUtil.getBridgePlays(handString, board)
        for tile in bridgePlays:
            if tile in allPlays:
                allPlays[tile] += bridgePlays[tile]
            else:
                allPlays[tile] = bridgePlays[tile]
        if not allPlays:
            allPlays[(0, 0)] = BananagramsUtil.getFirstPlays(handString)
        return allPlays

    @staticmethod
    # get words to play from hand to blank board
    # params: letters in hand
    def getFirstPlays(letters):
        allWords = list(words.anagram(letters))  # empty board means all anagrams are valid
        playableWords = []
        for word in allWords:
            word = word.upper()
            playableWords.append((word, 0, (-1, 0)))  # all first plays go across
        return playableWords

    @staticmethod
    # get plays that bridge between two or more tiles already on the board
    def getBridgePlays(handString, board):
        # helper methods
        # get all words in a column/row
        # params: priority queue with letters in a col/row
        def getWords(pQueue):
            tileLetters = ""
            for item in pQueue.heap:  # add each tile's letter to string
                tileLetters += board[item[2]]
            return list(words.anagram(handString + tileLetters))  # find anagrams

        # convert priority queue of letters to a list with blanks in gaps between tiles
        # params: priority queue
        def queueToList(pQueue):
            order = []
            if not pQueue.isEmpty():
                t = pQueue.pop()
                prev = t
                order.append((board[t], t))
                while not pQueue.isEmpty():  # loop until queue is empty
                    t = pQueue.pop()  # this method "destroys" the queue
                    x = prev[0] - t[0]
                    y = prev[1] - t[1]
                    gap = max(x, y) - 1
                    if x > 0:
                        x = 1
                    if y > 0:
                        y = 1
                    for i in range(gap):  # add Nones inbetween tiles
                        order.append((None, (prev[0] - x, prev[1] - y)))
                    order.append((board[t], t))  # add letter and spacing to list in order
                    prev = t
            return order

        # check the order and spacing of letters in a word to make sure they fit in the board
        # params: word to check, list of [(letter, tile)]
        def getFit(word, handString, queueList):
            startOffsets = []
            lenW = len(word)
            lenQ = len(queueList)
            for startIndex in range(1 - lenW, lenQ):
                fits = True
                fromHand = False
                hand = list(handString)
                for wordIndex, letter in enumerate(word):
                    letter = letter.upper()
                    queueIndex = startIndex + wordIndex
                    if 0 <= queueIndex < lenQ:
                        queueLetter, _ = queueList[queueIndex]
                        if queueLetter is None:
                            if letter in hand:
                                hand.remove(letter)
                                fromHand = True
                            else:
                                fits = False
                                break
                        elif queueLetter != letter:
                            fits = False
                            break
                    elif letter in hand:
                        hand.remove(letter)
                        fromHand = True
                    else:
                        fits = False
                        break
                if fits and fromHand:
                    startOffsets.append(-startIndex)
            return startOffsets

        # main method
        if handString == "":
            return {}
        cols, rows = BananagramsUtil.getColsRows(board)
        colWords = {}  # holds all the words that are playable vertically
        rowWords = {}  # holds all the words that are playable horizontally
        for col in cols:  # get all words from each column and row
            colWords[col] = getWords(cols[col])
        for row in rows:
            rowWords[row] = getWords(rows[row])
        allPlays = {}  # holds all the plays available with the current hand
        for col in colWords:  # check for words that fit in board vertically
            wordList = colWords[col]
            colList = queueToList(cols[col])
            firstTile = colList[0][1]
            for word in wordList:  # go through all words
                startOffsets = getFit(word, handString, colList)
                for offset in startOffsets:
                    test = board.copy()
                    startTile = (col, firstTile[1] + offset)
                    for wordIndex, letter in enumerate(word):
                        nextTile = (startTile[0], startTile[1] - wordIndex)
                        test[nextTile] = letter.upper()
                    if not BananagramsUtil.check(test)[1]:  # check copy of board for valid
                        if startTile not in allPlays:
                            allPlays[startTile] = []
                        allPlays[startTile].append((word.upper(), 0, (0, -1)))
        for row in rowWords:  # same as cols above
            wordList = rowWords[row]
            rowList = queueToList(rows[row])
            firstTile = rowList[0][1]
            for word in wordList:
                startOffsets = getFit(word, handString, rowList)
                for offset in startOffsets:
                    test = board.copy()
                    startTile = (firstTile[0] + offset, row)
                    for wordIndex, letter in enumerate(word):
                        nextTile = (startTile[0] - wordIndex, startTile[1])
                        test[nextTile] = letter.upper()
                    if not BananagramsUtil.check(test)[1]:
                        if startTile not in allPlays:
                            allPlays[startTile] = []
                        allPlays[startTile].append((word.upper(), 0, (-1, 0)))
        return allPlays

    @staticmethod
    # create two dictionaries with all tiles in each occupied column and row of the board
    # params: board to get from
    def getColsRows(board):
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
        # keys are ints of the col/row, values are priority queues sorted from left->right/top->bottom
        return cols, rows

    @staticmethod
    # get the space above, below, left, and right of a tile
    # params: board to search, tile to check
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
    # get the boundaries of used the board (left, top, right, bottom)
    # params: board to check
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
    # represents a priority queue using a heap to store data
    def __init__(self):
        self.heap = []
        self.count = 0

    # add an item to the priority queue
    # params: item to add, priority to insert
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    # remove and return the lowest priority item in the queue
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    # return true if heap is empty
    def isEmpty(self):
        return len(self.heap) == 0

    # if item already in priority queue with higher priority, update its priority and rebuild the heap
    # if item already in priority queue with equal or lower priority, do nothing
    # if item not in priority queue, do the same thing as self.push
    # params: item to update, new priority
    def update(self, item, priority):
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

    # if item is in heap, return priority otherwise return None
    # params: item to search for
    def findItem(self, item):

        for p, c, v in self.heap:
            if v == item:
                return p
        return None
