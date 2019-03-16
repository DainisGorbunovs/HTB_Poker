import socket
import sys
import json

HOST, PORT = "35.197.236.148", 9877

login = {
    'type': 'login',
    'player': 'schnitzel',
    'tournament': False
}

b = json.dumps(login).encode('utf-8')

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # sock.sendall(bytes(login + "\n", "utf-8"))
    length = len(b).to_bytes(4, 'little')
    sock.sendall(length)
    sock.sendall(b)

    # Receive data from the server and shut down
    newlength = sock.recv(4)
    newlength_int = int.from_bytes(newlength, 'little')


    received_json = str(sock.recv(newlength_int), "utf-8")
    received_dict = json.loads(received_json)
    print(json.dumps(received_dict, indent=4, sort_keys=True))

