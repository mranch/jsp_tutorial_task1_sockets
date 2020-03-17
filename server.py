import socket
import pickle
from functools import reduce

IP = '127.0.0.1'
PORT = 1234
drinks = ['coffee', 'water', 'soda']
adds = ['milk', 'sugar']
HEADER_SIZE = 10
goods = {
    "drinks": {
        "coffee": 10,
        "water": 20,
        "soda": 30
    },
    "adds": {
        "milk": 7,
        "sugar": 8
    }
}


def receive_order(client_sock):
    message = client_sock.recv(100)
    message_len = int(message[:HEADER_SIZE])
    print(f"Message_len {message_len}")
    message = pickle.loads(message[HEADER_SIZE:])
    print(message)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(5)

    while True:
        client_socket, address = s.accept()
        receive_order(client_socket)
        # resp = bytes(f"'you sent': {message}", "utf-8")
        # resp = pickle.dumps(resp)
        # client_socket.send(resp)
