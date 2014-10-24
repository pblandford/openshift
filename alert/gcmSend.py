import jsonpickle
import httplib
import logging

import cm_definitions

class NotRegisteredException(Exception):
	pass

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

	raise NotRegisteredException()
	if (responseObject['success'] != 1):
		for result in responseObject['results']:
			logging.error(result)
			if 'error' in result and result['error'] == 'NotRegistered':
				raise NotRegisteredException()

		raise Exception("Unexpected response: " + str(responseObject['failure']) + " messages failed")
	
