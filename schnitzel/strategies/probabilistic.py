from ..game import Game
from .decisionmaker import *
from treys import Card


class Probabilistic(object):
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
        latest_status = self.game.status[-1]
        schnizel_userId = self.game.login_response['playerId']
        schnizel_player = None
        for player in latest_status['activePlayers']:
            if player['playerId'] == schnizel_userId:
                schnizel_player = player

        pocket_cards = latest_status['pocketCards']
        community_cards = latest_status['communityCards']


        community = [Card.new('Ah'), Card.new('2d'), Card.new('Tc')]
        hand = [Card.new('As'), Card.new('3c')]
        bidAmount = int(latest_status['stake']) - int(schnizel_player['stake'])
        currentMoney = schnizel_player['chips']

        action, amount = decision(community, hand, bidAmount, currentMoney)
        return action, amount, False
