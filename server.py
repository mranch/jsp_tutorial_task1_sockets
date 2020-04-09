import socket
import pickle
import my_sqlite_db

IP = '127.0.0.1'
PORT = 1234
HEADER_SIZE = 10


def update_order_list(drink, add=None):
    my_sqlite_db.create_order(drink, add)


class MakeDrinkException(Exception):
    def __init__(self, message):
        self.message = message


def make_drink(drink, add=None):
    my_sqlite_db.make_drink(drink, add)


def send_response(status_code, message):
    return {
        "status code": status_code,
        "message": message
    }


def process_order(data):
    try:
        drinks = my_sqlite_db.get_drinks()
        adds = my_sqlite_db.get_additions()
        if 'drink' not in data:
            raise MakeDrinkException("You did not order a drink!")
        elif data['drink'] not in [drink[0] for drink in drinks]:
            raise MakeDrinkException("Some unknown drink!")
        else:
            for drink in drinks:
                if data['drink'] == drink[0]:
                    drink_name, drink_amount = drink
            if drink_amount == 0:
                raise MakeDrinkException("You are late! No such drink left!")
            else:
                message = f"You successfully ordered {drink_name}"
                if 'add' not in data:
                    make_drink(drink_name)
                    update_order_list(drink_name)
                else:
                    if data['add'] not in [add[0] for add in adds]:
                        raise MakeDrinkException("Some unknown add!")
                    else:
                        for add in adds:
                            if data['add'] == add[0]:
                                add_name, add_amount = add
                        if add_amount == 0:
                            raise MakeDrinkException("No such add left!")
                        else:
                            make_drink(drink_name, add_name)
                            update_order_list(drink_name, add_name)
                            message += f" with {add_name}"
                    message += "!"
    except MakeDrinkException as e:
        return send_response(404, e.message)
    else:
        return send_response(201, message)


def check_history():
    order_history = my_sqlite_db.check_history()
    return send_response(202, order_history)


def check_resources():
    resources = my_sqlite_db.check_resources()
    return send_response(203, resources)


def check_resources():
    return send_response(203, goods)


def receive_command(client_sock):
    message = client_sock.recv(200)
    message_len = int(message[:HEADER_SIZE])
    message = pickle.loads(message[HEADER_SIZE:])
    if message['command type'] == 'order drink':
        return process_order(message['data'])
    elif message['command type'] == 'check history':
        return check_history()
    elif message['command type'] == 'check resources':
        return check_resources()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(50)

    while True:
        client_socket, address = s.accept()
        received_command = receive_command(client_socket)
        resp = pickle.dumps(received_command)
        client_socket.send(resp)
