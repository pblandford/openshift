from __future__ import print_function
from .models import Percentage
from . import pc_definitions
from CurrencyFeed import cf_definitions

import os.path
import jsonpickle
import logging
from lockfile import FileLock

def insertPercentMapToDb(percentMap):
	logging.debug("start db insert")
	Percentage.objects.all().delete()

	insertList = []
	for key, value in percentMap.iteritems():
		fields = key.split("/")
		period = fields[0]
		sample = int(fields[1])

		percentSetList = value
		for percentSet in percentSetList:
			i=0
			currency = percentSet['currency']
			for pcVal in percentSet['percentages']:
				insertList.append(Percentage(currency=currency, percentage=float(pcVal), sample=sample, \
					number=i, period=period))
				i += 1

	Percentage.objects.bulk_create(insertList)
	logging.debug("end db insert")

def percentFileName(period, sample):
	return pc_definitions.percentStoreDir + "/" + period + "_" + str(sample)

def insertPercentMapToDir(percentMap):

	if not os.path.exists(pc_definitions.percentStoreDir):
		os.mkdir(pc_definitions.percentStoreDir)

	lock = FileLock(pc_definitions.lockfile)
	with lock:
		Percentage.objects.all().delete()

		for key, value in percentMap.iteritems():
			fields = key.split("/")
			period = fields[0]
			sample = int(fields[1])

			with open(percentFileName(period, sample), "w") as fh:
				json = jsonpickle.encode(value, unpicklable=False)
				fh.write(json)

def getPercentSetFromDir(period, sample):

	lock = FileLock(pc_definitions.lockfile)
	with lock:
		with open(percentFileName(period, sample), "r") as fh:
			json = fh.read()

	percentSet = jsonpickle.decode(json)

	return percentSet

def getPercentSetFromDb(period, sample):

	percentList = Percentage.objects.filter(period=period, sample=sample)

	percentSet = []
	for c in cf_definitions.currencies:
		percentForCurrency = {"currency": c, "percentages" : []}
		percentObjects = Percentage.objects.filter(period=period, sample=sample, currency=c).order_by('number')
		logging.debug(percentObjects)
		for po in percentObjects:
			percentForCurrency["percentages"].append(po.percentage)
		percentSet.append(percentForCurrency)
		
	return percentSet
