#!/usr/bin/env python3

from pyzabbix import ZabbixMetric, ZabbixSender
from elasticsearch import Elasticsearch
from classes.elasticClass import elasticfunctions
from classes.daemonClass import Daemon
from classes.networkclass import networks
import datetime
import iperf3
import time
import sys


################################################
#########Parameters Begin
################################################
fileConfig = '/home/sonda/iperf/config.cfg'
with open(fileConfig) as f:
	for lines in f:
		SelectRow = lines.split(";")
		indexpattern = SelectRow[0]
		bw = int(SelectRow[1])
		framesize = int(SelectRow[2])
		PathLogs = SelectRow[3]
		pidName = SelectRow[4]
		change = int(SelectRow[5])
		iperfserver = SelectRow[6]
		iperfport = SelectRow[7]
		durationsec = int(SelectRow[8])
		hostmanesonda = SelectRow[9]
		hostelastic = SelectRow[10]
		portelastic = SelectRow[11]
		selectadapter = SelectRow[12]

################################################						
###call class()
################################################
networkClass  = networks()
ip,mask,adapter  = networkClass.findipadapters(PathLogs,selectadapter)
macadapter  = networkClass.findMacadapters(PathLogs,adapter)
print PathLogs
counterror = 0
start_run = str(datetime.datetime.now())
#print start_run
class MyDaemon(Daemon):
	def run(self):
	
			while True:
			

				fileConfig = '/home/sonda/iperf/config.cfg'
				with open(fileConfig) as f:
					for lines in f:
						SelectRow = lines.split(";")
						indexpattern = SelectRow[0]
						bw = int(SelectRow[1])
						framesize = int(SelectRow[2])
						PathLogs = SelectRow[3]
						pidName = SelectRow[4]
						change = int(SelectRow[5])
						iperfserver = SelectRow[6]
						iperfport = SelectRow[7]
						durationsec = int(SelectRow[8])
						hostmanesonda = SelectRow[9]
						hostelastic = SelectRow[10]
						portelastic = SelectRow[11]
						selectadapter = SelectRow[12]
		
				try:
					#client.json_output = True
					client = iperf3.Client()
					client.duration = durationsec
					client.omit = 5
					client.server_hostname = iperfserver
					client.port = iperfport
					#client.zerocopy = True
					MBps = 1000000
					client.blksize = framesize
					client.bandwidth = bw*MBps
					client.bind_address = ip
					utc_datetime = datetime.datetime.utcnow()
					exct_time = str(datetime.datetime.now())	
					st = utc_datetime.strftime("%Y-%m-%d")
					indexname = indexpattern+str(st)
					if hostmanesonda == 'generico':
						hostname = 'sonda_'+macadapter
					else:
						hostname = hostmanesonda
					ts = datetime.datetime.utcnow()	
					TimetoStart = str(time.time())
					f = open(PathLogs, "a")
					f.write(('%s -- Begin  connection from server: %s \n') % (exct_time,hostname))
					f.write(('%s -- Begin  connection server: %s port: %s \n') % (exct_time,client.server_hostname, client.port))
					#print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
					result = client.run()

					#print '###########$$$$$$$$$$$$$$$$$$$$$###################'

					#print result
					#print '###########$$$$$$$$$$$$$$$$$$$$$###################'
					if result.error:
						#print(result.error)
						f.write(('%s -- Error to run Iperf \n') % (exct_time))
						counterror = counterror + 1
						f.write(('Start Run program: %s \n') % (start_run))
						f.write(('%s -- number of errors: %s \n') % (exct_time,counterror))
					else:
						f.write(('%s -- mean_rtt : %s \n') % (exct_time,result.json['end']['streams'][0]['sender']['mean_rtt']))
						networkrtt = result.json['end']['streams'][0]['sender']['mean_rtt']
						try:
							# Send metrics to zabbix trapper
							f.write(('%s -- Create packet for send zabbix server \n') % (exct_time))
							packet = [
							  ZabbixMetric(ip, 'bwUp', result.sent_bps),
							  ZabbixMetric(ip, 'bwDown', result.received_bps),
							  #ZabbixMetric('hostname1', 'test[system_status]', "OK"),
							  #ZabbixMetric('hostname1', 'test[disk_io]', '0.1'),
							  #ZabbixMetric('hostname1', 'test[cpu_usage]', 20, 1411598020),
							]
							
							#f.write(('%s\n') % (packet))
							#results = ZabbixSender(client.server_hostname, 10051, chunk_size=1).send(packet)
							results = ZabbixSender(ip, 10051, chunk_size=1).send(packet)
							f.write(('%s -- zabbix server results: %s \n') % (exct_time,results))	
							f.write(('%s -- data sent zabbix server \n') % (exct_time))	
						except:
							f.write(('%s -- Error to send data on zabbix Server \n') % (exct_time))	
						### Index data
						#networkrtt = 12300
						queryElastic  = elasticfunctions(hostelastic,portelastic)
						#f.write(queryElastic)
						resultados  = queryElastic.indexelastic(indexname, hostname,ip,client.duration,result.received_bps,result.sent_bps,networkrtt,ts)
						if resultados == 'error':
							#print ('appears an error in elastic index : %s ' % (indexname))
							f.write(('%s -- appears an error in elastic index  : %s \n') % (exct_time,indexname))	
							#print 'ohhh!!!'
						else:
							f.write(('%s -- Inserted ok in elastic index : %s \n') % (exct_time,indexname))	
							#print resultados['_shards']['successful']
							#print ('Inserted ok in elastic index : %s ' % (indexname))
					#print '#######################'
					#print 'sleep 10 seconds'
				except:
					f.write(('%s -- Error to start cliente iperf on zabbix Server \n') % (exct_time))						
				del client
				f.write(('%s -- sleep 10 seconds\n') % (exct_time))
				f.write(('%s -- ####################	$$$$	#####################\n') % (exct_time))
				f.close()
				time.sleep(10)
				#f.write(('%s -- #############################\n') % (exct_time))
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
