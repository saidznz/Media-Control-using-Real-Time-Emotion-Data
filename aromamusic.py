import matplotlib.pyplot as plt
import matplotlib.animation as an
import time, sys
import vlc, random
from tkinter import Tk, Label, PhotoImage,Button

#This is the function for displaying message box
def popmessage(emotion):
	root = Tk()
	# First command line arg is image path. PNG format
	img = PhotoImage(file=emotion)
	img = img.subsample(1, 1)
	my_image = Label(root, image=img)
	my_image.pack()
	button = Button(root, text='OK', width=30, command=root.destroy)
	button.pack(padx=40, pady=40)
	button.config(bg='dark green', fg='white')
	button.config(font=('helvetica', 100, 'underline italic'))
	root.mainloop()


#start playing music at the beginning
tracks = ["MP3/14.mp3","MP3/35.mp3","MP3/02.mp3","MP3/10.mp3"]
aroma = ["aroma/peppermint.png","aroma/lemon.png","aroma/orange.png","aroma/lavender.png"]
player = vlc.MediaPlayer(tracks[random.randint(0,3)])
player.play()
onPlay = True
fig = plt.figure()
#fig.suptitle("Real Time Emotion Data updated in every 0.3 sec")
#ax1 = fig.add_subplot(111)


happyCounter = 0
sadCounter = 0
happy = False

def refreshGraphData(i):
	
	global happyCounter, sadCounter, happy, player, onPlay
	print("Refreshing Data.....")
	graphData = open("emotiondata.csv", "r").read()
	lines = graphData.split("\n")[-200:]
	xValues = []
	yValues = []
	faceIds = []
	smile = []
	
	
	for line in lines[1:]:
		happycounter = 0
		if len(line) > 1:
			cols = line.split(",")
			x = float(cols[0])  # Time
			y = float(cols[11]) # Joy
			fid = cols[1] # face ID
			sm = float(cols[20])
			xValues.append(x)
			yValues.append(y)
			faceIds.append(fid)
			smile.append(sm)
	
		
	#print(eyeClosure[-1])
	
	#deal with joy using counters
	if(faceIds[-1]!="nan"):
		if(onPlay==False):
			player = vlc.MediaPlayer(tracks[random.randint(0,3)])
			player.play()
			onPlay = True
		#print(eyeClosure[-2])
		if((yValues[-1] > 30) | (smile[-1] > 30)):   #Happy when Joy or smile, sad otherwise
			happyCounter += 1
			sadCounter = 0
		else:
			sadCounter += 1
			happyCounter = 0
		print("Happy: ",happyCounter)
		print("Sad: ", sadCounter)	
		if(happyCounter==15):
			if(happy==False):
				#call change/play/stop music a + aroma for happiness suggestion here 
				player.stop()
				player = vlc.MediaPlayer(tracks[random.randint(0,1)]) # play happy track randomly 0,1
				player.play()
				onPlay = True
				happy = True
				print("Changing to Happy Track")
				popmessage(aroma[random.randint(0,1)]) # suggest Aroma
				
			happyCounter = 0 # restart the counter when a person is already happy

		if(sadCounter==100):
			if(happy):
				#call change/play/stop music a + aroma for sadness suggestion here
				player.stop()
				player = vlc.MediaPlayer(tracks[random.randint(2,3)])
				player.play()
				onPlay = True
				happy = False
				print("Changing to Sad Track")
				popmessage(aroma[random.randint(2,3)]) # suggest Aroma

			sadCounter = 0 # restart the counter when a person is already sad
	else:
		player.stop()
		onPlay = False
	#end of dealing with happiness
	
	#ax1.clear()
	#ax1.plot(xValues[-100:], yValues[-100:], color='green')
	#plt.xlabel("Time")
	#plt.legend(["Joy 😃","Fear 😨","Sadness 😞"], loc = "upper left")
	#plt.ylabel("Joy")

ani = an.FuncAnimation(fig,refreshGraphData, interval = 300) #refreshing every 500 miliseconds
plt.show()

