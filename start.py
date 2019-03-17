from schnitzel.strategies import *
from schnitzel import Game


game = Game(RandomWalk(), tournament=False)
game.run()
print('End')
