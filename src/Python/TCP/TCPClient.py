'''
Created on Apr 29, 2013

@author: Abbad
'''

import socket
import os
import sys, getopt
import time

# global variables 
host = "localhost"
port = 5005

def printHelp():
	'''
		this is to print options.
	'''
	print 'This is a TCP client:'
	print 'usage:'
	print '-l localHost \t\t\t default localhost'
	print '-p port number \t\t\t default 5005'
	
def checkArguments(argv):
	'''
		this is to check arguments.
	'''
	try:
		opts, args = getopt.getopt(argv[1:],"hl:p:",["host", "portNumber"])
	except getopt.GetoptError:
		print 'TCPClient.py -l <hostname> -p <port>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			printHelp()
			sys.exit()
		elif opt in ('-l'):
			global host
			host = arg
		elif opt in ('-p'):
			global port
			port = int(arg)
	
def getStatistics():
	'''
		this is to open and read the statistics which are dumped from udp server.
	'''
	
	with open(fileName,'r') as f:
		read_data = f.read()
	
	f.close()
	
	return read_data 
	
if __name__ == '__main__':
	'''
		start of the program.
	'''
	checkArguments(sys.argv)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	
	while 1:
		
		s.send(getStatistics())
		
	
	s.close()
	