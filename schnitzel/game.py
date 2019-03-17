from . import TransactionClient


# from .strategies import Strategy


class Game(object):
    def __init__(self, strategy: object, tournament: bool = False):
        self.strategy = strategy
        self.strategy.attach_game(self)
        self.login_response = None
        self.tournament = tournament
        self.client = None
        self.status = []

    def run(self):
        client = TransactionClient(log_game=True)
        self.client = client
        # Client login
        self.login_response = client.login(tournament=self.tournament)
        schnitzel_user = self.login_response['playerId']
        print(f'We are {schnitzel_user}')

        total_chips = None
        begin_hand = True
        token = None
        while begin_hand:
            # Begin hand (repeated)
            auction_or_summary = client.receive_response()

            if auction_or_summary is None:
                if token == 99:
                    print('Reached 100 hand limit... the server closed the TCP channel')
                else:
                    print('We lost?... the server closed the TCP channel.')
                client.close()
                return

            # End bet sequence
            if auction_or_summary['type'] == 'summary':
                summary = auction_or_summary

                # get another message: bankrupt if chips == 0
                # bankrupt = client.receive_response()
                break

            auction = auction_or_summary
            token = auction['token']

            # Make a bid for a superpower
            superpower_type, superpower_bid = self.strategy.superpower_bid()
            auction_result = client.auction_response(token, superpower_type, superpower_bid)

            # one per action of any player, or card dealt
            # TODO: should we expect more messages from the server?
            status = client.receive_response()

            if status['type'] == 'bankrupt':
                print('We lost... bankrupt')
                client.close()
                return

            # if we won or lost, then just leave
            if self.check_bankrupt(status) or self.check_win(status):
                client.close()
                return

            schnitzel_status = None
            for item in status['activePlayers']:
                if item['playerId'] == schnitzel_user:
                    schnitzel_status = item
                    break

            if 'roles' not in status:
                break

            roles = {v: k for k, v in status['roles'].items()}
            schnitzel_role = roles[schnitzel_user] if schnitzel_user in roles else None

            if total_chips is None:
                total_chips = len(status['activePlayers']) * 1000
            self.status.append(status)

            # Bet sequence (repeated until check/call/fold/raise)
            bet_sequence = True
            while bet_sequence:
                bet_or_status = client.receive_response()

                if bet_or_status['type'] == 'bankrupt':
                    print('We lost... bankrupt')
                    client.close()
                    return
                if bet_or_status['type'] == 'status':
                    status = bet_or_status
                    schnitzel_status = None
                    for item in status['activePlayers']:
                        if item['playerId'] == schnitzel_user:
                            schnitzel_status = item
                            break

                    # if we won or lost, then just leave
                    if self.check_bankrupt(status) or self.check_win(status):
                        client.close()
                        return
                    self.status.append(status)
                    continue

                if bet_or_status['type'] == 'summary':
                    summary = bet_or_status
                    bet_sequence = False

                    # get another message: bankrupt if chips == 0
                    # bankrupt = client.receive_response()
                    break

                bet = bet_or_status
                token = bet['token']

                action, stake, use_reserve = self.strategy.make_a_bet()
                client.bet_response(token, action, stake, use_reserve)

                # if action is a superpower
                if action in ['spy', 'seer', 'leech']:
                    superpower_response = client.receive_response()

            schnitzel_chips = schnitzel_status['chips']
            print(f'Finished hand {token}, chips: {schnitzel_chips} / {total_chips}')

        client.close()

    def check_bankrupt(self, status: dict) -> bool:
        playerId = self.login_response['playerId']

        for bankrupt_player in status['bankruptPlayers']:
            if bankrupt_player == playerId:
                print('You lost...')
                return True

        return False

    def check_win(self, status: dict) -> bool:
        playerId = self.login_response['playerId']

        is_it_a_win = len(status['activePlayers']) == 1 and \
            status['activePlayers'][0]['playerId'] == playerId

        if is_it_a_win:
            print('You won!!!!')
        return is_it_a_win
