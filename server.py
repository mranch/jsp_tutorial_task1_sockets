import socket
import pickle

IP = '127.0.0.1'
PORT = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)

while True:
    client_socket, address = s.accept()
    message = client_socket.recv(100)
    print(pickle.loads(message))
