import socket
# from server import IP, PORT
import pickle

IP = '127.0.0.1'
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))
d = {
    "first": 1
}
d = pickle.dumps(d)
s.send(d)
