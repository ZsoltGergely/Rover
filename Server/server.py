import socket
import os
from _thread import *
import time
import json

cfg = open("server_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)


port = config["port"]
host = '0.0.0.0'
ThreadCount = 0

ServerSideSocket = socket.socket()

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        data_str = data.decode('utf-8')
        print(data_str)
        if not data:
            break

        connection.sendall(str.encode(data_str))
    connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
