#!/usr/bin/python

import os

periods = {
	'M1': 60,
	'M5': 60 * 5,
	'M15': 60 * 15,
	'M30': 60 * 30,
	'H1': 60 * 60,
	'H4': 60 * 60 * 4,
	'D1': 60 * 60 * 24,
	'W1': 60 * 60 * 24 * 7,
	'MN1': 60 * 60 * 24 * 28
}

def checkDue(filename, modTimes):
	periodName = os.path.basename(filename).split('_')[1]

	periodLen = periods[periodName]
	modTime = os.path.getatime(filename)

	if filename not in modTimes:
		modTimes[filename] = modTime
		return True

	if modTimes[filename] != modTime:
		modTimes[filename] = modTime
		return True

	return False

