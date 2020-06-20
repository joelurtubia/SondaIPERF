#!/usr/bin/env python3

from pyzabbix import ZabbixMetric, ZabbixSender
from elasticsearch import Elasticsearch
from classes.elasticClass import elasticfunctions
import datetime
import iperf3
import time

#client = iperf3.Client()


PathLogs = '/home/sonda/iperf/logiperf.log'
while True:

	#client.json_output = True
	client = iperf3.Client()
	client.duration = 5
	client.omit = 5
	client.server_hostname = '172.16.78.242'
	client.port = 5201
	client.zerocopy = True
	MBps = 1000000
	client.blksize = 1348
	client.bandwidth = 100*MBps
        client.bind_address = '172.16.78.196'
	##Get last records from 2 minutes ago
	#st = datetime.today().isoformat()
	#st = datetime.date.today().isoformat()
	utc_datetime = datetime.datetime.utcnow()
	st = utc_datetime.strftime("%Y-%m-%d")
	#today = date.today().isoformat()
	indexname = 'sondas-'+str(st)
	hostelastic = '172.16.78.242'
	port = 9200
	hostname = 'sondaLab'
	ip = '172.16.78.196'
	ts = datetime.datetime.utcnow()	
	TimetoStart = str(time.time())
	f = open(PathLogs, "a")
	f.write(('%s -- Begin  connection server: %s port: %s \n') % (TimetoStart,client.server_hostname, client.port))
	#print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
	result = client.run()

	#print '###########$$$$$$$$$$$$$$$$$$$$$###################'

	#print result
	#print '###########$$$$$$$$$$$$$$$$$$$$$###################'
	if result.error:
		#print(result.error)
		f.write(('%s -- Error \n') % (TimetoStart))
	else:
		#print('')
		#print (result.json)
		#print('Test completed:')
		#print('  started at         {0}'.format(result.time))
		#print('  bytes transmitted  {0}'.format(result.sent_bytes))
		#print(' retransmits        {0}'.format(result.retransmits))
		#print(' jitter (ms) {0}'.format(result.jitter_ms))	
		#print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))

		#print('Average transmitted data in all sorts of networky formats:')
		#print(' Sent bits per second      (bps)   {0}'.format(result.sent_bps))
		#print(' Sent Kilobits per second  (kbps)  {0}'.format(result.sent_kbps))
		#print(' Sent Megabits per second  (Mbps)  {0}'.format(result.sent_Mbps))
		#print(' Sent KiloBytes per second (kB/s)  {0}'.format(result.sent_kB_s))
		#print(' Sent MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))
		#print('  Duracion en seg: {0}'.format(client.duration))
		#print('  Protocolo : {0}'.format(result.protocol))
		#print('  blksize: {0}'.format(result.blksize))
		
		# Send metrics to zabbix trapper
		f.write(('%s -- Create packet for send zabbix server \n') % (TimetoStart))
		packet = [
		  ZabbixMetric(ip, 'bwUp', result.sent_bps),
		  ZabbixMetric(ip, 'bwDown', result.received_bps),
		  #ZabbixMetric('hostname1', 'test[system_status]', "OK"),
		  #ZabbixMetric('hostname1', 'test[disk_io]', '0.1'),
		  #ZabbixMetric('hostname1', 'test[cpu_usage]', 20, 1411598020),
		]

		results = ZabbixSender(client.server_hostname, 10051, chunk_size=1).send(packet)
		f.write(('%s -- data sent zabbix server \n') % (TimetoStart))	
		### Index data
		networkrtt = 12300
		queryElastic  = elasticfunctions(hostelastic,port)
		resultados  = queryElastic.indexelastic(indexname, hostname,ip,client.duration,result.received_bps,result.sent_bps,networkrtt,ts)
		if resultados == 'error':
			#print ('appears an error in elastic index : %s ' % (indexname))
			f.write(('%s -- appears an error in elastic index  : %s \n') % (TimetoStart,indexname))	
			#print 'ohhh!!!'
		else:
			f.write(('%s -- Inserted ok in elastic index : %s \n') % (TimetoStart,indexname))	
			#print resultados['_shards']['successful']
			#print ('Inserted ok in elastic index : %s ' % (indexname))
	#print '#######################'
	#print 'sleep 10 seconds'
	del client
	f.write(('%s -- sleep 10 seconds\n') % (TimetoStart))
	f.close()
	time.sleep(10)	
	#print '#######################'
