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
send_port = _variables.send_port
rcv_port = _variables.rcv_port
ip = _variables.send_ip
myIP = _variables.myIP
once = _variables.once
count_once = int(math.log(once, 2))
count_init = []

c = 0
for LED in LEDs:
	count_init.append(LED//once)
	c += 1
for i in range(len(ip)):
	print("HOST:" + ip[i] +", PORT:" + str(send_port[i]))
print("解像度: " + str(width) + "x" + str(height))
send_client = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for i in range(len(ip))]
rcv_client = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for i in range(len(ip))]

for i in range(len(ip)):
	rcv_client[i].bind(("192.168.0.120", rcv_port[i]))
	print("port: " + str(rcv_port[i]))

offset = 0
pixels_bin = [[[] for col in range(width)] for row in range(height)]
pixels = [[[-1, -1] for col in range(width)] for row in range(height)]
colors = [[0 for col in range(width)] for row in range(height)]
frames = []

def send_soc(num, items):
	msg = "/init/"
	if(type(items) is list):
		msg += json.dumps(items)
	elif(type(items) is str):
		msg += items
	send_client[num].sendto(msg.encode('utf-8'), (ip[num], send_port[num]))
	print(msg)
	while True:
		try:
			rcv_byte = bytes()
			rcv_byte, addr = rcv_client[num].recvfrom(64)
			msg = rcv_byte.decode()
			if msg == '1':
				break
		except KeyboardInterrupt:
				rcv_client[num].close()
count = 0
def capture(cap):
	global count
	ret, frame = cap.read()
	h = frame.shape[0]
	w = frame.shape[1]
	frame = frame[2:h-2,3:w-3]
	frame = cv2.resize(frame,(width, height))
	cv2.imwrite('img/' + str(count) + '.jpg', frame)
	count += 1
	return frame

def analyze(frame):
	global pixels_bin
	for j in range(width):
		for i in range(height):
			pixelValue = frame[i, j]
			r = frame.item(i, j, 2)
			g = frame.item(i, j, 1)
			b = frame.item(i, j, 0)
			color = int((r + g + b) / 3)
			if color > 200:
				pixels_bin[i][j].append(1)
				if(colors[i][j] == 0 or colors[i][j] < color):
					colors[i][j] = color
			else:
				pixels_bin[i][j].append(0)

def apply(count_reverce, count_esp):
	global pixels_bin, pixels, colors, offset
	for j in range(width):
		for i in range(height):
			if(len(pixels_bin[i][j]) > 0):
				bin = "0b"
				for num in pixels_bin[i][j]:
					bin += str(num)
				bin = int(bin, 2)
				pixels_bin[i][j] = []
				ledNum = -1
				if(bin >= 64):
					if(count_reverce == 0):
						ledNum = once - 1 - bin + offset
					else:
						ledNum = bin + offset
					flag_lednum = False
					for column in range(width):
						for row in range(height):
							if(pixels[row][column][0] == ledNum and pixels[row][column][1] == count_esp):
								flag_lednum = True
								break
						if(flag_lednum):
							break
					if(not flag_lednum):
						pixels[i][j][0] = ledNum
						pixels[i][j][1] = count_esp
					else:
						same_c = colors[row][column]
						if(same_c < colors[i][j] and pixels[i][j][1] == count_esp):
							print("ESP: " + str(count_esp) + " POS :" + str(pixels[row][column][0]) + " currentPOS: " + str(ledNum) + " pastX: " + str(column) + " pastY: " + str(row) +  " currentX: " + str(j) + " currentY: " + str(i) + " same Color: " + str(same_c) + " Corrent Color: " + str(colors[i][j]))
							pixels[i][j][0] = ledNum
							pixels[i][j][1] = count_esp
							pixels[row][column][0] = -1
							pixels[row][column][1] = -1

def onLed():
	global offset, frames
	cap = cv2.VideoCapture(camera)
	for cnt_esp in range(len(count_init)):
		print(cnt_esp)
		offset = 0
		for i in range(len(ip)):
			send_soc(i, "off")
		for i in range(count_init[cnt_esp]):
			for cnt_rvrc in range (2):
				for j in range(count_once):
					onLed_oneSctn = int(once / (2 ** (j + 1)))
					onled_sep = 2 ** (j + 1)
					onLed = []
					for sep_pos in range(onled_sep):
						for k in range(offset, onLed_oneSctn + offset):
							if(cnt_rvrc == 0):
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
					send_soc(cnt_esp, onLed)
					sleep(0.3)
					analyze(capture(cap))
					send_soc(cnt_esp, "off")
				apply(cnt_rvrc, cnt_esp)
			offset += once
	with open('pos.json', 'w') as f:
		json.dump(pixels, f, ensure_ascii=False, indent=2)
	cap.release()

onLed()
