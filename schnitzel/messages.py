from .transaction_client import send_request


def login(tournament: bool = False, player: str = 'schnitzel'):
    return send_request({
        'type': 'login',
        'player': player,
        'tournament': tournament
    })
