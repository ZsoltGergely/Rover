import mysql.connector
import json
import traceback
from _thread import *
import time
import socket
from cryptography.fernet import Fernet




# random
from random import seed
from random import randint
# random

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
ClientSocket = socket.socket()
crypto = Fernet(key)

seed(1)


def get_enviroment():

    presssure = randint(0, 50)
    temperature = randint(50, 100)
    humidity = randint(0, 10)


    return presssure, temperature, humidity

def get_gyro():

    gyro_x = randint(3000, 5000)
    gyro_y = randint(3000, 5000)
    gyro_z = randint(3000, 5000)


    return gyro_x, gyro_y, gyro_z

def get_light():

    uv_index =  randint(0, 10)
    ir_light = randint(0, 100)
    visible_light = randint(0, 100)


    return uv_index, ir_light, visible_light

def get_air():

    eco2 = randint(0, 100)
    tvoc = randint(0, 100)


    return eco2, tvoc

def upload_loop():
    while True:
        presssure, temperature, humidity = get_enviroment()
        gyro_x, gyro_y, gyro_z, = get_gyro()
        uv_index, ir_light, visible_light = get_light()
        eco2, tvoc = get_air()
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

def control_loop():
    while True:
        print("Waiting for commands...")
        command = ClientSocket.recv(1024)
        decrypted_message = crypto.decrypt(command)
        print(str(decrypted_message))
        ClientSocket.send(command)
        print("Confirmation sent!")

        #Command execution goes
        time.sleep(5)
        enc_message = crypto.encrypt(str.encode(decrypted_message.decode()+";DN"))
        ClientSocket.send(enc_message)




if __name__ == '__main__':
    print("Starting db upload thread.")
    start_new_thread(upload_loop, ())
    print("Connecting to socket.")
    try:
        ClientSocket.connect((socket_host, socket_port))
    except socket.error as e:
        print(str(e))
    print("Starting control thread.")
    control_loop()
