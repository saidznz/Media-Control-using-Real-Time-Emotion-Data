import matplotlib.pyplot as plt
import matplotlib.animation as an

# from sender program (messi)
'''from socket import *
import sys
import json
import unicodedata
s = socket(AF_INET, SOCK_DGRAM)
host = "192.168.100.181"
port = 5000
buf = 1024
data= b"Hello"
addr = (host, port)
num = 1'''
#end

#light control code
from phue import Bridge
b = Bridge('192.168.100.159')
b.connect()
b.get_api()
lights = b.lights
lights = b.get_light_objects('id')
if(lights[2].on == False):
   lights[2].on = True
   lights[2].brightness = 127
#lights[2].hue = 0
#end


fig = plt.figure()
fig.suptitle("Real Time Emotion Data updated in every 1 sec")
ax1 = fig.add_subplot(111)


def refreshGraphData(i):
	print("Refreshing Data.....")
	graphData = open("emotiondata.csv", "r").read()
	lines = graphData.split("\n")
	xValues = []
	yValues = []
	zValues = []
	aValues = []
	angValues = []
	supValues = []
	
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
			xValues.append(x)
			yValues.append(y)
			zValues.append(z)
			aValues.append(a)
			angValues.append(ang)
			supValues.append(sup)
			
			#extra lines from messi
			'''data = json.dumps({"Time": x, "Joy": y, "Eyeclosure": ec})
			s.sendto(data.encode(),addr)
			print ("sending ...", data.encode())'''
			#end

			
			
	#light control code
	# red:0, blue:46920, green:25500, yellow:12750, pink:56100 , white: 50000
	if(yValues[-1]>50):
		#print("Happy")
		lights[2].hue = 24432 #  joy, green
	elif(aValues[-1])>30:
		lights[2].hue = 47104 # sad, blue
	elif(angValues[-1]>30):
		lights[2].hue = 0 # angry, red
	elif(supValues[-1]>30):
		lights[2].hue = 10179  # suprise, yellow
	elif(zValues[-1]>30):
		lights[2].hue = 49298 # fear, purple
	else:
		lights[2].hue = 50000
	#end of light control code
	ax1.clear()
	ax1.plot(xValues, yValues)
	ax1.plot(xValues, zValues)
	ax1.plot(xValues, aValues)
	plt.xlabel("Time")
	plt.legend(["Joy 😃","Fear 😨","Sadness 😞"], loc = "upper left")
	#plt.ylabel("Joy")
ani = an.FuncAnimation(fig, refreshGraphData, interval = 300)
plt.show()
