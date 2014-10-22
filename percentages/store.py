from __future__ import print_function
from .models import Percentage
from . import pc_definitions
import os.path
import jsonpickle
from lockfile import FileLock

def insertPercentMap(percentMap):

	print("start")


	Percentage.objects.all().delete()

	for key, value in percentMap.iteritems():
		fields = key.split("/")
		period = fields[0]
		sample = int(fields[1])

		percentSetList = value
		for percentSet in percentSetList:
			i=0
			currency = percentSet['currency']
			for pcVal in percentSet['percentages']:
#				print(currency, period, sample, pcVal, i)

				percentage = Percentage(currency=currency, percentage=float(pcVal), sample=sample, \
					number=i, period=period)
				percentage.save()

				i += 1
	print("end")

def percentFileName(period, sample):
	return pc_definitions.percentStoreDir + "/" + period + "_" + str(sample)

def insertPercentMapToDir(percentMap):

	print("start")

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
