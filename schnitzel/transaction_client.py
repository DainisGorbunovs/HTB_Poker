import socket
import json

HOST, PORT = "35.197.236.148", 9877


class TransactionClient(object):
    def __init__(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server and send data
        self.sock.connect((HOST, PORT))

    # close sock when destructor is ran
    def __del__(self):
        self.sock.close()

    # request_message is a dict (key = field name)
    def send_request(self, request_message: dict) -> dict:
        request_bytes = json.dumps(request_message).encode('utf-8')

        # Send the request
        request_length_bytes = len(request_bytes).to_bytes(4, 'little')
        self.sock.sendall(request_length_bytes)
        self.sock.sendall(request_bytes)

        return self.receive_response()

    def receive_response(self):
        # Receive data from the server and shut down
        response_length_bytes = self.sock.recv(4)
        response_length = int.from_bytes(response_length_bytes, 'little')

        if response_length == 0:
            return None

        received_json = str(self.sock.recv(response_length), 'utf-8')
        received_dict = json.loads(received_json)
        return received_dict

    def login(self, tournament: bool = False, player: str = 'schnitzel'):
        return self.send_request({
            # Always “login”
            'type': 'login',

            # Your allocated player name
            'player': player,

            # True if the connection wants to join the next tournament, otherwise false
            'tournament': tournament
        })

    def auction_response(self, token: int = 0, super_power: str = None, bid: int = 0):
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

        return self.send_request(response)

    def bet_response(self, token: int = 0, action: str = 'fold',
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

        return self.send_request(response)
