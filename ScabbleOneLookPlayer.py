from OneLookPlayer import OneLook


# player that plays the highest scoring scrabble word available
class ScrabbleOneLook(OneLook):
    def __str__(self):
        return "Scrabble One Look"

    def heuristic(self, play):
        scrabble = {"A": 1, "E": 1, "I": 1, "L": 1, "N": 1, "O": 1, "R": 1, "S": 1, "T": 1, "U": 1,
                    "D": 2, "G": 2,
                    "B": 3, "C": 3, "M": 3, "P": 3,
                    "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
                    "K": 5,
                    "J": 8, "X": 8,
                    "Q": 10, "Z": 10}
        word = play[0]
        points = 0
        for letter in word:
            points += scrabble[letter]  # add scrabble tile value
        return points
