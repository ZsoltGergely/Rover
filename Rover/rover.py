import mysql.connector
from flask import Flask, request, jsonify
import json

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

mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db
)

mycursor = mydb.cursor(buffered=True)


seed(1)

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    data = request.json
    print(request.json)
    return jsonify(data)


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




for i in range(10):
    presssure, temperature, humidity = get_enviroment()
    gyro_x, gyro_y, gyro_z, = get_gyro()
    uv_index, ir_light, visible_light = get_light()
    eco2, tvoc = get_air()

    sql_query = "INSERT INTO `sensor_data`(`presssure`, `temperature`, `humidity`, `gyro_x`, `gyro_y`, `gyro_z`, `uv_index`, `ir_light`, `visible_light`, `eco2`, `tvoc`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
    mycursor.execute(sql_query.format(presssure, temperature, humidity, gyro_x, gyro_y, gyro_z, uv_index, ir_light, visible_light, eco2, tvoc))
    mydb.commit()

if __name__ == '__main__':
    app.run(host = '0.0.0.0',  port = 5000)
