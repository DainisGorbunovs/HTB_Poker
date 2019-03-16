import json
from schnitzel import TransactionClient


client = TransactionClient(log_game=True)
# Client login
login_response = client.login()

# Begin hand (repeated)
auction = client.receive_response()

auction_result = client.auction_response()

status = client.receive_response()

# Bet sequence (repeated until check/call/fold/raise)
bet = client.receive_response()

client.bet_response()

client.close()

