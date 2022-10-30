from OneLookPlayer import OneLook


# one look player that plays the longest word available
class LongestOneLook(OneLook):
    # what should return when printed
    def __str__(self):
        return "Longest Word One Look"

    # evaluate play/state
    def heuristic(self, play):
        return len(play[0])  # return length of word
