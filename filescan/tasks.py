from __future__ import print_function
from celery import task
import jsonpickle
import httplib
import os
import filescan
from CurrencyFeed import cf_definitions
from . import fs_definitions
from . import percentmap
from datetime import datetime


@task
def scantask():
	print("starting scantask")
	if not os.path.exists(cf_definitions.percentdir):
		os.mkdir(cf_definitions.percentdir)	

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

