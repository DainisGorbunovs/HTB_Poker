from . import TransactionClient
# from .strategies import Strategy
from .card_convert import CardConvert
import logging


class Game(object):
    def __init__(self, strategy: object, tournament: bool = False):
        logging.basicConfig(level=logging.DEBUG)
        self.strategy = strategy
        self.login_response = None
        self.tournament = tournament
        self.client = None
        self.status = []
        self.superpowers = {}
        self.leeched = []
        self.spied = []
        self.strategy.attach_game(self)

    def run(self):
        client = TransactionClient(log_game=True)
        self.client = client
        # Client login
        self.login_response = client.login(tournament=self.tournament)
        self.superpowers = self.login_response['superPowers']
        begin_chips = self.login_response['chips']
        blinds_initial_value = self.login_response['blinds']['initialValue']
        stable_hand_count = self.login_response['blinds']['stableHandCount']
        growth_rate = self.login_response['blinds']['growthRate']
        seer = self.superpowers['seer']
        spy = self.superpowers['spy']
        leech = self.superpowers['leech']

        reserve_seer = self.login_response['superPowersReserve']['seer']
        reserve_spy = self.login_response['superPowersReserve']['spy']
        reserve_leech = self.login_response['superPowersReserve']['leech']

        reserve_chips = self.login_response['chipsReserve']
        tournaments_scores = self.login_response['tournamentsScores']

        logging.debug(f'LOGIN_RESPONSE: chips: {begin_chips}, blinds (value: {blinds_initial_value}, '
                      f'stable hand count: {stable_hand_count}, growth rate: {growth_rate})')
        logging.debug(f'Superpowers: {seer} seer, {spy} spy, {leech} leech. '
                      f'Reserved: {reserve_seer} seer, {reserve_spy} spy, {reserve_leech} leech.')
        logging.debug(f'{reserve_chips} reserve chips, {tournaments_scores} tournaments scores.')

        schnitzel_user = self.login_response['playerId']
        logging.debug(f'We are {schnitzel_user}')



        total_chips = None
        begin_hand = True
        token = None

        while begin_hand:
            # Begin hand (repeated)
            auction = client.receive_response()

            if auction is None:
                if token == 99:
                    logging.warning('Reached 100 hand limit... the server closed the TCP channel')
                else:
                    logging.warning('Unknown result... the server closed the TCP channel.')
                client.close()
                return

            # auction = auction
            token = auction['token']

            # Make a bid for a superpower
            superpower_type, superpower_bid = self.strategy.superpower_bid()
            auction_result = client.auction_response(token, superpower_type, superpower_bid)
            won_superpower = auction_result['superPower'] if auction_result['superPower'] is not None else 'none'
            logging.debug(f'[AUCTION_RESULT] We won: {won_superpower}.')
            self.leeched = []
            self.spied = []

            # one status per action of any player, or card dealt
            # Bet sequence (repeated until check/call/fold/raise)
            bet_sequence = True
            while bet_sequence:
                response = client.receive_response()

                if response['type'] == 'status':
                    self.status.append(response)
                    self.superpowers = response['superPowers']
                    current_player, stake, pot = response['currentPlayer'], int(response['stake']), response['pot']
                    current_player = 'SCHNITZEL BOT' if current_player == schnitzel_user else current_player
                    community_cards = CardConvert.convert_cards(response['communityCards'])
                    pocket_cards = CardConvert.convert_cards(response['pocketCards'])
                    logging.debug(f'STATUS [{token}, {current_player}]: stake: {stake}, pot: {pot},'
                          f' community cards: {community_cards}, pocket_cards: {pocket_cards}')
                elif response['type'] == 'bet':
                    logging.debug(f'BET [{token}]')
                    action, stake, use_reserve = self.strategy.make_a_bet()
                    token = response['token']

                    logging.debug(f'BET_RESPONSE [{token}]: action: {action}, stake: {stake}, use reserve: {use_reserve}')
                    client.bet_response(token, action, stake, use_reserve)

                    # if action is a superpower
                    if action in ['spy', 'seer', 'leech']:
                        logging.debug(f'Received SuperPower response: {token}')
                        superpower_response = client.receive_response()
                        card = CardConvert.convert_cards([superpower_response['card']])
                        logging.debug(f'SUPER_POWER [{token}]: card: {card}')
                        if action == 'leech':
                            self.leeched.append(card)
                        elif action == 'spy':
                            self.spied.append(card)
                elif response['type'] == 'summary':
                    hand = response['hand']
                    winners = response['winners']
                    logging.debug(f'SUMMARY [{token}]: hand: {hand}')
                    for winner in winners:
                        playerId = winner['playerId']
                        chips = winner['chips']
                        best_hand = CardConvert.convert_cards(winner['bestHand'])
                        logging.debug(f'[summary] winner {playerId}, chips: {chips}, best hand {best_hand}')
                    break
                elif response['type'] == 'bankrupt':
                    hand = response['hand']
                    logging.info(f'BANKRUPT [{token}]: hand: {hand}')
                    begin_hand = False

            if total_chips is None:
                total_chips = self.get_total_chips()
            schnitzel_chips = self.get_schnitzel_chips()

            if self.has_schnitzel_won():
                logging.info(f'WON [{token}] chips: {schnitzel_chips} / {total_chips}')
                break

            logging.info(f'Finished hand {token}, chips: {schnitzel_chips} / {total_chips}')

        client.close()

    def get_schnitzel_chips(self) -> int:
        chip_count = 0
        for player in self.status[-1]['activePlayers']:
            if player['playerId'] == self.login_response['playerId']:
                return player['chips']
        return int(chip_count)

    def get_total_chips(self) -> int:
        chip_count = 0
        for player in self.status[0]['activePlayers']:
            chip_count += player['chips'] + player['stake']
        return int(chip_count)

    def has_schnitzel_won(self) -> bool:
        active_players = self.status[-1]['activePlayers']
        return len(active_players) == 1 and active_players[0]['playerId'] == self.login_response['playerId']
