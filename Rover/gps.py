import serial
from time import time

class date:
	def __init__(self):
		self.day = None
		self.month = None
		self.year = None

	def set(self, day, month, year):
		self.day = day
		self.month = month
		self.year = year


class timeClass:
	def __init__(self):
		self.hour = None
		self.minute = None
		self.secs = None

	def set(self, hour, minute, second):
		self.hour = hour
		self.minute = minute
		self.secs = second


class Gps(serial.Serial):

	def __init__(self, port="/dev/ttyUSB2", baud=9600):
		super().__init__(port, baud, timeout=5)
		self.port = port
		self.send("AT+CGPS=1,2")
		self.lat = None
		self.log = None
		self.date = date()
		self.UTC_time = timeClass()
		self.alt = None
		self.speed = None
		self.course = None

	def __del__(self):
		self.close()

	def send(self, cmd):
		try:
			self.write(bytes(cmd + "\r", "ascii"))
		except Exception:
			try:
				self.__init__(self.port)
			finally:
				return

	def getline(self):
		try:
			return self.readline().decode("ascii")
		except Exception:
			try:
				self.__init__(self.port)
			finally:
				return " "

	def sendRecieve(self, cmd):
		self.send(cmd)
		str=self.getline()
		while len(str)>1:
			print(str)
			str=self.getline()

	def __str__(self):
		try:
			return "Time: %dh %dm %ds Coordinates: %f %f Alt: %fm Speed: %fm/s Course: %fdeg" % (
				self.UTC_time.hour, self.UTC_time.minute, self.UTC_time.secs, self.lat,
				self.log, self.alt, self.speed,
				self.course)
		except:
			return "Nincs"

	def update(self):
		self.send("AT+CGPSINFO")
		phrase = self.getline()
		while "+CGPSINFO:" not in phrase:
			phrase = self.getline()
		seqs = phrase.split(",")
		seqs[0] = seqs[0][11:]
		seqs[8] = seqs[8][:len(seqs[8]) - 2]
		# +CGPSINFO: [lat],[N/S],[log],[E/W],[date],[UTC time],[alt],[speed],[course]
		# ['4551.909138', 'N', '02547.269043', 'E', '180321', '072016.0', '526.6', '0.0', '191.3']
		try:
			if int(float(seqs[0])) > 90:
				self.lat = float(seqs[0]) / 100
				if seqs[1] != 'N':
					self.lat *= -1

			if int(float(seqs[2])) > 180:
				self.log = float(seqs[2]) / 100
				if seqs[3] != 'E':
					self.lat *= -1

			self.date.set(int(float(seqs[4][:2])), int(float(seqs[4][2:4])), int(float(seqs[4][4:])))
			self.UTC_time.set(int(float(seqs[5][:2])), int(float(seqs[5][2:4])), float(seqs[5][4:]))

			self.alt = float(seqs[6])
			self.speed = float(seqs[7]) * 0.51444444444444444444444444444  # knots to m/s
			self.course = float(seqs[8])
		finally:
			return seqs

	def test(self, t=None):
		if t is None:
			while True:
				self.update()
				print(self)
		elif t>0:
			start=time()
			while time()<start+t:
				self.update()
				print(self)
