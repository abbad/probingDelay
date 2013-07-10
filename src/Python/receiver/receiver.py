'''
Created on may 7, 2013

@author: Abbad

This module will call UDP server and TCP server.

'''

from subprocess import Popen
from time import sleep
from os import system, remove, listdir, pipe, fdopen, close, O_WRONLY, O_RDONLY
from os import path as osPath
from inspect import currentframe, getfile
from sys import path

# code to include subfolder modules (packages)
cmd_subfolder = osPath.realpath(osPath.abspath(osPath.join(osPath.split(getfile( currentframe() ))[0],"subfolder")))
if cmd_subfolder not in path:
	path.insert(0, cmd_subfolder)

from utilities.getChar import *
from utilities.user_pipes import preparePipes, closePipe

def cleanUp():
	'''
		delete all xml files that are generated by udp server.
	'''
	for files in listdir("."):
			if files.endswith(".xml"):
				remove(files)
				
def menu():
	
	p1 = None
	p2 = None
	
	while 1:
		print "Select one of the following:"
		print "1. start TCP Client"
		print "2. start UDP Server"
		print "3. quit"
		getch = Getch() 
		val = getch.__call__()
		if val == '1':
			p1 = launchTCPClient()
		if val == '2':
			p2 = launchUdpServer()
		if val == '3':
			try:
				if p1:
					p1.terminate()
				if p2:
					p2.terminate()
			except:
				print "error while terminating one of the processes"
			exit()
			
'''
	@pipeArg1 This is for sending command and also notification period to receiver. 
	@pipeArg2 This is for statistics. 
'''
def launchTcpClient(pipeArg1, pipeArg2):
	print 'Starting TCP client'
	args = ["python", "TCPClient.py", "-a", pipeArg1, "-v", pipeArg2]
	return Popen(args, shell=False)

'''
	@pipeArg1 This is for sending statistics. 
'''
def launchUdpServer(notificationPeriod):
	print 'Starting UDP server'
	args =  ["python", "UDPserver.py", "-n", notificationPeriod]
	p2 = Popen(args, shell=False)

'''
	 Create pipe for communication between tcp client and udp server. 
	 this pipe will send the statistics from udp server to tcp client. 
'''
def createPipesForStatistics():
	
	pipeout_tcpClient, pipein_udpserver = pipe()
	
	#prepare pipeOut for tcp client
	tcp_pipeArg, tcp_pipeHandler = preparePipes(pipeout_tcpClient, pipein_udpserver)
	
	#prepare pipeIn for udp Server
	udp_pipeArg, udp_pipeHandler = preparePipes(pipein_udpserver, pipeout_tcpClient)
	
	return tcp_pipeArg, tcp_pipeHandler, udp_pipeArg, udp_pipeHandler
	
if __name__ == '__main__':

	pipes = createPipesForStatistics()
	
	# Create pipe for communication
	pipeout, pipein = pipe()
	
	pipearg, pipeHandler = preparePipes(pipein, pipeout)

	# Start child with argument indicating which FD/FH to read from
	TCPsubproc = launchTcpClient(pipearg, pipes[0])
	
	# Close write end of pipe in parent
	closePipe(pipein, pipeHandler)
	
	# Close both ends of statistics pipes 
	closePipe(pipes[0], pipes[1])
	closePipe(pipes[2], pipes[3])

	# Read from child (could be done with os.write, without os.fdopen)
	pipefh = fdopen(pipeout, 'r')
	message = pipefh.read()
	
	if(message[0:14] == "startUdpServer"):
		UDPServerSubProc = launchUdpServer(message[14:], pipes[2])  
	
	pipefh.close()

	# Wait for the child to finish
	#TCPsubproc.wait()
	
	
	# to do : implement a pipe to connect the tcp client with udp server wherein the udpserver sends statistics to udp client. 