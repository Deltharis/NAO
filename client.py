import urllib2
import json
from naoqi import ALProxy, ALModule
import unicodedata
url = 'http://localhost:8080/NaoServer/webapi/get/getList'
actionUrl = 'http://localhost:8080/NaoServer/webapi/get/getAction/'
ip = "127.0.0.1"
port = 9559
tts = ALProxy("ALTextToSpeech", ip, port)
mem = ALProxy("ALMemory", ip, port)
motion = ALProxy("ALMotion", ip, port)

class test(ALModule):
	"""Word said, let's parse it"""
	def wordSaid(self,key,value,message):
		"""method for caring about word said"""
		print "hi"
	pass
	
	
response = urllib2.urlopen(url).read()
data  = json.loads(response)
list = data['list']




tts.say("Hello, world! List has " + str(len(list)) + " words!")




mem.subscribeToEvent("WordRecognized","test","wordSaid")




def handleAngle(data):
	print data
	names  = ["HeadYaw", "HeadPitch"]
	angles = [0., 0.]
	times  = [1.0, 1.0]
	isAbsolute = True
	motion.angleInterpolation(names, angles, times, isAbsolute)
	print data['names']
	names = data['names']
	angles = data['angles']
	times = data['times']
	print names
	names2 = []
	for name in names:
		names2.append(unicodedata.normalize('NFKD', name).encode('ascii','ignore'))
	print names2
	print 'Here!'
	motion.setStiffnesses("Body",1.0)
	motion.angleInterpolation(names2, angles, times, True);
	motion.setStiffnesses("Body",0.0)

def parseAction(data):
	if data['kod'] == 'complex':
		print 'Here1!'
		print 'what1'
		print 'what2'
		for l in data['actionChain']:
			print 'Here2!'

			parseAction(l)
	else:
		print 'Here3!'
		if data['kod'] == 'angle':
			handleAngle(data)





action = urllib2.urlopen(actionUrl + "do").read()
data = json.loads(action)
print data
print data
if data != "":
	parseAction(data)


