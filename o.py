# OpenCV のインポート
import cv2

#osc関係のインポート
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

from time import sleep

TAPEs = 4
LEDs = 150
width,height=32,18

#座標用の辞書
pixels = {}

############OSC通信セットアップ#############
port_num = 8888
ip = "192.168.13.5"

# セットアップ
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default = ip, help="The ip of th OSC Server")
parser.add_argument("--port", type=int, default=port_num, help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.UDPClient(args.ip, args.port)

print("ip:" + ip +", port:" + str(port_num))

##########WEBカメラを取得############
def initialize():
	#つけるLED位置の初期化
	led_pos = 0

	# VideoCaptureのインスタンスを作成する。
	# 引数でカメラを選べれる。
	cap = cv2.VideoCapture(3)
	colorRange = 25
	while True:
		# VideoCaptureから1フレーム読み込む
		ret, frame = cap.read()

		###OSCでLEDを光らせる###
		#OSCのメッセージを作成
		msg = osc_message_builder.OscMessageBuilder(address="/init")
		#LEDの位置をメッセージのアーギュメントに追加
		msg.add_arg(led_pos)
		#LEDをONにする「1」を(ry)
		msg.add_arg(1)
		#メッセージを送れる状態に変換
		msg = msg.build()
		#メッセージ送信
		client.send(msg)
		print(led_pos)

		###光を認識###
		#キャプチャしたフレームをリサイズ
		frame = cv2.resize(frame,(width, height))
		#グレースケールに変換
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#二値化
		ret, frame = cv2.threshold(frame, colorRange, 255, cv2.THRESH_BINARY)
		cv2.imshow('Edited Frame', frame)

		for j in range(width):
			for i in range(height):
				#ピクセルの色情報を変数に代入
				pixelValue = frame[i, j]
				if pixelValue > colorRange :
					if str(j) + " " + str(i) in pixels:
						pixels[str(j) + " " + str(i)] = pixels[str(j) + " " + str(i)] + " " + str(led_pos)
					else:
						pixels[str(j) + " " + str(i)] = str(led_pos)
						break
				# if j == 77 and i == 43:
				# 	print("aaaaaaaaaaaaa")
		msg = osc_message_builder.OscMessageBuilder(address="/init")
		msg.add_arg(led_pos)
		msg.add_arg(0)
		msg = msg.build()
		sleep(0.05)
		client.send(msg)

		
		#LEDがすべて認識されたら終了
		if led_pos == TAPEs * LEDs - 1:
			break
		led_pos = led_pos + 1
	# キャプチャをリリースして、ウィンドウをすべて閉じる
	cap.release()
	cv2.destroyAllWindows()

#LED1が光って、画面上の10-15だった場合、
#辞書形式で{"10 15": "1"}で保存
#一定時間でイニシャライズ
#解析したpixelをLEDの位置に置き換えて送信


def add_argColor(msg,r,g,b):
	if r==0 and g==0 and b==0:
		msg.add_arg(0)
	elif r==1 and g==0 and b==0:
		msg.add_arg(1)
	elif r==0 and g==1 and b==0:
		msg.add_arg(2)
	elif r==0 and g==0 and b==1:
		msg.add_arg(3)
	elif r==1 and g==1 and b==0:
		msg.add_arg(4)
	elif r==0 and g==1 and b==1:
		msg.add_arg(5)
	elif r==1 and g==0 and b==1:
		msg.add_arg(6)
	elif r==1 and g==1 and b==1:
		msg.add_arg(7)
	elif r==2 and g==0 and b==0:
		msg.add_arg(8)
	elif r==0 and g==2 and b==0:
		msg.add_arg(9)
	elif r==0 and g==0 and b==2:
		msg.add_arg(10)
	elif r==2 and g==2 and b==0:
		msg.add_arg(11)
	elif r==0 and g==2 and b==2:
		msg.add_arg(12)
	elif r==2 and g==0 and b==2:
		msg.add_arg(13)
	elif r==2 and g==2 and b==2:
		msg.add_arg(14)
	elif r==0 and g==1 and b==2:
		msg.add_arg(15)
	elif r==0 and g==2 and b==1:
		msg.add_arg(16)
	elif r==2 and g==1 and b==0:
		msg.add_arg(17)
	elif r==1 and g==2 and b==0:
		msg.add_arg(18)
	elif r==1 and g==0 and b==2:
		msg.add_arg(19)
	elif r==2 and g==0 and b==1:
		msg.add_arg(20)
	elif r==1 and g==1 and b==2:
		msg.add_arg(21)
	elif r==1 and g==2 and b==1:
		msg.add_arg(22)
	elif r==2 and g==1 and b==1:
		msg.add_arg(23)
	elif r==2 and g==1 and b==2:
		msg.add_arg(24)
	elif r==2 and g==2 and b==1:
		msg.add_arg(25)
	elif r==1 and g==2 and b==2:
		msg.add_arg(26)


#############動画を取得##############
# VideoCaptureのインスタンスを作成する。
# 引数で動画を選択
def video_send():
	video = cv2.VideoCapture("apple_test.mp4")

	while(True):
		ret, videoFrame = video.read()

		videoFrame = cv2.resize(videoFrame,(width, height))
		msg = osc_message_builder.OscMessageBuilder(address="/led")
		msg_2 = osc_message_builder.OscMessageBuilder(address="/led_2")
		if not ret:
			video.set(cv2.CAP_PROP_POS_FRAMES, 0)
			continue
    #(height, width) = videoFrame.shape[:2]
		cv2.imshow("frame", videoFrame)
		for j in range(width):
			for i in range(height):
				if str(j) + " " + str(i) in pixels:
					pixelValue = videoFrame[i, j]
					leds = pixels[str(j) + " " + str(i)].split(" ")
					if len(leds) == 1:
						num = int(leds[0])
						msg.add_arg(num)
						values = []
						for value in pixelValue:
							value = int(value)
							if value < 84:
								values.append(0)
							elif value >= 84 and value < 168:
								values.append(1)
							elif value >= 168:
								values.append(2)
						add_argColor(msg,values[0],values[1],values[2])
					else:
						values = []
						for led in leds:
							num = int(led)
							msg.add_arg(num)
							i = 0
							for value in pixelValue:
								value = int(value)
								if value < 84:
									values.append(0)
								elif value >= 84 and value < 168:
									values.append(1)
								elif value >= 168:
									values.append(2)
								i = i + 1
							add_argColor(msg,values[0],values[1],values[2])
				if i == height - 1:
					msg = msg.build()
					sleep(0.001)
					client.send(msg)
					msg = osc_message_builder.OscMessageBuilder(address="/led")

		k = cv2.waitKey(1)
		if k == 27:
			break

	video.release()
	cv2.destroyAllWindows()

##############実行#################
while True:
	initialize()
	video_send()


#pin2つに増やす方法
	#単純