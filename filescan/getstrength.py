#!/usr/bin/python
from __future__ import print_function


def getPercentages(quotes, isBase):
	startQuote = quotes[len(quotes)-1]
	percentages = [] * len(quotes)
	percentages.append(0.0)

	#for quote in quotes[len(quotes)-2:-1:-1]:
	for i in range(len(quotes)-2, -1, -1):
		quote = quotes[i]
		if isBase:
			percentage = ((quote-startQuote)/startQuote) * 100
		else:
			percentage = ((startQuote-quote)/startQuote) * 100
		percentages.append(percentage)

	return percentages

# get a list of percentage lists for each base or counter currency
def addPercentages(currency, period, sample, quoteMap):
	quoteSets = quoteMap[currency]

	percentagesList = []

	for quoteSet in quoteSets:
		if quoteSet.period != period:
			continue

		percentagesList.append(getPercentages(quoteSet.quotes[0:sample], quoteSet.base == currency))

	return percentagesList

# Given a single currency and period, return a list of combined percentage movements relative
# to all other currencies
def getStrength(currency, period, sample, quoteMap):

	# get list of lists of percentages, one for each other currency
	percentagesList = addPercentages(currency, period, sample, quoteMap)


	combinedPercentages = [0] * sample
	# cycle list of lists, adding the values of each list to a single combined list
	for pl in percentagesList:
		i=0
		for pc in pl:
			combinedPercentages[i] += pc
			i+=1

	for i in range(len(combinedPercentages)):
		combinedPercentages[i] = round(combinedPercentages[i],4)

	return combinedPercentages

