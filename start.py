import json
from schnitzel import TransactionClient

client = TransactionClient()

# Client login
login_response = client.login()

# Begin hand
auction = client.receive_response()

auction_result = client.auction_response()

status = client.receive_response()

print(json.dumps(login_response, indent=4, sort_keys=True))
