import socket
import pickle
import my_sqlite_db

IP = '127.0.0.1'
PORT = 1234
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
current_order_id = 1
orders = []


def update_order_list(drink, add=None):
    global current_order_id
    order_info = {
            "order id": current_order_id,
            "order content": {
                "drink": drink
            }
        }
    if add:
        order_info['order content']['add'] = add
    orders.append(order_info)
    current_order_id += 1

    # my_sqlite_db
    my_sqlite_db.create_order(drink, add)


class MakeDrinkException(Exception):
    def __init__(self, message):
        self.message = message


def make_drink(drink, add=None):
    goods['drinks'][drink] -= 1
    if add:
        goods['adds'][add] -= 1

    # sqlite3 db
    my_sqlite_db.make_drink(drink, add)


def send_response(status_code, message):
    return {
        "status code": status_code,
        "message": message
    }


def process_order(data):
    try:
        if 'drink' not in data:
            raise MakeDrinkException("You did not order a drink!")
        elif data['drink'] not in goods['drinks']:
            raise MakeDrinkException("Some unknown drink!")
        elif goods['drinks'][data['drink']] == 0:
            raise MakeDrinkException("You are late! No such drink left!")
        else:
            message = f"You successfully ordered {data['drink']}"
            if 'add' not in data:
                make_drink(data['drink'])
                update_order_list(data['drink'])
            else:
                if data['add'] not in goods['adds']:
                    raise MakeDrinkException("Some unknown add!")
                elif goods['adds'][data['add']] == 0:
                    raise MakeDrinkException("No such add left!")
                else:
                    make_drink(data['drink'], data['add'])
                    update_order_list(data['drink'], data['add'])
                    message += f" with {data['add']}"
            message += "!"
    except MakeDrinkException as e:
        return send_response(404, e.message)
    else:
        return send_response(201, message)


def check_history():
    for order in orders:
        print(order)
    return send_response(202, orders)


def receive_command(client_sock):
    message = client_sock.recv(200)
    message_len = int(message[:HEADER_SIZE])
    print(f"Message_len {message_len}")
    message = pickle.loads(message[HEADER_SIZE:])
    print(message)
    if message['command type'] == 'order drink':
        return process_order(message['data'])
    elif message['command type'] == 'check history':
        return check_history()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    s.listen(50)

    while True:
        client_socket, address = s.accept()
        received_command = receive_command(client_socket)
        print("PPPPPPPPPPPPPPPPPPPPPP")
        print(received_command)
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        resp = pickle.dumps(received_command)
        client_socket.send(resp)
