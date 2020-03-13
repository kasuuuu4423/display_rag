import cv2
import numpy as np
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep
import math
import collections
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
count_init = LEDs//once
offset = 0
pixels_bin = [[[] for col in range(width)] for row in range(height)]
pixels = [[-1 for col in range(width)] for row in range(height)]
colors = [[0 for col in range(width)] for row in range(height)]
frames = []

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default = ip, help="The ip of th OSC Server")
parser.add_argument("--port", type=int, default=port_num, help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.UDPClient(args.ip, args.port)
print("IP Address:" + ip +", Port:" + str(port_num))

def send_osc(items):
	msg = osc_message_builder.OscMessageBuilder(address="/init")
	if isinstance(items, list):
		for item in items:
			msg.add_arg(item)
	else:
		msg.add_arg(items)
	msg = msg.build()
	client.send(msg)

def onLed():
	global offset, frames
	for i in range(count_init):
		onLed = []
		for j in range(count_once):
			onLed_oneSctn = int(once / (2 ** (j + 1)))
			onled_sep = 2 ** (j + 1)
			onLed = []
			for sep_pos in range(onled_sep):
				for k in range(offset, onLed_oneSctn + offset):
					if(sep_pos%2 == 0):
						onLed.append(1)
					else:
						onLed.append(0)
			onLed = [i for i, x in enumerate(onLed) if x == 1]
			send_osc(onLed)
			#sleep(0.2)
			frames.append(capture())
		for ana_item in frames:
			analyze(ana_item)
		apply()
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

def apply():
	global pixels_bin, pixels, colors, offset
	for j in range(width):
		for i in range(height):
			if(pixels_bin[i][j] is not None):
				bin = "0b"
				for num in pixels_bin[i][j]:
					bin += str(num)
				bin = int(bin, 2)
				ledNum = once - bin + offset
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