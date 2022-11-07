import random
from Util import BananagramsUtil as util
from SimpleDictOneLookPlayer import SimpleDictOneLook

class TestSimpleDictOneLook(SimpleDictOneLook):

    def __str__(self):
        return "Test Longest Word One Look"

    def heuristic(self, play):
        return random.randint(0,9)