from .transaction_client import send_request


def login(tournament: bool = False, player: str = 'schnitzel'):
    return send_request({
        # Always “login”
        'type': 'login',

        # Your allocated player name
        'player': player,

        # True if the connection wants to join the next tournament, otherwise false
        'tournament': tournament
    })


def auction_response(token: int = 0, super_power: str = None, bid: int = 0):
    response = {
        # Always “auction_response”
        'type': 'auction_response',

        # The value from the Auction message
        'token': token
    }

    # Optional
    if super_power:
        # The name of the super power being bid for.
        response['superPower'] = super_power

        # The number of chips to bid in the auction
        response['bid'] = bid

    return send_request(response)


def bet_response(token: int = 0, action: str = 'fold',
                 stake: int = None, use_reserve: bool = False):
    response = {
        # Always “bet_response”
        'type': 'bet_response',

        # The value from the Bet message
        'token': token,

        # Either a game action (check, call, raise, fold)
        # or a super power to use (spy, seer, leech)
        'action': action,

        # True to allow use of reserve chips or super powers if
        # the main counts are insufficient
        'use_reserve': use_reserve
    }

    if action == 'raise':
        # Required when action is raise. The number of chips
        # to raise by (excluding the chips required to call).
        response['stake'] = stake

    return send_request(response)

