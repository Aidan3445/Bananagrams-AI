import argparse
from game.Bananagrams import Bananagrams
from players.LongestWordPlayer import *
from players.ScrabblePlayer import *
from players.ShortestWordPlayer import *

parser = argparse.ArgumentParser(description="Bananagrams AI")
setPlayers = parser.add_subparsers(title="Set Players", dest="setPlayers")

presets = setPlayers.add_parser(name="presets")
group = presets.add_mutually_exclusive_group()
group.add_argument("-l", "--lookies", action="store_true", help="One One-Look Player of each type: ["
                                                                "LongestOneLook(), ScrabbleOneLook(), "
                                                                "ShortestOneLook()]")
group.add_argument("-st", "--starries", action="store_true", help="One 'A* Player' of each type: [LongestAStar(), "
                                                                  "ScrabbleAStar()]")
group.add_argument("-t", "--trialies", action="store_true", help="One 'Trial Player' of each type: ["
                                                                 "LongestOneLookTrial(2), LongestOneLookTrial(3),"
                                                                 "\nLongestOneLookTrial(4), LongestOneLookTrial(5)]")
group.add_argument("-sm", "--smarties", action="store_true", help="One 'Smart Player' of each type: ["
                                                                  "LongestOneLookSmarty(2, 5), LongestAStarSmarty("
                                                                  "2, 5), ScrabbleOneLookSmarty(2, 5), "
                                                                  "ScrabbleAStarSmarty(2, 5)]")
group.add_argument("-m", "--mixies", action="store_true", help="One player of each type: [ScrabbleOneLook(), "
                                                               "LongestAStar(), ScrabbleOneLookTrial(2), "
                                                               "LongestOneLookSmarty(5, 2)]")
group.add_argument("-u", "--user", action="store_true", help="Default: User single-player.")

custom = setPlayers.add_parser(name="custom")
custom.add_argument("-ol", "--one-look-longest", action="count", default=0, help="Add 'One-Look Player(s)' with the "
                                                                                 "longest word heuristic.")
custom.add_argument("-os", "--one-look-scrabble", action="count", default=0, help="Add 'One-Look Player(s)' with the "
                                                                                  "scrabble score heuristic.")
custom.add_argument("-oh", "--one-look-shortest", action="count", default=0, help="Add 'One-Look Player(s)' with the "
                                                                                  "shortest word heuristic.")
custom.add_argument("-al", "--astar-longest", action="count", default=0, help="Add 'A* Player(s)' with the "
                                                                              "longest word heuristic.")
custom.add_argument("-as", "--astar-scrabble", action="count", default=0, help="Add 'A* Player(s)' with the "
                                                                               "scrabble score heuristic.")
custom.add_argument("-tol", "--trial-look-longest", action="count", default=0, help="Add 'One-Look Trial Player(s)' "
                                                                                    "with the longest word heuristic.")
custom.add_argument("-tos", "--trial-look-scrabble", action="count", default=0, help="Add 'One-Look Trial Player(s)' "
                                                                                     "with the scrabble score "
                                                                                     "heuristic.")
custom.add_argument("-tal", "--trial-astar-longest", action="count", default=0, help="Add 'A* Trial Player(s)' with "
                                                                                     "the longest word heuristic.")
custom.add_argument("-tas", "--trial-astar-scrabble", action="count", default=0, help="Add 'A* Trial Player(s)' with "
                                                                                      "the scrabble score heuristic.")
custom.add_argument("-sol", "--smart-look-longest", action="count", default=0, help="Add 'One-Look Smart Player(s)' "
                                                                                    "with the longest word heuristic.")
custom.add_argument("-sos", "--smart-look-scrabble", action="count", default=0, help="Add 'One-Look Smart Player(s)' "
                                                                                     "with the scrabble score "
                                                                                     "heuristic.")
custom.add_argument("-sal", "--smart-astar-longest", action="count", default=0, help="Add 'A* Smart Player(s)' with "
                                                                                     "the longest word heuristic.")
custom.add_argument("-sas", "--smart-astar-scrabble", action="count", default=0, help="Add 'A* Smart Player(s)' with "
                                                                                      "the scrabble score heuristic.")

parser.add_argument("-r", "--runs", type=int, default=0, help="Number of runs to simulate. Default: 0 --> "
                                                              "press space to start next game.")
parser.add_argument("-s", "--screen-size", type=int, default=800, help="Resize the game window to SCREEN_SIZE square "
                                                                       "pixels.")


def presets(args):
    runCount = args.runs
    screenSize = args.screen_size
    if args.mixies:
        mixies = [ScrabbleOneLook(), LongestAStar(),
                  ScrabbleOneLookTrial(2), LongestOneLookSmarty(5, 2)]
        return Bananagrams(mixies, runCount=runCount, screenSize=screenSize)
    elif args.smarties:
        smarties = [LongestOneLookSmarty(2, 5), LongestAStarSmarty(2, 5),
                    ScrabbleOneLookSmarty(2, 5), ScrabbleAStarSmarty(2, 5)]
        return Bananagrams(smarties, runCount=runCount, screenSize=screenSize)
    elif args.trialies:
        trialies = [LongestOneLookTrial(2), LongestOneLookTrial(3),
                    LongestOneLookTrial(4), LongestOneLookTrial(5)]
        return Bananagrams(trialies, runCount=runCount, screenSize=screenSize)
    elif args.starries:
        starries = [LongestAStar(), ScrabbleAStar()]
        return Bananagrams(starries, runCount=runCount, screenSize=screenSize)
    elif args.lookies:
        lookies = [LongestOneLook(), ScrabbleOneLook(), ShortestOneLook()]
        return Bananagrams(lookies, runCount=runCount, screenSize=screenSize)
    else:
        return Bananagrams(screenSize=screenSize)


def custom(args):
    runCount = args.runs
    screenSize = args.screen_size
    players = []
    for ol in range(args.one_look_longest):
        players.append(LongestOneLook())
    for os in range(args.one_look_scrabble):
        players.append(ScrabbleOneLook())
    for oh in range(args.one_look_shortest):
        players.append(ShortestOneLook())
    for al in range(args.astar_longest):
        players.append(LongestAStar())
    for as_ in range(args.astar_scrabble):
        players.append(ScrabbleAStar())
    for tol in range(args.trial_look_longest):
        players.append(LongestOneLookTrial(3))
    for tos in range(args.trial_look_scrabble):
        players.append(ScrabbleOneLookTrial(3))
    for tal in range(args.trial_astar_longest):
        players.append(LongestAStarTrial(2))
    for tas in range(args.trial_astar_scrabble):
        players.append(ScrabbleAStarTrial(2))
    for sol in range(args.smart_look_longest):
        players.append(LongestOneLookSmarty(5, 2))
    for sos in range(args.smart_look_scrabble):
        players.append(ScrabbleOneLookSmarty(5, 2))
    for sal in range(args.smart_astar_longest):
        players.append(LongestAStarSmarty(5, 2))
    for sas in range(args.smart_astar_scrabble):
        players.append(ScrabbleAStarSmarty(5, 2))
    return Bananagrams(players, runCount=runCount, screenSize=screenSize)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.setPlayers == "presets":
        game = presets(args)
    elif args.setPlayers == "custom":
        game = custom(args)
    else:
        game = Bananagrams(screenSize=args.screen_size)
else:
    # fill in with players, leave blank for user single player
    players = []
    game = Bananagrams(players)

game.newGame()
