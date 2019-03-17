from schnitzel.strategies import *
from schnitzel import Game


# game = Game(RandomWalk(), tournament=False)
game = Game(Probabilistic(), tournament=True)
game.run()
print('End')
