'''
Created on Apr 13, 2013

@author: Abbad
'''

from socket import socket, AF_INET, SOCK_DGRAM
from sys import platform, exit, argv
from getopt import getopt, GetoptError
from time import time, sleep
from thread import start_new_thread
from os import write

from utilities.udp_client_win32_named_pipes import writeToPipe

# global variables
host = "localhost"              # Symbolic name meaning all available interfaces
port = 4001                     # port number
bufferSize = 2084
statNotPeriod = 0				#statisticsNotificationPeriod. // this means that the server will drop a statistics 
numberOfPackets = 0
pipeIn = None

	 
def printHelp():
	print 'This is a UDP client:'
	print 'usage:'
	print '-l host \t\t\t default localhost'
	print '-p port number \t\t\t default 4001'
	print '-b buffer size \t\t\t default 1024'
	print '-f file name \t\t\t default stat.xml'
	print '-n notification period \t\t default 20 seconds'

def checkArguments(argv):
	try:
		opts, args = getopt(argv[1:],"hl:p:b:n:",["host", "portNumber", "bufferSize", "notificationPeriod"])
	except GetoptError:
		print 'UDPClient .py -l <hostname> -p <port> -b <bufferSize> -n <notificationPeriod>'
		exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			exit()
		elif opt in ('-l'):
			global host
			host = arg
		elif opt in ('-p'):
			global port 
			port = int(arg)
		elif opt in ('-b'):
			global bufferSize
			bufferSize = int(arg)
		elif opt in ('-n'):
			global statNotPeriod
			statNotPeriod = int(arg)

def monitorValues():
	'''
		this function will keep on checking on the notificatin peroid. 
	'''	
	global numberOfPackets
	startTime = time()
	stopTime = startTime + statNotPeriod
	while 1:
		if stopTime <= time():
			start_new_thread(writeToPipe, ( str(numberOfPackets) + "time:" + str(time()),))
			stopTime = time() + statNotPeriod
			numberOfPackets = 0
	
def createConnection():
	'''
		This will create a connection.
		@return a socket
	'''
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind((host, port))
	return sock
	
if __name__ == "__main__":
		
	checkArguments(argv)
	sock = createConnection()
	print host
	print "UDP Client: listening.."
	
	if statNotPeriod != 0:
		start_new_thread(monitorValues, ())
	
	while 1:
		data  = sock.recv(bufferSize)
		print "UDP Client : received message " + str(numberOfPackets)
		#print "UDP Client : size:" + str(len(data))
		numberOfPackets += 1
		
		
