from . import TransactionClient
# from .strategies import Strategy


class Game(object):
    def __init__(self, strategy: object):
        self.strategy = strategy
        self.strategy.attach_game(self)
        self.login_response = None

    def run(self):
        client = TransactionClient(log_game=True)
        # Client login
        self.login_response = client.login()

        begin_hand = True
        while begin_hand:
            # Begin hand (repeated)
            auction = client.receive_response()
            token = auction['token']

            # Make a bid for a superpower
            superpower_type, superpower_bid = self.strategy.superpower_bid()
            auction_result = client.auction_response(token, superpower_type, superpower_bid)

            # one per action of any player, or card dealt
            # TODO: should we expect more messages from the server?
            status = client.receive_response()

            # Bet sequence (repeated until check/call/fold/raise)
            bet = client.receive_response()

            client.bet_response()
            begin_hand = False

        client.close()
