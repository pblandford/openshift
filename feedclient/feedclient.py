#!/usr/bin/python

import httplib
from datetime import datetime
import time

from CurrencyFeed import cf_definitions

allPairs = "AUD/CAD,AUD/CHF,AUD/JPY,AUD/NZD,AUD/USD,CAD/CHF,CAD/JPY,CHF/JPY,EUR/AUD,EUR/CAD,EUR/CHF,EUR/GBP,EUR/JPY,EUR/NZD,EUR/USD,GBP/AUD,GBP/CAD,GBP/CHF,GBP/JPY,GBP/NZD,GBP/USD,NZD/CAD,NZD/CHF,NZD/JPY,NZD/USD,USD/CAD,USD/CHF,USD/JPY"

username = "pblandford"
password = "FadgTwbaem88"
baseurl = "webrates.truefx.com"
path="/rates/connect.html"
qualifier="CSIFeed"
MAX_LINES=100


def establish():

	params = "?u=%s&p=%s&q=%s&c=%s" % (username, password, qualifier, allPairs)
	connection = httplib.HTTPConnection(baseurl)
	connection.connect()
	connection.request('GET', path + params)

	response = connection.getresponse()

	if response.status != 200:
		print(response.status, response.reason)
		raise Exception("Got response %d" % response.status)

	sessionId = response.read().strip()

	return connection, sessionId


def getTicks(connection, sessionId):

	params = "?id=%s&f=csv" % sessionId
	connection.request('GET', path+params)
	response = connection.getresponse()

	if response.status != 200:
		print(response.status, response.reason)
		raise Exception("Got response %d" % response.status)

	return response.read().strip().split('\n')

def getFormatted(fullDate, openPrice):
	return ("%s;%s" %(openPrice, fullDate.strftime("%Y.%m.%d %H:%M:%S")))

def doWrite(fullDate, openPrice, file):
	print(file)
	line = getFormatted(fullDate, openPrice)

	with open(file) as fh:
		lines = fh.readlines()
		if len(lines) >= MAX_LINES:
			#import pdb; pdb.set_trace()
			newlines = [line] + lines[0:-1]
		else:
			newlines = [line] + lines

	with open(file, "w") as fh:
		for l in newlines:
			fh.write(l.strip() + "\n")

def writeByTime(fullDate, pair, openPrice, period):
	
	dir = cf_definitions.ramdir + "/" + pair.replace("/","")
	file = dir + "/PERIOD_" + period

	if isTime(period, fullDate):
		doWrite(fullDate, openPrice, file)	
	
def isTime(period, fullDate):
	if period == "M1":
		return True
	if period == "M5" and fullDate.minute % 5 == 0:
		return True
	if period == "M15" and fullDate.minute % 15 == 0:
		return True
	if period == "M30" and fullDate.minute % 30 == 0:
		return True
	if period == "H1" and fullDate.minute == 0:
		return True
	if period == "H4" and fullDate.minute == 0 and fullDate.hour % 4 == 0:
		return True
	if period == "D1" and fullDate.minute == 0 and fullDate.hour == 0:
		return True
	if period == "W1" and fullDate.minute == 0 and fullDate.hour == 0 and fullDate.weekday() == 0:
		return True
	if period == "MN1" and fullDate.minute == 0 and fullDate.hour == 0 and fullDate.day == 1:
		return True

	return False

def parseLine(line):
	print(line)
	fields = line.split(',')
	pair = fields[0]
	currentTime = datetime.today()
	bidPrice = fields[2] + fields[3]

	for period in cf_definitions.periods:
		writeByTime(currentTime, pair, bidPrice, period)


def parseData(tickData):
	
	for line in tickData:
		parseLine(line)

def update():
	connection, sessionId = establish()
	tickData = getTicks(connection, sessionId)
	parseData(tickData)

