class Taco:
    def __str__(self):
        return "taco"


t = Taco()

if type(t) == Taco:
    print("yes")
