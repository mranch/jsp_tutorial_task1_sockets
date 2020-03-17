import socket
# from server import IP, PORT
import pickle

IP = '127.0.0.1'
PORT = 1234
HEADER_SIZE = 10


class MakeDrinkCommand:
    def __init__(self, data):
        self._data = data
        self.dumped_data = pickle.dumps(self._data)
        self.data_size = len(self.dumped_data)

    def send(self, server_socket):
        server_socket.send(bytes(f"{self.data_size:<{HEADER_SIZE}}", "utf-8") + self.dumped_data)


# example of order
# {
#   drink: coffee

# optional:
#   add: milk
# }
def order_drink(order, sock):
    make_drink_command = MakeDrinkCommand(order)
    make_drink_command.send(sock)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    first_order = {
        "drink": "coffee",
        "add": "milk"
    }
    second_order = {
        "drink": "soda"
    }
    order_drink(first_order, s)
    while True:
        resp = s.recv(100)

        print(pickle.loads(resp))
