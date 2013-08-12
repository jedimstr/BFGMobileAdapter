BFGMobile
=========
Originally derived from Christian Berendt's api-example.py for BFGMiner for the BFG RPC Portion of the script
Copyright 2013 Philip De Leon


Description:  
This is a simple Python Script to take data from the BFGMiner RPC and send it to the MobileMiner Apps' REST API.
See more info on the MobileMiner suite of Monitoring and Control Apps, check out http://www.mobileminerapp.com/

Right now this script only posts data to the API for monitoring and does not allow for remote Miner control.
It is currently set for a time-interval of 30 seconds between POSTs to the API.  This is configurable from within the script.
