import socket
import json

HOST, PORT = "35.197.236.148", 9877


# message is a dict (key = field name)
def send_request(request_message: dict) -> dict:
    request_bytes = json.dumps(request_message).encode('utf-8')

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        # Send the request
        request_length_bytes = len(request_bytes).to_bytes(4, 'little')
        sock.sendall(request_length_bytes)
        sock.sendall(request_bytes)

        # Receive data from the server and shut down
        response_length_bytes = sock.recv(4)
        response_length = int.from_bytes(response_length_bytes, 'little')

        received_json = str(sock.recv(response_length), 'utf-8')
        received_dict = json.loads(received_json)
        return received_dict
