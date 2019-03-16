from ..game import Game


class Strategy(object):
    def __init__(self):
        self.game = None

    def superpower_bid(self):
        pass

    def attach_game(self, game: Game):
        self.game = game
