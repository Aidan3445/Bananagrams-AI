import heapq
from abc import ABC, abstractmethod
from AIPlayer import AIPlayer
from Util import BananagramsUtil as util


# AI players that use A* to make moves
class AStar(AIPlayer, ABC):
    @abstractmethod
    # A* heuristics take in states, not plays
    def heuristic(self, state):
        pass

    @abstractmethod
    # whether to terminate a search at a state
    def terminateSearch(self, state):
        pass

    # use A* to determine the best moves
    def nextMoves(self):
        frontier = PriorityQueue()
        explored = set()
        start = self.Node(self.State(self.board, self.hand), [])
        frontier.push(start, self.heuristic(start.state))
        while not frontier.isEmpty():
            current = frontier.pop()
            currentBoard = current.state.board
            currentHand = current.state.hand
            if self.terminateSearch(current.state):
                return current.moves
            explored.add(current)
            allPlays = util.getAllPlays(currentBoard, currentHand)
            for tile in allPlays:
                for play in allPlays[tile]:
                    move = (tile, play)
                    nextBoard, nextHand = util.makeMove(move, currentBoard, currentHand)
                    successor = self.State(nextBoard, nextHand)
                    newMoves = current.moves + [move]
                    print(newMoves)
                    cost = len(newMoves) + self.heuristic(successor)
                    child = self.Node(successor, newMoves)
                    if child not in explored:
                        frontier.update(child, cost)
        return []

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
