import cv2
import numpy as np
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
from time import sleep
import math
import _variables

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
pixels_bin = np.empty((height,width,3), int)
pixels = np.empty((height,width,4), int)
colors = np.empty((height,width), int)
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

#offsetから！！！！！！！
def onLed():
	onLed = []
	for i in range(count_once):
		onLed_oneSctn = int(once / (2 ** (i + 1)))
		onled_sep = 2 ** (i + 1)
		onLed = []
		for j in range(onled_sep):
			for k in range(offset, onLed_oneSctn + offset):
				if(j%2 == 0):
					onLed.append(1)
				else:
					onLed.append(0)
		onLed = [i for i, x in enumerate(onLed) if x == 1]
		send_osc(onLed)
		frames[i] = capture()
		analyze(frames[i])

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
				pixels_bin[i, j].append(1)
				if(colors[i, j] is None or colors[i, j] < b):
					colors[i, j] = b

def apply(pix, clrs):
	for j in range(width):
		for i in range(height):
			if(pix[i, j] is not None):
				bin = "0b"
				for num in pix[i, j]:
					bin += str(num)
				bin = int(bin, 0)
				ledNum = once - bin + offset
				if(pix.count(ledNum) == 0):
					pix[i, j] = ledNum
				else:
					same = pix.index(ledNum)
					same_c = clrs[same]
					if(same_c < clrs[i, j]):
						pix[i, j] = ledNum
						pix[same] = None

onLed()
apply(pixels_bin, colors)
offset += once


# def initialize():
# 	led_pos = 0

# 				# if j == 77 and i == 43:
# 				# 	print("aaaaaaaaaaaaa")
# 		msg = osc_message_builder.OscMessageBuilder(address="/init")
# 		msg.add_arg(led_pos)
# 		msg.add_arg(0)
# 		msg = msg.build()
# 		sleep(0.05)
# 		client.send(msg)

# 		#LEDがすべて認識されたら終了
# 		if led_pos == TAPEs * LEDs - 1:
# 			break
# 		led_pos = led_pos + 1
# 	# キャプチャをリリースして、ウィンドウをすべて閉じる
# 	cap.release()
# 	cv2.destroyAllWindows()