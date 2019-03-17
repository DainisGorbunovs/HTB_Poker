from ..game import Game


class RandomWalk(object):
    def __init__(self):
        self.game = None
        self.our_bet = 100

    def attach_game(self, game: Game):
        self.game = game

    # auction_response
    def superpower_bid(self):
        return None, 0

    # bet_response
    def make_a_bet(self):
        # action, stake, use_reserve
        return 'raise', self.our_bet, False
