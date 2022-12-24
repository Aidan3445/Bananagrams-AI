Final Project for CS4100 at Northeastern University

Using https://github.com/fogleman/TWL06 for word dictionary.

We applied search, game-playing, and probabilistic algorithms to develop AI Bananagrams players. 

The main.py script can be run with a series of command-line arguments to control the size of the window, number of run simulations, and which players are in the simulation. Running the script without any arguemnts will enter the user single player mode where you can test your own Bananagrams skills.
You can also edit the main.py script to allow for even more customization of the AI players.

# Banan-AI-grams

### Driving Questions
For our project, we used AI strategies to solve the game of Bananagrams. Our driving questions are as follows: 
* How can we use AI to solve Bananagrams?
* What is the most effective strategy to solve the problem? 
* How can we, as humans, use AI to become better Bananagrams players? 

### What is Bananagrams? 

The game of Bananagrams can be played with between one and four players. The game is set up with a communal pool of face-down letter tiles from which each player draws a certain number to form their hand. When the game begins, all players, at the same time, flip their tiles to reveal the letters and arrange them into a grid of valid, connecting words. During play, if a player wants to get rid of a tile, perhaps a problematic letter like “Q” or “Z,” they may “dump,” and exchange that one tile with two from the center pool. When any one player successfully places all tiles onto their board, they call “Peel!” and all players must draw a tile from the pool. Once the pool is depleted and there can be no more even “peels,” the first player to play all of their tiles on their board is the winner. 

Bananagrams does not reward complex words like Scrabble, and all that matters is playing all of one’s tiles in some valid word. It is a game of speed. 

### Tools 
We use Python and the Pygame library to visualize the board in our implementation. We borrowed the priority queue class from the Berkeley PacMan Programming Assignment. To check for valid words and to find anagrams of a set of letters, we utilize the TWL06 word search library, which uses a directed acyclic word graph (DAWG) to efficiently look up and check words. 

### Relaxations 
Between the actual Bananagrams game and our model, we made two relaxations. 
First, in the actual game, all players play synchronously. However, in our model, they take turns playing one word at a time. To clarify, if each player has one turn in a “round,” then in each “round,” the order they take their turns will be random, so one player does not have the advantage of always playing first. 

Second, in the actual game, players can reconstruct sections or their entire board at any time to better suit the words they aim to play. In our model, we do not allow Players to do this; once a word is played on the board, it may not be changed. Due to this relaxation, at the end of a game, a stalemate may occur. 

### Modeling 
We faced some limitations when modeling the game and defined the model as follows. 
The GameState is the communal tile pool from which players “peel.” Each AI playing agent, or Player’s, State is their board of played tiles and their hand of remaining tiles. 

At their turn, a Player can take the action to “play” a word onto their board, “peel” a letter when some player has used all of its tiles, and/or “dump” a tile. The Trial and Smart Players, which will be defined below, also can “wait” during their turn and not play any word. 

To “get successors,” each Player uses an algorithm that analyzes their current board of played words and their hand of tiles to find all possible moves they can take. Once they gather all possible moves, each Player will evaluate the moves using their distinct algorithm and a specified heuristic to decide the best move to take. At each turn, the Player’s State (input) is evaluated to return the move, a word played on their board, they should take (output). 

### Algorithms
TODO: write the breakdown of main algorithms in the game logic


### Playing Agents
To solve Bananagrams, we used four different playing agents, Players, the implement different algorithms to choose the next move they should take at each turn. 

The first and most simple agent is the OneLook Player. OneLook searches through all possible moves at the current state and evaluates the playable words based on a specified heuristic. OneLook’s three possible heuristics evaluate to find, respectively, the longest possible word (LongestWord), the shortest possible word (ShortestWord), and the word with the highest Scrabble score, which values rare letters (Scrabble). OneLook is the most efficient algorithm. 

The second agent is the A* Player, which uses the A* search algorithm to find the best sequence of moves from the current state. The algorithm evaluates the resulting hand after playing a word based on a specified heuristic. Similar to OneLook, A*’s two heuristics evaluate for the longest word and the highest Scrabble score. This Player is slower than OneLook but is more effective. 

Third, the Trial Player uses either A* or OneLook in an attempt to predict future events and makes a move accordingly. Trial samples each action– either “peel,” “wait,” or “dump”– a given number of times to determine the most optimal move according to OneLook/A*’s heuristic. The Trial algorithm evaluates the board at each sample using a sample heuristic. The sample heuristics evaluate based on the average word length and the average word Scrabble score. The Trial Player is less efficient but more effective. 
	
The fourth and final agent is the Smart Player, which combines either the A* or OneLook Player with the Trial Player. Smart Players use A*/OneLook at the beginning of the game to quickly make moves and then switch to Trial when few tiles remain in the pool. Smart Players take advantage of A*/OneLook’s efficiency in combination with the improved performance of the Trial Player at the end when there is a higher risk of getting stuck in a stalemate and a single move may directly result in a win. 

### Analysis 
First, since we do not allow Players to redraw their boards, A* and OneLook Players often end in a stalemate in single-player games. However, Smart and Trial Players have much higher single-player success rates because, while they do take longer to choose moves, they think ahead to pick moves that reduce the likelihood of getting stuck in a stalemate at the game’s end. 

Additionally, Smart Players, which combine OneLook/A* with Trial, have the highest overall win rates because they have both speed and accuracy. This result aligns with our hypothesis and driving motivation for writing the Smart Player: a winning strategy must combine the positive attributes of the other three algorithms and use the pairing to reduce individual weaknesses. 

In terms of the two common heuristics, LongestWord and Scrabble, there is no clear winning strategy. So, the AI agents do not reveal how a human could adopt its methods to improve their play in real life; playing simply based on word length or Scrabble score does not guarantee a win. 

### Conclusion
Moving forward, we consider changing our model to remove the need for the current relaxations. If we enable the Players to compete synchronously, instead of taking turns, then the efficiency of the algorithms would become much more important and would likely lead to more clear results. Further, we would like to improve the efficiency of our existing algorithms, particularly the method that searches the board for all possible moves. Finally, again removing a relaxation, we would like to add the ability for Players to redraw portions of their boards or their entire board to eliminate the chance of getting stuck and ending in a stalemate. This addition of redrawing the board would likely change Player performance, efficiency, and success rates. 

We have successfully answered our driving question of using AI to solve Bananagrams and which strategies are most effective. However, we were unable to use our AI to inform us how humans could improve their own Bananagrams play. 
