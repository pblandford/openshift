from __future__ import print_function
from .models import Percentage
from . import pc_definitions
from CurrencyFeed import cf_definitions
import filescan

import os.path
import jsonpickle
import logging
from lockfile import FileLock
from bulk_update.helper import bulk_update

def insertPercentMapToDb(percentMap):
	logging.debug("start db insert")

	# get cached percentMap

	try:
		fullPercentMap = getPercentMapFromDir()
	except IOError as e:
		logging.info("No cached percent map - creating new", exc_info=e)
		fullPercentMap = {}

	print("Full: " + str(len(fullPercentMap)))

	# update cached percentMap with values from new one (cached one should be complete,
	# the new one may be partial)
	for key, value in percentMap.iteritems():
		fullPercentMap[key] = value

	insertList = []
	for key, value in fullPercentMap.iteritems():
		fields = key.split("/")
		period = fields[0]
		sample = fields[1]
		
		# the value is an array of percent sets, one for each currency
		percentSetList = value
		for percentSet in percentSetList:
			# a percent set consists of a currency, and a list of percentages
			currency = percentSet['currency']
			i=0
			for pcVal in percentSet['percentages']:
				percentage = Percentage(currency=currency, period=period, sample=int(sample), percentage=pcVal, number=i)
				insertList.append(percentage)
				i+=1

	logging.debug("Inserting " + str(len(insertList)))
	Percentage.objects.all().delete()
	if len(insertList) > 0:
		Percentage.objects.bulk_create(insertList)
	logging.debug("end db insert")

	# store values as a cache for next time
	insertPercentMapToDir(fullPercentMap)

def percentFileName(period, sample):
	return pc_definitions.percentStoreDir + "/" + period + "_" + str(sample)

def insertPercentMapToDir(percentMap):

	if not os.path.exists(pc_definitions.percentStoreDir):
		os.mkdir(pc_definitions.percentStoreDir)

	lock = FileLock(pc_definitions.lockfile)
	with lock:

		for key, value in percentMap.iteritems():
			fields = key.split("/")
			period = fields[0]
			sample = int(fields[1])

			with open(percentFileName(period, sample), "w") as fh:
				json = jsonpickle.encode(value, unpicklable=False)
				fh.write(json)

def getPercentSetListFromDir(period, sample):

	lock = FileLock(pc_definitions.lockfile)
	logging.debug("opening " + percentFileName(period, sample))
	with lock:
		with open(percentFileName(period, sample), "r") as fh:
			json = fh.read()

	percentSet = jsonpickle.decode(json)

	return percentSet

def getPercentMapFromDir():

	percentMap = {}
	for p in cf_definitions.periods:
		for s in cf_definitions.samples:
			percentSetList = getPercentSetListFromDir(p,s)
			percentMap[filescan.percentmap.periodSampleKey(p,s)] = percentSetList

	return percentMap
	

def getPercentSetListFromDb(period, sample):

	percentList = Percentage.objects.filter(period=period, sample=sample)

	percentSet = []
	for c in cf_definitions.currencies:
		percentForCurrency = {"currency": c, "percentages" : []}
		percentObjects = Percentage.objects.filter(period=period, sample=sample, currency=c).order_by('number')
		print("found " + str(len(percentObjects)) + " Objects")
		for po in percentObjects:
			percentForCurrency["percentages"].append(po.percentage)
		percentSet.append(percentForCurrency)
		
	return percentSet
