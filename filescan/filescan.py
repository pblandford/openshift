from __future__ import print_function
import os
import string
import time
import logging
import sys
from datetime import datetime

from getstrength import getStrength
import fs_definitions
from CurrencyFeed import cf_definitions

logging.basicConfig(level=logging.DEBUG)

# Class to contain a full list of quotes for a single currency pair and period
class QuoteSet:
	base = ""
	counter = ""
	period = ""
	quotes = []

	def __init__(self, base, counter, period):
		self.base = base
		self.counter = counter
		self.period = period
		self.quotes = []

	def __str__(self):
		return self.base + "/" + self.counter + " " + self.period + " " + str(self.quotes)

def fileScan(period, sample):
	quoteMap = doScan(period, sample)
	return doPercentages(period, sample, quoteMap)

def getQuote(line):
	line = line.replace("\n", "").replace("\r", "")
	price, time = line.split(";")

	return float(price)


def doScan(periodInput, sampleInput):
	quoteMap = {}
	for c in cf_definitions.currencies:
		quoteMap[c] = []

	for pairDir in os.listdir(fs_definitions.ramdisk):
		base = pairDir[:3]
		counter = pairDir[3:]

		fullPairDir = fs_definitions.ramdisk + "/" + pairDir
		if not os.path.isdir(fullPairDir):
			continue

		for periodFile in os.listdir(fullPairDir):
			period = periodFile.replace("PERIOD_", "")
			if period != periodInput:
				continue

			fullPeriodFile = fullPairDir + "/" + periodFile
			with open(fullPeriodFile) as f:
				lines = f.readlines()

				quoteSet = QuoteSet(base, counter, period)
				for line in lines:
					try:
						quoteSet.quotes.append(getQuote(line))
					except Exception as e:
						print(line)
						print(fullPeriodFile)
						print(fullPairDir)
						raise e

				quoteMap[base].append(quoteSet)
				quoteMap[counter].append(quoteSet)

	return quoteMap

def doPercentages(period, sample, quoteMap):
	percentSets = []

	for c in cf_definitions.currencies:
		percentSet = {}
		percentSet['currency'] = c
		percentSet['percentages'] = getStrength(c, period, sample, quoteMap)
		percentSets.append(percentSet)

	return percentSets
			
