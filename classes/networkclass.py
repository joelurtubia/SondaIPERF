#!/usr/bin/env python

import sys, os, time, atexit
from signal import SIGTERM
import datetime as dt
import time
import sys, time
import ifaddr
import socket
import re
import datetime
#from classes.MysqlClass import mysqlClass
import netifaces
import logging

class networks:

			
			
			def __init__(self):
			
				self.exct_time = str(datetime.datetime.now())
				
			'''
			def __init__(self):
				try:
					self.mysqlcass = mysqlClass()
					self.path = '/etc/sysconfig/network-scripts/ifcfg-'
					#self.PathLogs = '/home/sonda/pidAndLogs/logchangeip.log'
					self.exct_time = str(datetime.datetime.now())
					self.secs = 0.500
					########################################################
					# create logger
					self.logger = logging.getLogger("simple_example")
					self.logger.setLevel(logging.DEBUG)
					# create console handler and set level to debug
					ch = logging.StreamHandler()
					ch.setLevel(logging.DEBUG)
					# create formatter
					formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
					# add formatter to ch
					ch.setFormatter(formatter)
					# add ch to logger
					self.logger.addHandler(ch)
					########################################################
					
				except MySQLdb.Error, e:
					print e.args
					print 'ERROR: %d: %s' % (e.args[0], e.args[1])
					sys.exit(1)
			
			'''
			def filexits (self,findeAdapter,f):
				##Check if file to change exists	
				if (os.path.isfile(self.path+findeAdapter)):
					print 'file exists'
					f.write(('%s -- file exists: %s \n')% (self.exct_time,findeAdapter))
					return True
				else:
					print 'file not exists'
					f.write(('%s -- file NOT exists: %s \n')% (self.exct_time,findeAdapter))
					return False
					sys.exit()

			def stopsoftware (self,f):
				f.write(('%s --- Stop all daemon \n') % (self.exct_time))
				os.system("/usr/bin/python /home/sonda/daemon/daemonStatusStream.py stop")
				time.sleep(self.secs)
				os.system("/usr/bin/python /home/sonda/daemon/daemonPmt.py stop")
				time.sleep(self.secs)
				os.system("/usr/bin/python /home/sonda/daemon/daemonStatistics.py stop")
				time.sleep(self.secs)
				os.system("/usr/bin/python /home/sonda/daemon/daemonErrorTs.py stop")
				time.sleep(self.secs)
				os.system("/usr/bin/python /home/sonda/daemon/daemonRemoveFiles.py stop")
				time.sleep(self.secs)
				f.write(('%s --- finish Stop all daemon \n') % (self.exct_time))
				resultsQuery = self.mysqlcass.fetchall(("select NfqueueNum,mcast,status,UNIX_TIMESTAMP(timeMcast) from mcast;"))
				#print(resultsQuery)
				f.write(('%s --- Query : %s \n') % (self.exct_time,resultsQuery))
				for row in resultsQuery:
					NfqueueNum  = row[0]
					mcast  = row[1]
					status  = int(row[2])
					timeMcast  = row[3]
					#timeDB = time.mktime(datetime.datetime.strptime(timeMcast, "%d/%m/%Y %H:%m").timetuple())
					#print(timeMcast)
					os.system(("/usr/bin/python /home/sonda/daemon/daemonAnalizer.py stop %s") % (NfqueueNum))
					f.write("%s --- Stop Mcast: %s \n" % (self.exct_time,mcast))
					time.sleep(self.secs)	
				f.write(('%s --- stop mariadb service \n') % (self.exct_time))
				os.system("systemctl stop mariadb")	
				time.sleep(self.secs)
				f.write(('%s --- stop grafana-server service \n') % (self.exct_time))
				os.system("systemctl stop grafana-server")
				time.sleep(self.secs)				
				f.write('########################## \n')
				f.write('Finish to Stop Daemon scripts \n')

					


		

			def chekifreboot (self,):
					f = open(self.PathLogs, "a")
					try:
						querydata = self.mysqlcass.query("SELECT changeIP from systemIP where changeIP=1;")
						print 'This is query : %s' % querydata[0]
						if (querydata[0] == 1):
							print 'need to reboot %s' % querydata
							f.write(('%s --  need to reboot \n') % (self.exct_time))
						else:
							f.write(('%s --  NOT need to reboot\n')% (self.exct_time))
								
						f.write(('%s --  Interface Query \n')% (self.exct_time))
						f.close()
					except:
						
						
						f.write(('%s -- ERROR !!! ,Interface Query\n')% (self.exct_time))
						
					f.close()

			def reboot (self,f):
					f.write(('%s -- reboot system \n')% (self.exct_time))
					f.write(('%s -- ##### 25 percent ... reboot progress  \n')% (self.exct_time))
					f.write(('%s -- ########## 50 percent ...  reboot progress  \n')% (self.exct_time))
					f.write(('%s -- ############### 100 percent ... now reboot \n')% (self.exct_time))
					os.system('reboot')		
					
					
			def getIpfromDb (self,PathLogs):
			
					f = open(PathLogs, "a")
					f.write('Check if adapters found in DB \n')
					f.close
					self.findipadapters(PathLogs)
					
					f = open(PathLogs, "a")
					try:
						querydata = self.mysqlcass.mysqlfetchall("SELECT id,adapter,ip,mask,gw,proto,changeIP,speed,traffic from systemIP where changeIP=1;")
						#print 'This is query : %s' % querydata[0]
						f.write(('%s --  Results of query: %s \n')% (self.exct_time,querydata))
						print querydata
						if (querydata != False):
							for row in querydata:
								print("changeip ?? = %s" % row[6])
								f.write(('%s --  changeip ?? = %s \n')% (self.exct_time,row[6]))							
								if (row[6] ==1):
									id = row[0]
									adapter = row[1]
									ip = row[2]
									mask = row[3]
									gw = row[4]
									proto = row[5]
									changeIP = row[6]
									speed = row[7]
									traffic = int(row[8])
									print 'need to change '
									f.write(('%s -- ERROR !!! ,Need to change IP : %s \n')% (self.exct_time,adapter))
									f.write(('%s -- id: %s,adapter: %s,ip: %s,mask: %s,gw: %s,proto: %s,changeIP: %s,f: %s,speed: %s,traffic: %s \n')% (self.exct_time,id,adapter,ip,mask,gw,proto,changeIP,f,speed,traffic))
									self.writenewIP(id,adapter,ip,mask,gw,proto,changeIP,speed,traffic,PathLogs)
								else:
									f.write(('%s --  NOT need to change IP from adapter :%s \n')% (self.exct_time,row[1]))
						else:
							f.write(('%s -- Not Results found in query, NOT need to change IP from adapter \n')% (self.exct_time))
								
					except:	
						f.write(('%s -- ERROR !!! ,Interface Query not need to change any IP from interface : %s\n')% (self.exct_time,adapter))
						
					f.close()
					
			def checkInArray(self,findValue,arrayValues):
				
					r = re.compile(findValue)
					newlist = list(filter(r.findall, arrayValues)) # Read Note
					print newlist
					if newlist:
						return True
					else:
						return False
			def getspeed(self,argument):
				if (argument == 1):
					ETHTOOL_OPTS = "speed 100 duplex full autoneg off"
					return ETHTOOL_OPTS
				elif(argument == 2):
					ETHTOOL_OPTS = "speed 1000 duplex full autoneg off"
					return ETHTOOL_OPTS
				elif(argument == 3):
					ETHTOOL_OPTS = "autoneg on"
					return ETHTOOL_OPTS
					
			def findipadapters (self,PathLogs,selectadapter):
			#def findipadapters (self,PathLogs):
					#self.filexits(path)
					f = open(PathLogs, "a")
					f.write(('%s --  begin function findipadapters() \n')% (self.exct_time))
					f.write(('%s \n')% (netifaces.interfaces()))
					

					for adapter in netifaces.interfaces():
						#print adapter
						f.write (('This is the adapter: %s\n') % (adapter))
						addrs = netifaces.ifaddresses(adapter)
						f.write('IP Adapter address  \n')
						f.write(('%s \n')% (addrs))
						try:
							IP = addrs[netifaces.AF_INET]
							for IPaddr in IP:
								if (IP[0]['addr'] != '127.0.0.1'):  			
									#print IP[0]['addr']
									ip = IP[0]['addr']
									#print IP[0]['netmask']
									mask = IP[0]['netmask']
									#print 'this is IP: '+ip
									f.write('################################################\n')
									f.write(('IP: %s, mask: %s, adapter: %s')%(ip,mask,adapter))
									#print '##########\n'
									#print 'this is the adapter : '+adapter
									if (selectadapter == adapter):
										f.write('################################################\n')
										f.write(('Adapter found !!!, IP: %s, mask: %s, adapter: %s')%(ip,mask,adapter))
										return (ip,mask,adapter)						
									
									
						except:
							print 'Not IPv4 for interface : %s' % adapter	

			def findMacadapters (self,PathLogs,adapter):
					#self.filexits(path)
					f = open(PathLogs, "a")
					f.write(('%s --  begin function findMacadapters() \n')% (self.exct_time))
					f.write (('This is the adapter: %s\n') % (adapter))
					addrs = netifaces.ifaddresses(adapter)
					#print addrs
					try:
						IP = addrs[netifaces.AF_LINK]
						for IPaddr in IP:
							addr = IP[0]['addr']
							mac = addr.replace(':','')
							return mac.upper()
								
					except:
						print 'Not Mac IPv4 for interface : %s' % adapter	
							
						
						
			def writenewIP (self,id,adapter,ip,mask,gw,proto,changeIP,speed,traffic,PathLogs):
						f = open(PathLogs, "a")
						try:
							newIP = ip
							findeAdapter = adapter
							gateway = gw
							protocol = proto
							#f.write(('%s -- protocol is static,add IP :%s \n')% (self.exct_time,newIP))	
							ifcfg = []
							ETHT_OPTS = self.getspeed(speed)
							f.write(('%s -- ETHT_OPTS: %s \n')% (self.exct_time,ETHT_OPTS))
							#with open (path+findeAdapter, 'r' ) as f:
							checkfile = self.filexits(findeAdapter,f)
							f.write(('%s -- Check if file exists: %s \n')% (self.exct_time,findeAdapter))
							if checkfile == True:
									f.write(('%s -- exists file, open : %s \n')% (self.exct_time,findeAdapter))
									input_file = open(self.path+findeAdapter, "r")
									for line in input_file:
										lineclean = line.rstrip()
										#print 'begin #########'
										#print lineclean
										#print 'end #########'
										
										match_BOOTPROTO = re.findall('BOOTPROTO', lineclean) # should be your regular expression
										match_IPADDR = re.findall('IPADDR', lineclean) # should be your regular expression
										match_NETMASK = re.findall('NETMASK', lineclean) # should be your regular expression
										match_GATEWAY = re.findall('GATEWAY', lineclean) # should be your regular expression
										match_DEFROUTE = re.findall('DEFROUTE=', lineclean) # should be your regular expression
										
										match_ETHTOOL_OPTS = re.findall('ETHTOOL_OPTS', lineclean) # should be your regular expression
										if match_BOOTPROTO:
											print 'find bootproto'
											f.write(('%s -- Adapter values : %s  protocol : %s \n')% (self.exct_time,findeAdapter,protocol))
											search = lineclean.split("=")
											#print search
											if protocol == 'static':
												print 'find dhcp value'
												lineclean='BOOTPROTO=static'
											else:
												lineclean='BOOTPROTO=dhcp'
												
										###Check if protocol is static		
										if 	protocol == 'static':			
											
											f.write(('%s -- protocol is static \n')% (self.exct_time))													
											if match_IPADDR and protocol=='static':
												lineclean='IPADDR='+newIP
												f.write(('%s -- protocol is static,add IP:%s \n')% (self.exct_time,newIP))	
											if match_NETMASK and protocol=='static':
												lineclean='NETMASK='+mask
												
											if match_GATEWAY and protocol=='static':
												if gateway == 'none':
													lineclean='#GATEWAY='
												else:
													lineclean='GATEWAY='+gateway		
											#f.write(('%s -- write static options\n')% (self.exct_time))
											if match_ETHTOOL_OPTS:
												lineclean=('ETHTOOL_OPTS="%s"')% (ETHT_OPTS)					
												f.write(('%s -- write ETHTOOL_OPTS: %s \n')% (self.exct_time,ETHT_OPTS))

											if match_DEFROUTE:
												lines = lineclean.split("=")												
												if traffic == 1:
													lineclean = lines[0]+'=NO'
												else:
													lineclean = lines[0]+'=YES'
												f.write(('%s -- write DEFROUTE: %s \n')% (self.exct_time,lineclean))												
											
										else:
											
											if match_IPADDR:
												print 'find'
												lineclean='#IPADDR='
											if match_NETMASK:
												lineclean='#NETMASK='
											if match_GATEWAY:
												lineclean='#GATEWAY='
											if match_ETHTOOL_OPTS:
												lineclean=('ETHTOOL_OPTS="%s"')% (ETHT_OPTS)
											if match_DEFROUTE:
												lines = lineclean.split("=")												
												if traffic == 1:
													lineclean = lines[0]+'=NO'
												else:
													lineclean = lines[0]+'=YES'
												f.write(('%s -- write DEFROUTE: %s \n')% (self.exct_time,lineclean))												
											
										ifcfg.append(lineclean)	
									
									#f.write(('%s -- array appened in ETHTOOL_OPTS: %s \n')% (self.exct_time,lineclean))									
									#print ifcfg
									checkip = self.checkInArray('IPADDR',ifcfg)
									print checkip
									checkmask = self.checkInArray('NETMASK',ifcfg)
									#print checkmask
									checkgw = self.checkInArray('GATEWAY',ifcfg)
									#print checkgw
									chekopts = self.checkInArray('ETHTOOL_OPTS',ifcfg)
									
									chekdefroute = self.checkInArray('DEFROUTE',ifcfg)
									
									if checkip == False and protocol=='static':
										lineclean='IPADDR='+newIP
										ifcfg.append(lineclean)
									if checkip == False and protocol=='dhcp':
										lineclean='#IPADDR='
										ifcfg.append(lineclean)
									
									
									if checkmask == False and protocol=='static':
										lineclean='NETMASK='+mask
										ifcfg.append(lineclean)
										
									if checkmask == False and protocol=='dhcp':
										lineclean='#NETMASK='
										ifcfg.append(lineclean)
									
									if chekopts == False:
										lineclean=('ETHTOOL_OPTS="%s"')% (ETHT_OPTS)	
										ifcfg.append(lineclean)	
										f.write(('%s -- array appened in ETHTOOL_OPTS: %s \n')% (self.exct_time,lineclean))										
									
									if checkgw == False and protocol=='static':
										if gateway == 'none':
											lineclean='#GATEWAY='
											ifcfg.append(lineclean)
										else:
											lineclean='GATEWAY='+gateway
											ifcfg.append(lineclean)
											
									#if checkgw == False and protocol=='dhcp':
									#	lineclean='#GATEWAY='
									#	ifcfg.append(lineclean)
									
									print ifcfg
									f.write(('%s -- Adapter values : %s \n')% (self.exct_time,findeAdapter))
									f.write(('%s \n') % (ifcfg))
									input_file.close()
									print'close file'
									
									with open((self.path+findeAdapter), "w") as file:
										for item in ifcfg:
											file.write("%s\n" % item)
											f.write(('%s -- wirte value :%s \n')% (self.exct_time,item))
											#print ("wirte value :%s\n" % item)

									try:
										querydata = self.mysqlcass.insert(("UPDATE systemIP SET changeIP = 0 WHERE adapter='%s';") % (findeAdapter))
										f.write(('%s --  update changeIP  from adapter : %s \n')% (self.exct_time,findeAdapter))
										time.sleep(5)
										self.stopsoftware(f)
										self.reboot(f)
									except:
										
										
										f.write(('%s -- Error update changeIP  from adapter : %s \n')% (self.exct_time,findeAdapter))
										
						
											
									# legal
							else:
								#print 'file %s not exists' % 
								f.write(('%s -- file no exists : %s \n')% (self.exct_time,self.path+findeAdapter))
									
								print '#############################################################'


						except:
							
							f.write(('%s -- error in function writenewIP  \n')% (self.exct_time))


