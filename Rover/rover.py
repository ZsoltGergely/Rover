import mysql.connector
import json
import traceback
from _thread import *
import time
import socket
from cryptography.fernet import Fernet
import serial

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



def upload_loop():
    while True:
        print("Trying to open serial port...")
        serial_connection = serial.Serial('/dev/ttyACM0')
        if serial_connection.is_open:
            print("Opened port " + serial_connection.name + " successfully")
            break
    print(serial_connection)

    while True:
        print("Yes")
        try:
            line = str(serial_connection.readline())
            line.replace("*", "")
            print(line)
            print(line)
            elements = line[3:-5].split(";")
            print(elements)

            pressure = float(elements[2])
            temperature = float(elements[0])
            humidity = float(elements[1])
            gyro_x = float(elements[10])
            gyro_y = float(elements[11])
            gyro_z = float(elements[12])
            uv_index = float(elements[5])
            ir_light = float(elements[4])
            visible_light = float(elements[3])
            eco2 = float(elements[7])
            tvoc = float(elements[6])
            rawh2 = float(elements[8])
            rawethanol = float(elements[9])
            acc_x = float(elements[13])
            acc_y = float(elements[14])
            acc_z = float(elements[15])
            mag_x = float(elements[16])
            mag_y = float(elements[17])
            mag_z = float(elements[18])


            sql_query = "INSERT INTO `sensor_data`(`pressure`, `temperature`, `humidity`, `gyro_x`, `gyro_y`, `gyro_z`, `uv_index`, `ir_light`, `visible_light`, `eco2`, `tvoc` , `rawh2`, `rawethanol`, `acc_x`, `acc_y`, `acc_z`, `mag_x`, `mag_y`, `mag_z`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
            mycursor.execute(sql_query.format(pressure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc, rawh2, rawethanol, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z))
            mydb.commit()
            print(sql_query.format(pressure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))

            time.sleep(1)
        except DataInvalid as e:

            print("Data with index " + str(e.index) + " is not in range: " + str(data_validation[e.index][0]) + " < " + str(e.value) + " < " + str(data_validation[e.index][1]))
            continue

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
                time.sleep(2)
                # enc_message = crypto.encrypt(str.encode(decrypted_message.decode()+";DN"))
                # Socket.send(enc_message)
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
