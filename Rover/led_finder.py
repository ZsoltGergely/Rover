import platform
import time
import subprocess
import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 8)

while 1:
	led = input("Enter led number: ")
	list1 = led.split(",")
	list2 = led.split("-")
	if len(list1) != 1:
		for i in list1:
			if int(i) != 51:
				pixels[int(i)] = (255, 255, 0)
			else:
				pixels.fill((0, 0, 0))
	elif len(list2) != 1:
		for i in range(int(list2[0]), int(list2[1])):
			pixels[i] = (255, 255, 0)

	elif len(list1) == 1 and len(list2) == 1:
		if(int(list1[0]) != 51):
			pixels[int(list1[0])] = (255, 255, 0)
		else:
			pixels.fill((0,0,0))
