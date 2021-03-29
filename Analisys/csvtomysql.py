import time
files = ["sensor_data_2.csv"]
for file in files:
    f = open(file, "r")
    g = open(file[:-4] + ".txt", "a")
    lines = f.read().splitlines()
    for line in lines:
        line = line.replace('"', '')
        line = line.replace("\n", "")
        line = "('" + line[:26]+"'"+line[26:] + "),\n"
        g.write(line)
    g.close()
    f.close()
