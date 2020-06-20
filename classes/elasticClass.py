from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions
import time
import json
'''
RETRY_ATTEMPTS = 15
RECONNECT_SLEEP_SECS = 0.5
#global msearch
###Call elasticsearch function
esconnection = Elasticsearch([{'host': '172.25.20.111', 'port': 9200}])
'''
class elasticfunctions:

	def __init__(self, hostelastic, port):		
		self.esconnection = Elasticsearch([{'host': hostelastic, 'port': port}])	  
	  

	def indexelastic(self,indexname, hostname,ip,duration,networkInbits,networkOutbits,networkrtt,ts):

						doc ={
							"host.name": hostname,
							'ip' : ip,
							'duration' : duration,
							'network.Inbits' : int(networkInbits),
							'network.Outbits' : int(networkOutbits),
							'network.rtt' : int(networkrtt),
							'@timestamp' : ts
							}
						try:	
							res = self.esconnection.index(index=indexname,body=doc)	
						except :
							res = 'error'
								
						return res
						
	def callDocStructure(self, zonal):

						doc ={
									  "query": { 
										"bool": { 
										  "must": [
											 {"match": { "zonal" : zonal}},
											#{ "match": { "value" : 0}}
										  ],
										}
									  },
									  'size' : 1000,
									  'from' : 0,
									"aggs":{
										"unique_term": {
											"terms": {
												"field": "node"
											}
										}
									}
								}
								
						return doc

	def callItemsId(self, zonal,node,key):

					SearchNodeItems ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "zonal" : zonal}},
							{ "match": { "node" : node}},
							{ "match": { "key_" : key}},

						  ]
						}
					  },
					  'size' : 1000,
					}
					return SearchNodeItems

	def getResultsById(self,itemid,substract):					
					doc ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "itemid" : itemid}},
							#{ "match": { "value" : 0}}
						  ],
						  "filter": [ 
							{ "range": { "clock": { "gte": substract }}} 
						  ]
						}
					  },
					  'size' : 1,
					  'from' : 0,
						 "sort" : [
							{ "clock" : {"order" : "desc"}},
						] 
					}
					return doc

	def getResultsByIdGtLt(self,itemid,gte,lt):					
					doc ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "itemid" : itemid}},
							#{ "match": { "value" : 0}}
						  ],
						  "filter": [ 
							{ "range": 
									{ "clock": 
											{ "gte": gte,"lte" : lt}
										
										}
								
								} 
						  ]
						}
					  },
					  'size' : 1000,
					  'from' : 0,
						 "sort" : [
							{ "clock" : {"order" : "asc"}},
						] 
					}
					return doc					

	def getResultsGt(self,itemid,substract):					
					doc ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "itemid" : itemid}},
							#{ "match": { "value" : 0}}
						  ],
		
						}
					  },
					  'size' : 10,
					  'from' : 0,
						 "sort" : [
							{ "clock" : {"order" : "desc"}},
						] 
					}
					return doc

	def getResultsGt50M(self,substract,gte,lt):					
					doc ={
					
					  "query": { 
						"constant_score" : {
						  "filter": {
					           "bool" : {
									"must" : [
										{ "range": { "value": { "gte": gte,"lte" : lt} } },
										{ "range": { "clock": { "gte": substract }} }
									]
								}
							}
							}
						
					  },
					  'size' : 100,
					  'from' : 0,
						 "sort" : [
							{ "clock" : {"order" : "desc"}},
						],
						"aggs" : {
							"bw" : {
								"terms" : { "field" : "value",  "size" : 15 }
							}
						}						
					}
					return doc
					
	def getHostIDItemId(self,ip,key):					
					doc ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "ip" : ip}},
							{ "match": { "key_" : key}}
						  ]
						}
					  },
					  'size' : 1000,
					  'from' : 0
					}
					return doc

	def getAvgItemID(self,itemid,interval):						
					docAvg ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "itemid" : itemid}},
							#{ "match": { "value" : 0}}
						  ],
						}
					  },

					  "aggs": {
						"bw_per_minute": {	
						  "date_histogram": {
							"field": "clock",	
								"ranges": [
									{ "to": "now-10M/M" }, 
									{ "from": "now-10M/M" } 
								],							
							#"interval": interval
							 #"offset":    "+13h"
							 #"time_zone": "-03:00"
						  },
						  "aggs": {
							"bw": {
							  "sum": {
								"field": "value"
							  }
							}
						  }
						},
						"avg_hour_bw": {
						  "avg_bucket": {
							"buckets_path": "bw_per_minute>bw" 
						  }
						}
					  },
					 'size' : 2,
						 "sort" : [
							{ "clock" : {"order" : "desc"}},
						] 					 
					}
					return docAvg	
					
	def getAvgByItemID(self,itemid,gte,lt):					
					doc ={
					  "query": { 
						"bool": { 
						  "must": [
							{ "match": { "itemid" : itemid}},
							#{ "match": { "value" : 0}}
						  ],
						  "filter": [ 
							{ "range": 
									{ "clock": 
											{ "gte": gte,"lte" : lt}
										
										}
								
								} 
						  ]
						}
					  },
					  'size' : 1000,
					  "aggs": {
						"single_avg_itemid": {
						  "avg": {
							"field": "value"
						  }
						}
					  }
					}
					return doc	
					
	def switch_demo(self, argument):
		switcher = {
			'video': "ONT_WAN_VIDEO",
			'internet': "ONT_WAN_INPUT,ONT_WAN_OUTPUT",
			'icmp': "icmpping"
		}
		return switcher

	def querygetItemID(self,indexName,doc):
		temp = []
		res = esconnection.search(index=indexName, doc_type="values", body=doc)
		#print 'This is the respinse Values : %s' % res
		
		for doc in res['hits']['hits']:
			#print("%s => %s => %s => %s" % (doc['_id'], doc['_source']['itemid'],doc['_source']['value'],doc['_source']['clock']))
			itemid = doc['_source']['itemid']
			range = doc['_source']['range']
			ip = doc['_source']['ip']
			zonal = doc['_source']['zonal']
			node = doc['_source']['node']
			key = doc['_source']['key_']
			temp.append(ip)
			temp.append(zonal)
			temp.append(node)
			temp.append(itemid)
			return temp		
					
	def msearch(self, es_conn, queries, index, doc_type, retries=0):
		"""
		Es multi-search query
		:param queries: list of dict, es queries
		:param index: str, index to query against
		:param doc_type: str, defined doc type i.e. event
		:param retries: int, current retry attempt
		:return: list, found docs
		"""
		#global msearch
		search_header = json.dumps({'index': index, 'type': doc_type})
		request = ''
		for q in queries:
			# request head, body pairs
			request += '{}\n{}\n'.format(search_header, json.dumps(q))
		try:
			resp = es_conn.msearch(body=request, index=index)
			found = [r['hits']['hits'] for r in resp['responses']]
		except (es_exceptions.ConnectionTimeout, es_exceptions.ConnectionError,
				es_exceptions.TransportError):  # pragma: no cover
			#logging.warning("msearch connection failed, retrying...")  # Retry on timeout
			print("msearch connection failed, retrying...")  # Retry on timeout
			if retries > RETRY_ATTEMPTS:  # pragma: no cover
				raise
			time.sleep(RECONNECT_SLEEP_SECS)
			resp = es_conn.msearch(body=request, index=index)
			found = [r['hits']['hits'] for r in resp['responses']]			
			#found = es_conn.msearch(queries=queries, index=index, retries=retries + 1)
		except Exception as e:  # pragma: no cover
			print("msearch error {} on query {}".format(e, queries))
			#logging.critical("msearch error {} on query {}".format(e, queries))
			raise
		return found				
