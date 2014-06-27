#!/usr/bin/python
#
# Originally derived from Christian Berendt's api-example.py for BFGMiner for the BFGMinerRPC Portion of the script
# Script was made to run with Python 2.x.  It may need to be substantially modified to work with Python 3.x.
#
# BFGMobileAdapter version 1.0.4
#
# Copyright 2013 Philip De Leon
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.  See COPYING for more details.

import os
import time
import datetime
import argparse
import json
import logging
import pprint
import socket
import urllib
import urllib2

print '[ -=-=-=-=- Starting BFGMobileAdapter - BFGMiner to MobileMiner Interface -=-=-=-=- ]'
while 1:
	logging.basicConfig(
			 format='%(asctime)s %(levelname)s %(message)s',
			 level=logging.DEBUG
	)
	
# Edit these values for individual Miner Instance
# --- Begin Miner Configuration ---
	emailAddy = 'yourEmail@email.com'
	applicationKey = 'ApplicationKey'
	machineName = 'Miner Machine Name'
# --- End Miner Configuration  ---

	apiKey = 'yIiEyL50VuMVdp'	
	reqURL = 'https://mobileminer.azurewebsites.net/api/MiningStatisticsInput?emailAddress='+emailAddy+'&applicationKey='+applicationKey+'&machineName='+machineName+'&apiKey='+apiKey

	parser = argparse.ArgumentParser()
	parser.add_argument("command", default="devs", nargs='?')
	parser.add_argument("parameter", default="", nargs='?')
	parser.add_argument("--hostname", default="localhost")
	parser.add_argument("--port", type=int, default=4028)
	args = parser.parse_args()

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		s.connect((args.hostname, args.port))
	except socket.error, e:
		logging.error(e)

	try:
		s.send("{\"command\" : \"%s\", \"parameter\" : \"%s\"}"
				% (args.command, args.parameter)
			  )
	except socket.error, e:
		logging.error(e)

	data = []
	data2 = []
	print '['+str(datetime.datetime.now()).split('.')[0]+']  Getting Data from BFGMiner RPC API using port:'+str(args.port)
	try:
		data = s.recv(32768)
	except socket.error, e:
		logging.error(e)

	try:
		s.close()
	except socket.error,e:
		logging.error(e)

	if data:
		data = json.loads(data.replace('\x00', ''))

	for item in data['DEVS']:
		device = dict()
		device[u'MinerName'] = u'BFGMobileAdapter'
		device[u'CoinSymbol'] = u'BTC'
		device[u'CoinName'] = u'Bitcoin'
		device[u'Algorithm'] = u'SHA-256'
		if not item.get('Name'):
				device[u'Kind'] = u'GPU'
				device[u'FanSpeed'] = item[u'Fan Speed']
				device[u'FanPercent'] = item[u'Fan Percent']
				device[u'GpuClock'] = item[u'GPU Clock']
				device[u'MemoryClock'] = item[u'Memory Clock']
				device[u'GpuVoltage'] = item[u'GPU Voltage']
				device[u'GpuActivity'] = item[u'GPU Activity']
				device[u'PowerTune'] = item[u'Powertune']
				device[u'Intensity'] = item[u'Intensity']
		elif item[u'Name'] == u'OCL':
				device[u'Kind'] =  item[u'Name']
				device[u'FanSpeed'] = item[u'Fan Speed']
				device[u'FanPercent'] = item[u'Fan Percent']
				device[u'GpuClock'] = item[u'GPU Clock']
				device[u'MemoryClock'] = item[u'Memory Clock']
				device[u'GpuVoltage'] = item[u'GPU Voltage']
				device[u'GpuActivity'] = item[u'GPU Activity']
				device[u'PowerTune'] = item[u'Powertune']
				device[u'Intensity'] = item[u'Intensity']
		else:
				device[u'Kind'] = item[u'Name']
		if not item.get('Name'):
				device[u'Index'] = item[u'GPU']
		else:
				device[u'Index'] = item[u'ID']
		if item[u'Enabled'] == u'Y':
			device[u'Enabled'] = True
		else:
			device[u'Enabled'] = False
		if u'Temperature' in item:
			device[u'Temperature'] = item[u'Temperature']
		device[u'Status'] = item[u'Status']
		device[u'AverageHashrate'] = item[u'MHS av'] * 1000
		device[u'CurrentHashrate'] = item[u'MHS 5s'] * 1000
		device[u'AcceptedShares'] = item[u'Accepted']
		device[u'RejectedShares'] = item[u'Rejected']
		device[u'HardwareErrors'] = item[u'Hardware Errors']
		device[u'Utility'] = item[u'Utility']		
		data2.append(device)

	req = urllib2.Request(reqURL)
	req.add_header('Content-Type', 'application/json')
	
	try: 
		response = urllib2.urlopen(req, json.dumps(data2))
	except urllib2.HTTPError, e:
		logging.warning('HTTPError = ' + str(e.code))
	except urllib2.URLError, e:
		logging.warning('URLError = ' + str(e.reason))
	except httplib.HTTPException, e:
		logging.warning('HTTPException')
	except Exception:
		import traceback
		logging.warning('Generic Exception: ' + traceback.format_exc())
		
	print '['+str(datetime.datetime.now()).split('.')[0]+']  Sending to MobileMiner API from '+machineName  
	time.sleep(30)

	
