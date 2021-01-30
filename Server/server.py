import socket
import os
from _thread import *
import time
import json

cfg = open("server_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)
commands = []
id = 0

client_port = config["client_port"]
rover_port = config["rover_port"]
host = '0.0.0.0'
ThreadCount = 0
ClientSocket = socket.socket()

class Command_class:
    def __init__(self, id, command):
        self.id = id
        self.command = command

    def execute(self):
        eval(self.command)


def Forward():
    print("Going forward 10")
    time.sleep(10)
    print("------------")
def Back():
    print("Going back 0")
    print("------------")
def Left():
    print("Going left 5")
    time.sleep(5)
    print("------------")
def Right():
    print("Going Right 2")
    time.sleep(2)
    print("------------")


def start_socket():
    try:
        ClientSocket.bind((host, client_port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening..')
    ClientSocket.listen(5)

def client_session(connection):
    connection.send(str.encode('Server is working:'))
    global id
    while True:
        data = connection.recv(2048)
        data_str = data.decode('utf-8')
        # print(data_str)
        if not data:
            break
        else:
            if 1==1: #if command is valid
                commands.append(Command_class(id, data_str))
                id += 1
                connection.sendall(str.encode(data_str))
            else:
                connection.sendall("DATA INVALID : " + str.encode(data_str))
    connection.close()

def handle_clients():
    global ThreadCount
    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(client_session, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

def execute_commands():
    while True:
        id_list = []
        if len(commands)!= 0:
            for command in commands:
                id_list.append(command.id)
            for command in commands:
                if command.id == min(id_list):
                    print("Running command with id: " + str(command.id))
                    command.execute()
                    commands.remove(command)



if __name__ == '__main__':
    start_socket()
    start_new_thread(handle_clients, ())
    execute_commands()
    ServerSideSocket.close()
