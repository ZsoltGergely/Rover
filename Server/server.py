import socket
import os
from _thread import *
import time
import json
import sys
from cryptography.fernet import Fernet


cfg = open("server_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)
commands = []
id = 0

client_port = config["client_port"]
rover_port = config["rover_port"]
key = config["key"]

host = '0.0.0.0'
rover_host = '0.0.0.0'
ThreadCount = 0
ClientSocket = socket.socket()
RoverSocket = socket.socket()
crypto = Fernet(key)

Valid_commands =[
"Forward()",
"Back()",
"Left()",
"Right()",
"Arm_up()",
"Arm_down()",
"Arm_Forward()",
"Arm_Back()",
"Arm_Left()",
"Arm_Right()",
"setCam()",
"setArm()"
]

def line_valid(command):
    print(command)
    split = command.split("(")
    print("Trying: " + split[0]+"()")
    if split[0]+"()" in Valid_commands:
        if split[0]+"()" == "setArm()":
            return True
        else:
            try:
                int(split[1][:-1])
                return True
            except ValueError:
                return False

class Command_class:
    def __init__(self, id, command):
        self.id = id
        self.command = command

    def execute(self, rover_connection):
        try:
            enc_message = crypto.encrypt(str.encode(self.command))
            rover_connection.sendall(enc_message)
            print("Sent: " + self.command)
            data = rover_connection.recv(2048)
            print(crypto.decrypt(data))
            decrypted_message = crypto.decrypt(data)
            print ("Confirmation received: " + str(decrypted_message))
            if decrypted_message.decode() == self.command:
                confirmation = rover_connection.recv(2048)
                decrypted_conf = crypto.decrypt(confirmation)
                print ("Command execution received: " + decrypted_conf.decode())
                if decrypted_conf.decode() == self.command+ ";DN" :
                    return True
                else:
                    print("execution not matching")
                    return False
            else:
                print("decrypted_message not matching")
                return False

        except socket.error:
            print ("Rover down")
            sys.exit()

def Ping(Socket):
    while True:
        time.sleep(3)
        print("Pinging rover...")
        enc_message = crypto.encrypt(str.encode("Ping"))
        Socket.send(enc_message)
        answer = Socket.recv(1024)
        decrypted_message = crypto.decrypt(answer)
        print(decrypted_message.decode())

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

def client_session(client_connection):
    client_connection.send(str.encode('Server is working:'))
    global id
    while True:
        data = client_connection.recv(2048)
        data_str = data.decode('utf-8')
        # print(data_str)
        if not data:
            break
        else:
            if data_str[:3] == "FL;":
                lines = data_str.split(";")
                lines.remove("FL")
                lines.remove("")
                for line in lines:
                    if line_valid(line): #if command is valid
                        commands.append(Command_class(id, line))
                        id += 1
                        enc_message = crypto.encrypt(str.encode(line))
                        client_connection.sendall(enc_message)
                    else:
                        enc_message = crypto.encrypt(str.encode("DATA INVALID : " + line))
                        client_connection.sendall(enc_message)

                print(lines)
            else:
                if line_valid(data_str): #if command is valid
                    commands.append(Command_class(id, data_str))
                    id += 1
                    enc_message = crypto.encrypt(str.encode(data_str))
                    client_connection.sendall(enc_message)
                else:
                    enc_message = crypto.encrypt(str.encode("DATA INVALID : " + data_str))
                    client_connection.sendall(enc_message)
    client_connection.close()


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
        start_new_thread(send_commands, (Rover, ))
        start_new_thread(Ping, (Rover, ))


def send_commands(rover_connection):
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
                    while command.execute(rover_connection) != True:
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
