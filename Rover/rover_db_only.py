import mysql.connector
import json
import serial
import time

class Error(Exception):
    pass

class DataInvalid(Error):
    def __init__(self, data, index):
        self.data = data
        self.index = index

data_validation = [
(1, 100000), #    presssure value range
(1, 100000), #    temperature value range
(1, 100000), #    humidity value range
(1, 100000), #    gyro_x value range
(1, 100000), #    gyro_y value range
(1, 10000000), #    gyro_z value range
(1, 100000), #    uv_index value range
(1, 100000), #    ir_light value range
(1, 100000), #    visible_light value range
(1, 100000), #    eco2 value range
(1, 100000)  #    tvoc value range
]

cfg = open("rover_config.json", "r")
tmpconfig = cfg.read()
cfg.close()
config = json.loads(tmpconfig)


db_host = config["db_host"]
db_user = config["db_user"]
db_pass = config["db_pass"]
db = config["db"]

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db
)


mycursor = mydb.cursor(buffered=True)



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




            sql_query = "INSERT INTO `sensor_data`(`pressure`, `temperature`, `humidity`, `gyro_x`, `gyro_y`, `gyro_z`,`uv_index`, `ir_light`, `visible_light`, `eco2`, `tvoc`, `rawh2`, `rawethanol`, `acc_x`, `acc_y`, `acc_z`, `mag_x`, `mag_y`, `mag_z`, `longitude`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
            mycursor.execute(sql_query.format(pressure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc, rawh2, rawethanol, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, 0))
            mydb.commit()
            # print(sql_query.format(pressure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))

            time.sleep(1)
        except DataInvalid as e:

            print("Data with index " + str(e.index) + " is not in range: " + str(data_validation[e.index][0]) + " < " + str(e.value) + " < " + str(data_validation[e.index][1]))
            continue



        # print("------------------------")
    serial_connection.__del__()





if __name__ == '__main__':
    print("Starting db upload thread.")
    upload_loop()
