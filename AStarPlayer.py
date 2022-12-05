from abc import ABC, abstractmethod
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util
from Util import PriorityQueue


# AI players that use A* to make moves
class AStar(AIPlayer, ABC):
    @abstractmethod
    # A* heuristics take in states, not plays params: state to evaluate
    # params: state to evaluate
    def heuristic(self, state):
        pass  # this should be a guess as to how many words it will take to finish the hand

    # whether to terminate a search at a state params: state to test
    # params: state to evaluate
    def terminateSearch(self, state):
        return util.countTiles(state.hand) <= util.countTiles(self.hand)/5

    # evaluate a set of moves to get their cost params: moves made
    # params: moves to evaluate cost from
    def getCost(self, moves):
        playedTiles = 0
        for move in moves:
            playedTiles += len(move[1][0])
        cost = util.countTiles(self.hand) - playedTiles
        return cost

    # use A* to determine the best moves
    # params: board to play on, hand to play from
    def nextMoves(self, board, hand):
        frontier = PriorityQueue()
        start = self.Node(self.State(board, hand), [])
        frontier.push(start, self.heuristic(start.state))
        while not frontier.isEmpty():
            current = frontier.pop()
            currentBoard = current.state.board
            currentHand = current.state.hand
            if self.terminateSearch(current.state) and current.moves:
                return current.moves
            allPlays = util.getAllPlays(currentBoard, currentHand)
            for tile in allPlays:
                for play in allPlays[tile]:
                    move = (tile, play)
                    nextBoard, nextHand = util.makeMove(move, currentBoard, currentHand)
                    successor = self.State(nextBoard, nextHand)
                    newMoves = current.moves + [move]
                    cost = self.getCost(newMoves) + self.heuristic(successor)
                    child = self.Node(successor, newMoves)
                    frontier.update(child, cost)
        return self.NoAStar(board, hand)  # no moves found

    # run if no A* moves found
    def NoAStar(self, board, hand):
        best = None
        lowest = float("inf")
        allPlays = util.getAllPlays(board, hand)
        for tile in allPlays:
            for play in allPlays[tile]:
                move = (tile, play)
                nextBoard, nextHand = util.makeMove(move, board, hand)
                val = self.heuristic(self.State(nextBoard, nextHand))
                if val < lowest:
                    best = move
                    lowest = val
        if best:
            return [best]
        else:
            return [(None, None)]

    # holds a game state which is the hand and the board (players do not know the tile pool)
    class State:
        def __init__(self, board, hand):
            self.board = board
            self.hand = hand

    # holds a node with a state and moves to get there
    class Node:
        def __init__(self, state, moves):
            self.state = state
            self.moves = moves

