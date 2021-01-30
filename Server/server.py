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
rover_host = '127.0.0.1'
ThreadCount = 0
ClientSocket = socket.socket()
RoverSocket = socket.socket()

class Command_class:
    def __init__(self, id, command):
        self.id = id
        self.command = command

    def execute(self, connection):
        connection.sendall(str.encode(self.command))
        print("Sent: " + self.command)
        data = connection.recv(2048)
        data_str = data.decode('utf-8')
        print ("Received: " + data_str)
        if data_str == self.command:
            return True
        else:
            return False
        print("------------")

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


def start_sockets():
    try:
        ClientSocket.bind((host, client_port))
    except socket.error as e:
        print(str(e))

    print('Client Socket is listening..')
    ClientSocket.listen(5)

    try:
        RoverSocket.bind((host, rover_port))
    except socket.error as e:
        print(str(e))

    print('Rover Socket is listening..')
    RoverSocket.listen(5)

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
        Client, client_address = ClientSocket.accept()
        print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
        start_new_thread(client_session, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))

def handle_rover():
    while True:
        Rover, rover_address = RoverSocket.accept()
        print('Rover connected from: ' + rover_address[0] + ':' + str(rover_address[1]))
        start_new_thread(execute_commands, (Rover, ))


def execute_commands(connection):
    while True:
        id_list = []
        if len(commands)!= 0:
            for command in commands:
                id_list.append(command.id)
            for command in commands:
                if command.id == min(id_list):
                    print("Running command with id: " + str(command.id))
                    tries = 0
                    # command.execute(connection)
                    while command.execute(connection) != True:
                        tries += 1
                        if tries == 5:
                            print("Transfer unsuccessfull: " + str(command))
                    commands.remove(command)




if __name__ == '__main__':
    start_sockets()
    start_new_thread(handle_clients, ())
    handle_rover()


    ClientSocket.close()
    RoverSocket.close()
