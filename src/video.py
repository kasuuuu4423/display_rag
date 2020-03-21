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
ip = _variables.send_ip

json_open = open('pos.json', 'r')
pos = json.load(json_open)
send_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_soc(ip, port, items):
	if(type(items) is list):
		msg = "/video/" + json.dumps(items)
	elif(type(items) is str):
		msg = items
	send_client.sendto(msg.encode('utf-8'), (ip, port))

def video_send():
	video = cv2.VideoCapture("./video/test.mp4")
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
					r = videoFrame.item(i, j, 1)
					g = videoFrame.item(i, j, 2)
					b = videoFrame.item(i, j, 0)
					color = [r, g, b]
					colors[pos[i][j][1]].append(pos[i][j][0])
					colors[pos[i][j][1]].append(color)
			for k in range(len(ip)):
				if(len(colors[k]) > 0):
					send_soc(ip[k], send_port[k], colors[k])
			sleep(0.0001)
		k = cv2.waitKey(1)
		if k == 27:
			break
	video.release()
	cv2.destroyAllWindows()

video_send()
