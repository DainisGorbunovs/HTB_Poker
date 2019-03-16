from . import TransactionClient
# from .strategies import Strategy


class Game(object):
    def __init__(self, strategy: object):
        self.strategy = strategy
        self.strategy.attach_game(self)
        self.login_response = None
        self.summary = None
        self.bankrupt = None

    def run(self):
        client = TransactionClient(log_game=True)
        # Client login
        self.login_response = client.login()

        begin_hand = True
        while begin_hand:
            # Begin hand (repeated)
            auction_or_summary = client.receive_response()

            # End bet sequence
            if auction_or_summary['type'] == 'summary':
                self.summary = auction_or_summary

                # get another message: bankrupt if chips == 0
                self.bankrupt = client.receive_response()
                break

            auction = auction_or_summary
            token = auction['token']

            # Make a bid for a superpower
            superpower_type, superpower_bid = self.strategy.superpower_bid()
            auction_result = client.auction_response(token, superpower_type, superpower_bid)

            # one per action of any player, or card dealt
            # TODO: should we expect more messages from the server?
            status = client.receive_response()

            # Bet sequence (repeated until check/call/fold/raise)
            bet_sequence = True
            while bet_sequence:
                bet_or_status = client.receive_response()

                if bet_or_status['type'] == 'status':
                    status = bet_or_status
                    continue

                bet = bet_or_status
                token = bet['token']

                action, stake, use_reserve = self.strategy.make_a_bet()
                client.bet_response(token, action, stake, use_reserve)

                # if action in ['check', 'call', 'fold', 'raise']:
                #     bet_sequence = False

        client.close()
