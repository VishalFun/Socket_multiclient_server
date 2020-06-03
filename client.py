import socket
from encryption import Encryption

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8080

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))


cipher_tool = Encryption()
Input = input('Enter message: ')
ClientSocket.send(cipher_tool.encrypt_message(Input))
Response = ClientSocket.recv(1024)
res = (cipher_tool.decrypt_message(Response))
print(res)
ClientSocket.close()
