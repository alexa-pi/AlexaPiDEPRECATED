#!/usr/bin/python
import time
import alsaaudio
import wave
import os
import random
import os
from creds import *
import requests
import json
import re
from memcache import Client


rf = open('recording.wav', 'wb')

recorded = False
file = '/sys/class/gpio/gpio409/value'
f = open(file, "r")
last = f.read()
f.close()
audio = ""


#Memcache Setup
servers = ["127.0.0.1:11211"]
mc = Client(servers, debug=1)

def gettoken():
	token = mc.get("access_token")
	refresh = refresh_token
	if token:
		return token
	elif refresh:
		payload = {"client_id" : Client_ID, "client_secret" : Client_Secret, "refresh_token" : refresh, "grant_type" : "refresh_token", }
		url = "https://api.amazon.com/auth/o2/token"
		r = requests.post(url, data = payload)
		resp = json.loads(r.text)
		mc.set("access_token", resp['access_token'], 3570)
		return resp['access_token']
	else:
		return False

		

def play(f):    
    device = alsaaudio.PCM()
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')
    device.setperiodsize(320)
    data = f.readframes(320)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(320)
		

def alexa():
	url = 'https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize'
	headers = {'Authorization' : 'Bearer %s' % gettoken()}
	d = {
   		"messageHeader": {
       		"deviceContext": [
           		{
               		"name": "playbackState",
               		"namespace": "AudioPlayer",
               		"payload": {
                   		"streamId": "",
        			   	"offsetInMilliseconds": "0",
                   		"playerActivity": "IDLE"
               		}
           		}
       		]
		},
   		"messageBody": {
       		"profile": "alexa-close-talk",
       		"locale": "en-us",
       		"format": "audio/L16; rate=16000; channels=1"
   		}
	}
	inf = open('recording.wav')
	files = [
		('file', ('request', json.dumps(d), 'application/json; charset=UTF-8')),
		('file', ('audio', inf, 'audio/L16; rate=16000; channels=1'))
	]	
	r = requests.post(url, headers=headers, files=files)
	inf.close()
	for v in r.headers['content-type'].split(";"):
		if re.match('.*boundary.*', v):
			boundary =  v.split("=")[1]
	data = r.content.split(boundary)
	for d in data:
		if (len(d) >= 1024):
			audio = d.split('\r\n\r\n')[1].rstrip('--')
	f = open("response.mp3", 'wb')
	f.write(audio)
	f.close()
	os.system('mpg321 -q 1sec.mp3 response.mp3')


token = gettoken()
os.system('mpg321 -q 1sec.mp3 hello.mp3')
while True:
	f = open(file, "r")
	val = f.read().strip('\n')
	if val != last:
		last = val
		if val == '1' and recorded == True:
			rf = open('recording.wav', 'w') 
			rf.write(audio)
			rf.close()
			inp = None
			alexa()
		elif val == '0':
			inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
			inp.setchannels(1)
			inp.setrate(16000)
			inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
			inp.setperiodsize(500)
			audio = ""
			f = wave.open('beep.wav', 'rb')
			play(f)
			f.close()
			l, data = inp.read()
			if l:
				audio += data
			recorded = True
	elif val == '0':
		l, data = inp.read()
		if l:
			audio += data
	f.close()	
	
