import jsonpickle

from CurrencyFeed import cf_definitions
from . import filescan
from . import fs_definitions

def periodSampleKey(period, sample):
	return period + "/" + str(sample)

# returns map of string(period+sample)=percentSet
def createPercentMap():
	percentMap = {}

	for period in cf_definitions.periods:
		for sample in cf_definitions.samples:
			percentSets = filescan.fileScan(period, sample)
			percentMap[periodSampleKey(period, sample)] = percentSets

	return percentMap

# returns tuple (high, low)
def getPair(percentMap, period, sample, threshold):
	
	percentSets = percentMap[periodSampleKey(period, sample)]

	# tuples of (currency, value)
	high = None
	low = None

	for percentSet in percentSets:
		last = percentSet['percentages'][len(percentSet['percentages'])-1]

		if last > threshold:
			if high == None or last > high[1]:
				high = (percentSet['currency'], last)

		if last < (0-threshold):
			if low == None or last < low[1]:
				low = (percentSet['currency'], last)

	highStr = "-" if high == None else high[0]
	lowStr = "-" if low == None else low[0]
	return highStr + "/" + lowStr

