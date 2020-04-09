import socket
import pickle
import time
import os

IP = '127.0.0.1'
PORT = 1234
HEADER_SIZE = 10


class CoffeeMachineCommand:
    def __init__(self, data):
        self._data = data
        self.dumped_data = pickle.dumps(self._data)
        self.data_size = len(self.dumped_data)

    def send(self, server_socket):
        server_socket.send(bytes(f"{self.data_size:<{HEADER_SIZE}}", "utf-8") + self.dumped_data)


def submit_order(order, sock):
    make_drink_command = CoffeeMachineCommand(
        {
            "command type": "order drink",
            "data": order
        }
    )
    make_drink_command.send(sock)


def check_history(sock):
    check_history_command = CoffeeMachineCommand(
        {
            "command type": "check history"
        }
    )
    check_history_command.send(sock)
    received_response = s.recv(1000)
    resp = pickle.loads(received_response)
    for order in resp['message']:
        print(order)


def check_resources(sock):
    check_resources_command = CoffeeMachineCommand(
        {
            "command type": 'check resources'
        }
    )
    check_resources_command.send(sock)
    received_response = s.recv(1000)
    resp = pickle.loads(received_response)
    goods = resp['message']
    print("Here are the drinks that are left:")
    for drink in goods['drinks']:
        print(f"{drink[1]} items of {drink[0]}")
    print("Here are the adds that are left:")
    for add in goods['adds']:
        print(f"{add[1]} items of {add[0]}")


def order_drink(sock):
    user_order = {}
    drink = input("Which drink do you want?\n")
    add = input("If you want an add, please enter it here. If not, please hit Enter.\n")
    user_order['drink'] = drink
    resp = "Ordering " + drink
    if add:
        user_order['add'] = add
        resp += f" with {add}"
    resp += ", please wait..."
    print(resp)
    time.sleep(1)
    submit_order(user_order, sock)
    received_response = sock.recv(100)
    response = pickle.loads(received_response)
    print(response['message'])
    if response['status code'] == 201:
        print('Please wait...')
        time.sleep(5)
        print('Your drink is ready!')


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    while True:
        try:
            user_choice = int(input("""Please choose one of the following options:
    1. Order a drink
    2. Check order history
    3. Check remaining resources
    4. Quit\n"""))
        except ValueError:
            print("Wrong input! Try again")
        else:
            if user_choice == 1:
                order_drink(s)
            elif user_choice == 2:
                check_history(s)
            elif user_choice == 3:
                check_resources(s)
            elif user_choice == 4:
                exit()
            else:
                print("We do not have so much options yet or you input wrong number! :)")
        time.sleep(3)
        print('\n' * 100)