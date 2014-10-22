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
	if not os.path.exists(fs_definitions.percentDir):
		os.mkdir(fs_definitions.percentDir)	

	percentMap = percentmap.createPercentMap()

	json = jsonpickle.encode(percentMap, unpicklable=False)
	headers = { "Content-type" : "application/json" }

	conn = httplib.HTTPConnection(fs_definitions.uploadServer)
	conn.request("POST", fs_definitions.uploadPath, json, headers)
	response = conn.getresponse()

	if (response.status != 200):
		raise Exception("Status code: " + str(response.status))

	msg = response.read()
	if (msg != "OK"):
		raiseException("Unexpected response: " + msg)

