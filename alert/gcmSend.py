import jsonpickle
import httplib

import cm_definitions


def sendAlert(regid, period, sample, threshold, pair):

	headers = { "Content-type" : "application/json", "Authorization" : "key=" + cm_definitions.gcmKey }

	body = { "registration_ids" : [ regid ], "data" : { "period" : period, "sample" : sample, \
		"threshold" : threshold, "pair" : pair } }

	json = jsonpickle.encode(body, unpicklable=False)

	print json

	conn = httplib.HTTPSConnection(cm_definitions.gcmHost)
	conn.request("POST", cm_definitions.gcmPath, json, headers)
	response = conn.getresponse()

	if (response.status != 200):
		raise Exception("Status Code: " + str(response.status))

	json = response.read()
	responseObject = jsonpickle.decode(json)

	if (responseObject['success'] != 1):
		raise Exception("Unexpected response: " + msg)
	
