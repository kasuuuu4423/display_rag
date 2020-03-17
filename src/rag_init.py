import cv2
import numpy as np
import argparse
import socket
from time import sleep
import math
import collections
import sys
import _variables
import json

TAPEs = _variables.TAPEs
LEDs = _variables.LEDs
width,height=_variables.width, _variables.height
camera = _variables.camera
port_num = _variables.port_num
ip = _variables.ip
once = 128
count_once = int(math.log(once, 2))
count_init = []
c = 0
for LED in LEDs:
	count_init.append(LED//once)
	c += 1

host = "192.168.1.9"
port = 37564
for i in ip:
	print("HOST:" + i +", PORT:" + str(port))

print(TAPEs)
print(LEDs)
print(str(width) + "x" + str(height))

offset = 0
pixels_bin = [[[] for col in range(width)] for row in range(height)]
pixels = [[-1 for col in range(width)] for row in range(height)]
colors = [[0 for col in range(width)] for row in range(height)]
frames = []

def send_soc(ip, items):
	socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_client.connect((ip, port))
	if(type(items) is list):
		msg = json.dumps(items)
	elif(type(items) is str):
		msg = items
	socket_client.send(msg.encode('utf-8'))
	response = socket_client.recv(4096)
	while not response:
		print('Wait for response.....')

def onLed():
	global offset, frames
	for c in range(len(count_init)):
		send_soc(ip[c], "off")
		for i in range(count_init[c]):
			onLed = []
			for cnt in range (2):
				for j in range(count_once):
					onLed_oneSctn = int(once / (2 ** (j + 1)))
					onled_sep = 2 ** (j + 1)
					onLed = []
					for sep_pos in range(onled_sep):
						for k in range(offset, onLed_oneSctn + offset):
							if(cnt == 0):
								if(sep_pos%2 == 0):
									onLed.append(1)
								else:
									onLed.append(0)
							else:
								if(sep_pos%2 == 0):
									onLed.append(0)
								else:
									onLed.append(1)
					onLed = [i + offset for i, x in enumerate(onLed) if x == 1]
					send_soc(ip[c], onLed)
					analyze(capture())
					send_soc(ip[c], "off")
				# for ana_item in frames:
				# 	analyze(ana_item)
				apply(cnt)
			offset += once

def capture():
	cap = cv2.VideoCapture(camera)
	ret, frame = cap.read()
	frame = cv2.resize(frame,(width, height))
	return frame

def analyze(frame):
	global pixels_bin, frames
	count_on = 0
	for j in range(width):
		for i in range(height):
			pixelValue = frame[i, j]
			r = pixelValue[2]
			g = pixelValue[1]
			b = pixelValue[0]
			if b > 200:
				pixels_bin[i][j].append(1)
				if(colors[i][j] == 0 or colors[i][j] < b):
					colors[i][j] = b
			else:
				pixels_bin[i][j].append(0)

def apply(count):
	global pixels_bin, pixels, colors, offset
	for j in range(width):
		for i in range(height):
			if(pixels_bin[i][j] is not None):
				bin = "0b"
				for num in pixels_bin[i][j]:
					bin += str(num)
				bin = int(bin, 2)
				if(count == 0):
					ledNum = once - bin + offset
				else:
					ledNum = bin + offset
				column = 0
				flag_lednum = False
				for row in range(height):
					if(pixels[row].count(ledNum) > 0):
						column = pixels[row].index(ledNum)
						flag_lednum = True
						break
				if(not flag_lednum):
					pixels[i][j] = ledNum
				else:
					same_c = colors[row][column]
					if(same_c < colors[i][j]):
						same = pixels[row][column]
						pixels[i][j] = ledNum
						pixels[row][column] = -1


onLed()
with open('pos.json', 'w') as f:
	json.dump(pixels, f, ensure_ascii=False, indent=4)