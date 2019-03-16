from ..game import Game


class RandomWalk(object):
    def __init__(self):
        self.game = None

    def superpower_bid(self):
        return None, 0

    def attach_game(self, game: Game):
        self.game = game
