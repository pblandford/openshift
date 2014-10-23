from __future__ import print_function
import jsonpickle
import httplib
import os
import filescan
from CurrencyFeed import cf_definitions
from . import fs_definitions
from . import percentmap
from datetime import datetime
import shutil


def scantask():
	print("starting scantask")

	percentMap = percentmap.createPercentMap()
	
	unionMap = diffMaps(percentMap)

	fullJson = jsonpickle.encode(percentMap, unpicklable=False)
	with open(fs_definitions.mapFile, "w") as fh:
		fh.write(fullJson)

	unionJson = jsonpickle.encode(unionMap, unpicklable=False)
	print(unionJson)

	headers = { "Content-type" : "application/json" }

	conn = httplib.HTTPConnection(fs_definitions.uploadServer)
	conn.request("POST", fs_definitions.uploadPath, unionJson, headers)
	response = conn.getresponse()

	if (response.status != 200):
		raise Exception("Status code: " + str(response.status))

	msg = response.read()
	if (msg != "OK"):
		raiseException("Unexpected response: " + msg)


def diffMaps(percentMap):
	
	try:
		with open(fs_definitions.mapFile, "r") as oldMapFh:
			oldMapJson = oldMapFh.read()
			oldMap = jsonpickle.decode(oldMapJson)
	except Exception:
		return percentMap
	
	unionMap = {}
	for key, value in oldMap.iteritems():
		if percentMap[key] != value:
			unionMap[key] = value

	return unionMap
