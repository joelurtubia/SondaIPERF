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

#client = iperf3.Client()

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

networkClass  = networks()
ip,mask,gw,adapter  = networkClass.findipadapters(PathLogs)
print (('this is the ip: %s, Mask : %s,gw : %s, adapter : %s  ')%(ip,mask,gw,adapter))
macadapter  = networkClass.findMacadapters(PathLogs,adapter)
print macadapter
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


#client.json_output = True
client = iperf3.Client()
client.duration = 2
client.omit = 5
client.protocol = 'udp'
client.server_hostname = iperfserver
client.port = iperfport
client.reverse = 0
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
f.write(('%s -- Begin UDP test connection server: %s port: %s \n') % (exct_time,client.server_hostname, client.port))
#print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
result = client.run()

#print '###########$$$$$$$$$$$$$$$$$$$$$###################'

#print result
#print '###########$$$$$$$$$$$$$$$$$$$$$###################'
if result.error:
	#print(result.error)
	f.write(('%s -- Error \n') % (exct_time))
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
	print('  jitter ms : {0}'.format(result.jitter_ms))
	print('  Mbps : {0}'.format(result.Mbps))
	print('  lost_percent : {0}'.format(result.lost_percent))
	
	
	
	#print('  blksize: {0}'.format(result.blksize))
	'''
	# Send metrics to zabbix trapper
	f.write(('%s -- Create packet for send zabbix server \n') % (exct_time))
	packet = [
	  ZabbixMetric(ip, 'bwUp', result.sent_bps),
	  ZabbixMetric(ip, 'bwDown', result.received_bps),
	  #ZabbixMetric('hostname1', 'test[system_status]', "OK"),
	  #ZabbixMetric('hostname1', 'test[disk_io]', '0.1'),
	  #ZabbixMetric('hostname1', 'test[cpu_usage]', 20, 1411598020),
	]

	results = ZabbixSender(client.server_hostname, 10051, chunk_size=1).send(packet)
	f.write(('%s -- data sent zabbix server \n') % (exct_time))	
	### Index data
	networkrtt = 12300
	queryElastic  = elasticfunctions(hostelastic,portelastic)
	resultados  = queryElastic.indexelastic(indexname, hostname,ip,client.duration,result.received_bps,result.sent_bps,networkrtt,ts)
	if resultados == 'error':
		#print ('appears an error in elastic index : %s ' % (indexname))
		f.write(('%s -- appears an error in elastic index  : %s \n') % (exct_time,indexname))	
		#print 'ohhh!!!'
	else:
		f.write(('%s -- Inserted ok in elastic index : %s \n') % (exct_time,indexname))	
		#print resultados['_shards']['successful']
		#print ('Inserted ok in elastic index : %s ' % (indexname))
	'''	
#print '#######################'
#print 'sleep 10 seconds'
del client
f.write(('%s -- sleep 10 seconds\n') % (exct_time))

f.write(('%s -- #############################\n') % (exct_time))
#time.sleep(10)
f.close()
#f.write(('%s -- #############################\n') % (exct_time))
#print '#######################'