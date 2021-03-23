import mysql.connector
import json
import traceback
from _thread import *
import time
import socket
from cryptography.fernet import Fernet
import movement_control as mvc

class Error(Exception):
    pass

class DataInvalid(Error):
    def __init__(self, data, index):
        self.data = data
        self.index = index

data_validation = [
(1, 1000), #    presssure value range
(1, 1000), #    temperature value range
(1, 1000), #    humidity value range
(1, 1000), #    gyro_x value range
(1, 1000), #    gyro_y value range
(1, 1000), #    gyro_z value range
(1, 1000), #    uv_index value range
(1, 1000), #    ir_light value range
(1, 1000), #    visible_light value range
(1, 1000), #    eco2 value range
(1, 1000)  #    tvoc value range
]

cfg = open("rover_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)


db_host = config["db_host"]
db_user = config["db_user"]
db_pass = config["db_pass"]
db = config["db"]
socket_host = config["server"]
socket_port = config["port"]
key = config["key"]

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db
)


mycursor = mydb.cursor(buffered=True)
crypto = Fernet(key)


def Forward(time):
    mvc.moveAtAngle(50, 0, time)

def Back(time):
    mvc.moveAtAngle(-50, 0, time)

def Right(time):
    mvc.turn(20, 1, time)

def Left(time):
    mvc.turn(20, 0, time)

def Camera_Up(value):
    mvc.camServo.write(value)

def Camera_Up(value):
    mvc.camServo.write(-value)

def control_loop(Socket):
    while True:
        try:
            print("Waiting for commands...")
            command = Socket.recv(1024)
            decrypted_message = crypto.decrypt(command)
            print(decrypted_message)
            if decrypted_message.decode() == "Ping":

                enc_message = crypto.encrypt(str.encode("Pong"))
                Socket.send(enc_message)
            else:
                Socket.send(command)
                print("Confirmation sent!")
                print(decrypted_message)
                eval(decrypted_message)
                enc_message = crypto.encrypt(str.encode(decrypted_message.decode()+";DN"))
                Socket.send(enc_message)
        except socket.timeout as e:
            print(str(e))
            socket_reconnect()



def socket_reconnect():
    print("Reconnecting to socket.")
    try:
        ClientSocket.connect((socket_host, socket_port))
        print("Starting control thread.")
        return ClientSocket
    except socket.error as e:
        print(str(e))
        return None



if __name__ == '__main__':
    mvc.init()
    ClientSocket = socket.socket()
    print("Connecting to socket.")
    try:
        ClientSocket.connect((socket_host, socket_port))
        ClientSocket.settimeout(5)
    except socket.error as e:
        print(str(e))
    print("Starting control thread.")
    control_loop(ClientSocket)
