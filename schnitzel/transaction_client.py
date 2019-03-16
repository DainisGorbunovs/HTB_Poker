import socket
import json
import uuid
import os

HOST, PORT = "35.197.236.148", 9877


class TransactionClient(object):
    def __init__(self, log_game: bool = False):
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server and send data
        self.sock.connect((HOST, PORT))

        self.log_game = log_game
        self.message_log = []

    # close sock when destructor is ran
    def close(self):
        self.sock.close()
        # Save to a game with a unique UUID.json
        filename = 'games/' + str(uuid.uuid4()) + '.json'

        if not os.path.exists('games'):
            os.makedirs('games')

        with open(filename, 'w') as outfile:
            json.dump(self.message_log, outfile)

    # request_message is a dict (key = field name)
    def send_request(self, request_message: dict) -> dict:
        if self.log_game:
            self.message_log.append(('Schnitzel Bot', request_message))
        request_bytes = json.dumps(request_message).encode('utf-8')

        # Send the request
        request_length_bytes = len(request_bytes).to_bytes(4, 'little')
        self.sock.sendall(request_length_bytes)
        self.sock.sendall(request_bytes)

        return self.receive_response()

    def receive_response(self) -> dict or None:
        # Receive data from the server and shut down
        response_length_bytes = self.sock.recv(4)
        response_length = int.from_bytes(response_length_bytes, 'little')

        if response_length == 0:
            return None

        received_json = str(self.sock.recv(response_length), 'utf-8')
        received_dict = json.loads(received_json)

        if self.log_game:
            self.message_log.append(('Server', received_dict))
        return received_dict

    #####
    # Texas Holdem commands
    #####
    def login(self, tournament: bool = False, player: str = 'schnitzel') -> dict:
        return self.send_request({
            # Always “login”
            'type': 'login',

            # Your allocated player name
            'player': player,

            # True if the connection wants to join the next tournament, otherwise false
            'tournament': tournament
        })

    def auction_response(self, token: int = 0, super_power: str = None,
                         bid: int = 0) -> dict:
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

    # server replies back, if we use a superpower
    def bet_response(self, token: int = 0, action: str = 'fold',
                     stake: int = 0, use_reserve: bool = False) -> dict or None:
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
