from ..game import Game
from .decisionmaker import *
from treys import Card
import traceback


class Probabilistic(object):
    def __init__(self):
        self.game = None

    def attach_game(self, game: Game):
        self.game = game

    def get_superpowers(self) -> dict:
        return self.game.superpowers

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

        hand = []
        community = []
        for pocket_card in pocket_cards:
            card_name = pocket_card['rank'].upper()[0] + pocket_card['suit'][0]
            if card_name[0] == '1':
                card_name = 'T' + card_name[1]
            hand.append(Card.new(card_name))

        for community_card in community_cards:
            card_name = community_card['rank'].upper()[0] + community_card['suit'][0]
            if card_name[0] == '1':
                card_name = 'T' + card_name[1]
            community.append(Card.new(card_name))

        # community = [Card.new('Jh'), Card.new('Ad'), Card.new('3s')]
        # hand = [Card.new('4s'), Card.new('Jc')]
        bidAmount = max(int(latest_status['stake']) - int(schnizel_player['stake']), 10)
        currentMoney = schnizel_player['chips']


        try:
            action, amount = decision(community, hand, bidAmount, currentMoney)
            print(f'Choosing {action}, and putting {amount}')
        except Exception as e:
            print(traceback.format_exc())
            print('Decision issue')
            return 'raise', bidAmount, False
        return action, amount, False
