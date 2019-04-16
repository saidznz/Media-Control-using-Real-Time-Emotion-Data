import matplotlib.pyplot as plt
import matplotlib.animation as an
import time, sys
from tkinter import Tk, Label, PhotoImage,Button

# from sender program (messi)
'''from socket import *
import sys
import json
import unicodedata
s = socket(AF_INET, SOCK_DGRAM)
host = "192.168.100.124"
port = 5000
buf = 1024
data= b"Hello"
addr = (host, port)
num = 1'''
#end
lightnumber = 4
group = [4,5]
#light control code
from phue import Bridge
b = Bridge(ip='192.168.100.103')
b.connect()
b.get_api()
#lights = b.lights
lights = b.get_light_objects('id')
if(lights[lightnumber].on == False):
   b.set_light(group, 'on', True)
   b.set_light(group,{'bri':220, 'transitiontime': 1})
   b.set_light(group,{'sat':200, 'transitiontime': 1})
else:
   b.set_light(group,{'bri':220, 'transitiontime': 1})
   b.set_light(group,{'sat':200, 'transitiontime': 1})

#lights[lightnumber].hue = 0
#end


fig = plt.figure()
fig.suptitle("Real Time Emotion Data updated in every 0.3 sec")
ax1 = fig.add_subplot(111)


eyeClosureCounter = 0
eyeOpenCounter = 0
sleep = False
def refreshGraphData(i):
	global eyeClosureCounter, eyeOpenCounter, sleep
	print("Refreshing Data.....")
	graphData = open("emotiondata.csv", "r").read()
	lines = graphData.split("\n")[-200:]
	xValues = []
	yValues = []
	zValues = []
	aValues = []
	angValues = []
	supValues = []
	faceIds = []
	eyeClosure = []
	
	for line in lines[1:]:
		happycounter = 0
		if len(line) > 1:
			cols = line.split(",")
			x = float(cols[0])  # Time
			y = float(cols[11]) # Joy
			z = float(cols[12]) # Fear
			a = float(cols[14]) # Sadness
			ang = float(cols[15]) # angry
			sup = float(cols[16]) # suprise
			ec = float(cols[33]) #Eye Closure
			fid = cols[1] # face ID
			xValues.append(x)
			yValues.append(y)
			zValues.append(z)
			aValues.append(a)
			angValues.append(ang)
			supValues.append(sup)
			faceIds.append(fid)
			eyeClosure.append(ec)

			
			
			#extra lines from messi
			'''data = json.dumps({"Time": x, "Joy": y, "Eyeclosure": ec})
			s.sendto(data.encode(),addr)
			print ("sending ...", data.encode())'''
			#end
	
		
	#print(eyeClosure[-1])
	
	#deal with sleep using counters
	if(faceIds[-1]!="nan"):
		#print(eyeClosure[-2])
		if(eyeClosure[-1]>50):
			eyeClosureCounter += 1
			eyeOpenCounter = 0
		else:
			eyeOpenCounter += 1
			eyeClosureCounter = 0
		print("Closed: ",eyeClosureCounter)
		print("Open: ", eyeOpenCounter)	
		if(eyeClosureCounter==10):
			#call bright -> dim -> off light function here
			if(lights[lightnumber].on==True):
				i = 170
				#lights[lightnumber].on = False
				while(i>0):
					print(i," th Loop")
					i -= 20
					#lights[lightnumber].brightness = i
					b.set_light(group,{'bri':i, 'transitiontime': 1})
					time.sleep(0.5)
					i += 10
					#lights[lightnumber].brightness = i
					b.set_light(group,{'bri':i, 'transitiontime': 1})
					time.sleep(0.5)
					if(i<1):
						#lights[lightnumber].on = False
						b.set_light(group, 'on', False)
			sleep = True
			eyeClosureCounter = 0 # restart the counter when a person is already sleeping
			print("Sleeping")

		if(eyeOpenCounter==20):
			#call on -> dim -> bright light function here
			if(lights[lightnumber].on == False):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 49298
				b.set_light(group,{'hue':49298, 'transitiontime': 1})
				j = 0
				while(j<170):
					j += 10
					#lights[lightnumber].brightness = j
					b.set_light(group,{'bri':j, 'transitiontime': 1})
					time.sleep(0.3)
					j -= 5
					#lights[lightnumber].brightness = j
					b.set_light(group,{'bri':j, 'transitiontime': 1})
					time.sleep(0.3)
					
			sleep = False
			eyeOpenCounter = 0 # restart the counter when a person is already awake
			print("Awake")
	#end of dealing with sleep
	
        #light emotionally controlled code control code
	# red:0, blue:46920, green:25500, yellow:12750, pink:56100 , white: 50000
	#face not detected
	if(faceIds[-1]=="nan"):
		if(lights[lightnumber].on == True):
			#lights[lightnumber].on = False
			b.set_light(group, 'on', False)
	#end
	#face detected
	else:
		if(yValues[-1]>40):
			#print("Happy")
			if((lights[lightnumber].on == False) and (sleep==False)):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 24432 #  joy, green
				b.set_light(group,{'hue':24432, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					#lights[lightnumber].hue = 24432
					b.set_light(group,{'hue':24432, 'transitiontime': 1})
		elif(aValues[-1])>30:
			if((lights[lightnumber].on == False) and (sleep==False)):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 47104 # sad, blue
				b.set_light(group,{'hue':47104, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					#lights[lightnumber].hue = 47104
					b.set_light(group,{'hue':47104, 'transitiontime': 1})
		elif(angValues[-1]>30):
			if((lights[lightnumber].on == False) and (sleep==False)):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 0 # angry, red
				b.set_light(group,{'hue':0, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					#lights[lightnumber].hue = 0
					b.set_light(group,{'hue':0, 'transitiontime': 1})
		elif(supValues[-1]>30):
			if((lights[lightnumber].on == False) and (sleep==False)):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 10179  # suprise, yellow
				b.set_light(group,{'hue':10179, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					#lights[lightnumber].hue = 10179
					b.set_light(group,{'hue':10179, 'transitiontime': 1})
		elif(zValues[-1]>30):
			if((lights[lightnumber].on == False) and (sleep==False)):
				#lights[lightnumber].on = True
				b.set_light(group, 'on', True)
				#lights[lightnumber].hue = 49298 # fear, purple
				b.set_light(group,{'hue':49298, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					#lights[lightnumber].hue = 49298
					b.set_light(group,{'hue':49298, 'transitiontime': 1})
		else:
			if((lights[lightnumber].on == False) and (sleep==False)):
				b.set_light(group, 'on', True)
				b.set_light(group,{'hue':49298, 'transitiontime': 1})
			else:
				if(lights[lightnumber].on == True):
					b.set_light(group,{'hue':49298, 'transitiontime': 1})
		#end of face detected block
		#end of light control code
	ax1.clear()
	ax1.plot(xValues[-100:], yValues[-100:], color='green')
	ax1.plot(xValues[-100:], zValues[-100:], color ='purple')
	ax1.plot(xValues[-100:], aValues[-100:], color='blue')
	plt.xlabel("Time")
	plt.legend(["Joy 😃","Fear 😨","Sadness 😞"], loc = "upper left")
	#plt.ylabel("Joy")

ani = an.FuncAnimation(fig, refreshGraphData, interval = 500) #refreshing every 500 miliseconds
plt.show()

