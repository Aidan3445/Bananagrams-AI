# AI Bananagrams Project

![Title](https://user-images.githubusercontent.com/102766475/209456396-e9169f5f-682f-4452-a594-d276f08c233a.png)

This is the final project for CS4100 at Northeastern University, where we applied search, game-playing, and probabilistic algorithms to develop AI Bananagrams players.

## Project Overview

The goal of this project was to use artificial intelligence strategies to tackle the game of Bananagrams, a fast-paced word game that challenges players to create valid words from a set of letter tiles. We explored various algorithms and playing strategies to create AI players capable of competing in Bananagrams.

## How to Run

The main.py script is the entry point for the project. You can run it with a series of command-line arguments to control the game's parameters, including the size of the window, the number of run simulations, and which AI players are in the simulation. If you run the script without any arguments, it will enter single-player mode, allowing you to test your own Bananagrams skills.

For further customization and experimentation, you can edit and run the main.py script from an IDE.

## Driving Questions

Our project was guided by several driving questions:

1. How can we use AI to solve Bananagrams?
2. What is the most effective strategy to solve the problem?
3. How can we, as humans, use AI to become better Bananagrams players?

## What is Bananagrams?

Bananagrams is a word game that can be played with one to four players. Players draw letter tiles to form their hand and create a grid of connecting words with these tiles. The game is fast-paced, and the objective is to be the first to play all tiles on the board. There are strategies involved in using limited vowels and challenging letters like 'Q' or 'Z.' Speed and creativity are essential in Bananagrams.

## Tools Used

We used Python and the Pygame library for visualizing the game board. For word checking and finding anagrams, we utilized the [TWL06](https://github.com/fogleman/TWL06) word search library, which employs a directed acyclic word graph (DAWG) to efficiently validate words.

## Relaxations

To make the problem tractable, we introduced two relaxations compared to the actual Bananagrams game:

1. Players take turns playing one word at a time instead of playing synchronously.
2. Players cannot reconstruct sections or their entire board once a word is played.

These relaxations might result in stalemates in single-player games.

## Modeling

The GameState represents the communal tile pool from which players 'peel.' Each AI playing agent, or Player, has a State representing their board of played tiles and their hand of remaining tiles.

Players can take actions like 'play' a word onto their board, 'peel' a letter when some player has used all its tiles, and/or 'dump' a tile. To find successors, each Player uses an algorithm that analyzes their current board and hand to find all possible moves. They evaluate these moves using their specific algorithm and a heuristic to decide the best move to take.

## Algorithms

### Checking Valid Boards/Moves

We used Breadth-First Search (BFS) to check for valid boards, ensuring no 'islands' and that all tiles are connected. We also looped through each row/column to identify the start tiles for words and then built words by moving down and/or across from each start tile. The [TWL06](https://github.com/fogleman/TWL06) library was used to validate words.

For single moves, we checked the words formed immediately after branching off the move.

### Move Generation

For the first move, we used the [TWL06](https://github.com/fogleman/TWL06) library to find all anagrams from the player's hand. As tiles accumulated on the board, we used the 'Bridge Moves' algorithm to generate a list of all anagrams, taking the player's hand and the tiles in that row/column into account.

### Playing Agents

We created four playing agents with different algorithms:

1. **OneLook Player**: This simple agent searches through all possible moves and evaluates playable words based on heuristics, such as longest word, shortest word, and highest Scrabble score.

2. **A* Player**: Using the A* search algorithm, this agent finds the best sequence of moves based on heuristics, including longest word and highest Scrabble score.

3. **Trial Player**: The Trial Player uses either A* or OneLook to predict future events by sampling each action (peel, wait, or dump) multiple times and choosing the optimal move based on heuristics.

4. **Smart Player**: The Smart Player combines A* or OneLook with Trial, switching between them depending on the game state to balance speed and accuracy.

## Analysis

- A* and OneLook Players often end in stalemates in single-player games due to the inability to redraw the board.
- Smart and Trial Players have higher single-player success rates as they think ahead to avoid stalemates.
- Smart Players, which combine A* or OneLook with Trial, have the highest overall win rates, showcasing the benefit of combining algorithms.
- Longest word and Scrabble score alone do not guarantee a win, suggesting that a more complex strategy is needed in Bananagrams.

## Conclusion and Future Work

We successfully used AI to solve Bananagrams and identified effective strategies. Future work could involve:

- Removing relaxations to enable synchronous play.
- Improving the efficiency of existing algorithms.
- Allowing players to redraw portions or their entire board to eliminate stalemate possibilities.

We have successfully answered our driving question of using AI to solve Bananagrams and which strategies are most effective. However, we were unable to use our AI to inform us how humans could improve their own Bananagrams play.
