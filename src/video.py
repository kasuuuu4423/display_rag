import cv2
import numpy as np
import socket
from time import sleep
import json
import _variables

TAPEs = _variables.TAPEs
LEDs = _variables.LEDs
width,height=_variables.width, _variables.height
camera = _variables.camera
send_port = _variables.send_port
ip = _variables.ip

json_open = open('pos.json', 'r')
pos = json.load(json_open)
send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_soc(ip, items):
	if(type(items) is list):
		msg = "/video/" + json.dumps(items)
	elif(type(items) is str):
		msg = items
	print(msg)
	send_client.sendto(msg.encode('utf-8'), (ip, send_port))

def video_send():
	video = cv2.VideoCapture("./video/bad.mp4")
	while(True):
		ret, videoFrame = video.read()
		if not ret:
			video.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
		videoFrame = cv2.resize(videoFrame,(width, height))
		cv2.imshow("frame", videoFrame)
		for j in range(width):
			colors = [[] for i in range(len(ip))]
			for i in range(height):
				if(pos[i][j][0] > 0 and 2700 > pos[i][j][0]):
					pixVal = videoFrame[i, j]
					g = hex(pixVal[1]).strip("0x")
					r = hex(pixVal[2]).strip("0x")
					b = hex(pixVal[0]).strip("0x")
					if(len(g) == 1):
						g = "0" + g
					elif(len(g) == 0):
						g = "00"
					if(len(r) == 1):
						r = "0" + r
					elif(len(r) == 0):
						r = "00"
					if(len(b) == 1):
						b = "0" + b
					elif(len(b) == 0):
						b = "00"
					color = "0x" + g + r + b
					colors[pos[i][j][1]].append(pos[i][j][0])
					colors[pos[i][j][1]].append(color)
			for k in range(len(ip)):
				send_soc(ip[k], colors[k])
			#sleep(0.1)
		k = cv2.waitKey(1)
		if k == 27:
			break
	video.release()
	cv2.destroyAllWindows()

video_send()