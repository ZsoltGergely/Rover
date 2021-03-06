import mysql.connector
import json
import traceback
from _thread import *
import time
import socket
from cryptography.fernet import Fernet
import serial
# random
from random import seed
from random import randint
# random

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



def read_data(serial_connection):
    line = ser.readline()
    if line[:1] == "*" and line[-2:-1]:
        line.replace("*", "")
        elements = line.split(";")
        for index, value in enumerate(elements):
            if not (value > data_validation[index][0] and value < data_validation[index][1]):
                raise DataInvalid(value, index)

        presssure = elements[0]
        temperature = elements[1]
        humidity = elements[2]
        gyro_x = elements[3]
        gyro_y = elements[4]
        gyro_z = elements[5]
        uv_index = elements[6] 
        ir_light = elements[7]
        visible_light = elements[8]
        eco2 = elements[9]
        tvoc = elements[10]

    return presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc


def upload_loop():
    while True:
        print("Trying to open serial port...")
        serial_connection = serial.Serial('/dev/ttyUSB0')
        if serial_connection.is_open:
            print("Opened port " + serial_connection.name + " successfully")
            break

    while True:
        try:
            presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc = read_data(serial_connection)
        except DataInvalid as e:

            print("Data with index " + str(e.index) + " is not in range: " + str(data_validation[e.index][0]) + " < " + str(e.value) + " < " + str(data_validation[e.index][1]))
            continue

        try:
            sql_query = "INSERT INTO `sensor_data`(`presssure`, `temperature`, `humidity`, `gyro_x`, `gyro_y`, `gyro_z`, `uv_index`, `ir_light`, `visible_light`, `eco2`, `tvoc`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
            mycursor.execute(sql_query.format(presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))
            mydb.commit()
            # print(sql_query.format(presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))
        except Exception:
            print("Error connecting to DB")
            print("------------------------")
            print(traceback.format_exc())
            print("------------------------")
            print("Reconnecting...")
            mydb.reconnect()
            print("------------------------")
            sql_query = "INSERT INTO `sensor_data`(`presssure`, `temperature`, `humidity`, `gyro_x`, `gyro_y`, `gyro_z`, `uv_index`, `ir_light`, `visible_light`, `eco2`, `tvoc`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
            mycursor.execute(sql_query.format(presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))
            mydb.commit()
            # print(sql_query.format(presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))

        time.sleep(1)
        # print("------------------------")
    serial_connection.close()

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

                #Command execution goes
                time.sleep(5)
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
    ClientSocket = socket.socket()
    print("Starting db upload thread.")
    start_new_thread(upload_loop, ())
    print("Connecting to socket.")
    try:
        ClientSocket.connect((socket_host, socket_port))
        ClientSocket.settimeout(5)
    except socket.error as e:
        print(str(e))
    print("Starting control thread.")
    control_loop(ClientSocket)
