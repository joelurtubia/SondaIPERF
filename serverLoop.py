#!/usr/bin/env python

import iperf3
import time

#server = iperf3.Server()
#print('Running server: {0}:{1}'.format(server.bind_address, server.port))


#!/usr/bin/env python

import sys, os, time, atexit
from signal import SIGTERM
import datetime as dt
import time
import sys, time
from classes.daemonClass import Daemon
#import glob
#from classes.extractresults import extractClass

'''
fileConfig = '/home/sonda/configPmt.cfg'
with open(fileConfig) as f:
	for lines in f:
		SelectRow = lines.split(";")
		pathError = SelectRow[0]
		splitName = SelectRow[1]
		searchName = SelectRow[2]
		PathLogs = SelectRow[3]
		pidName = SelectRow[4]

#print PathLogs		
#print pidName
'''
pidName = '/tmp/serveriperf.pid'
PathLogs = '/var/log/logserveriperf.log'
class MyDaemon(Daemon):
	def run(self):
		while True:	
			f = open(PathLogs, "a")
			exct_time = str(dt.datetime.now())	
			try:	
				server = iperf3.Server()
				#print('Restart Server Iperf !!!')
				f.write(('%s -- Restart Server Iperf !!! \n') % (exct_time))
				#print('Running server: {0}:{1}'.format(server.bind_address, server.port))
				f.write(('%s -- Running server: %s:%s !!! \n') % (exct_time,server.bind_address, server.port))
				result = server.run()
				
				
				if result.error:
					#print(result.error)
					f.write(('%s -- Error:  %s \n') % (exct_time,result.error))
				else:
					f.write(('%s -- bits per second :  %s \n') % (exct_time,result.received_Mbps))
					'''
					print('')
					
					print('Test results from {0}:{1}'.format(result.remote_host,result.remote_port))
					print('  started at         {0}'.format(result.time))
					print('  bytes received     {0}'.format(result.received_bytes))

					print('Average transmitted received in all sorts of networky formats:')
					print('  bits per second      (bps)   {0}'.format(result.received_bps))
					print('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
					print('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
					print('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
					print('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))
					print('')
					'''
					
				time.sleep(0.2)
				del server	
				f.write(('%s -- sleep 0,2 seconds!!! \n') % (exct_time))
				#del server
				
						
			except:
				print('Error to start iperf server')
				f.write(('%s -- Error to start iperf server \n') % (exct_time))
				f.write(('%s -- sleep 0,2 seconds!!! \n') % (exct_time))
				del server	
				time.sleep(0.2)		
			f.write(('%s -- ##################$$$$###############!!! \n') % (exct_time))		
			f.close()
    #print 'sleep 5 seconds'
    #time.sleep(5)
    #print '#######################'

if __name__ == "__main__":
	daemon = MyDaemon(pidName)
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)