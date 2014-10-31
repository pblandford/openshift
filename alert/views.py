from django.http import HttpResponse
from django.core import exceptions

import jsonpickle

from .models import Alert, Client
from CurrencyFeed import settings

import logging
import cm_definitions

def add(request, period, sample, threshold):

	if not 'regid' in request.POST:
		return HttpResponse(status=400)
	regid = request.POST['regid']

	try:
		client = Client.objects.get(regid=regid)
	except Client.DoesNotExist:
		return HttpResponse("Unknown", content_type="text/plain")

	alert = Alert(client = client, period = period, sample = int(sample), 
		threshold = float(threshold))
	alert.save()

	return HttpResponse("OK", content_type="text/plain")

def delete(request, period, sample, threshold):

	if not 'regid' in request.POST:
		return HttpResponse(status=400)
	regid = request.POST['regid']

	try:
		client = Client.objects.get(regid=regid)
	except Client.DoesNotExist:
		return HttpResponse("Unknown", content_type="text/plain")

	alerts = Alert.objects.filter(client=client, period=period, sample=int(sample), threshold=float(threshold))
	for a in alerts:
		a.delete()

	return HttpResponse("OK", content_type="text/plain")

def checkin(request):

	oldRegid = None

	if not 'regid' in request.POST:
		return HttpResponse(status=400)

	if not 'alerts' in request.POST:
		return HttpResponse(status=400)

	regid = request.POST['regid']
	if 'oldregid' in request.POST:
		oldRegid = request.POST['oldregid']

	logging.debug("Check in for " + regid)

	try:
		client = Client.objects.get(regid=regid)

		if oldRegid != None:
			logging.info("Client registering new ID - was: " + oldRegid + " now: " + regid)
			updateregid(oldRegid, regid)
			client.needsupdate = False
			client.save()

		if client.needsupdate == True:
			logging.info("Client with expired regid: " + regid)
			return HttpResponse("expired")
	except Client.DoesNotExist:
		logging.info("Login from new client " + regid)
		client = Client(regid=regid)
		client.save()

	alerts = request.POST['alerts']
	syncAlerts(alerts, client)

	try:
		with open(cm_definitions.adnetFile) as f:
			adnet = f.read().strip()
	except Exception:
		adnet = settings.AD_NETWORK

	responsehash = {}
	responsehash['AdNet'] = adnet

	responseJSON = jsonpickle.encode(responsehash, unpicklable=False)

	return HttpResponse(responseJSON, content_type="text/json")

def updateregid(oldregid, newregid):

	try:
		client = Client.objects.get(regid=oldregid)
		client.regid=newregid
		client.save()
	except Client.DoesNotExist:
		logging.error("Update regid for unknown client with old regid " + oldregid)
		client = Client(regid=newregid)
		client.save()

	return HttpResponse("OK", content_type="text/plain")

def syncAlerts(alertString, client):
	# ensure we have the alerts the client thinks we have
	print(alertString)
	alerts = jsonpickle.decode(alertString)
	for alert in alerts:
		try:
			dbAlert = Alert.objects.get(sample=alert['sample'], period=alert['period'], \
				threshold=alert['threshold'], client=client)
		except Alert.DoesNotExist:
			logging.info("adding unknown alert for " + client.regid)
			dbAlert = Alert(sample=alert['sample'], period=alert['period'], \
			        threshold=alert['threshold'], client=client)

	dbAlerts = Alert.objects.filter(client=client)
	for dbAlert in dbAlerts:
		found = False
		for alert in alerts:
			if alert['sample'] == dbAlert.sample and alert['period'] == dbAlert.period \
				and alert['threshold'] == dbAlert.threshold:
					found = True
					break

		if not found:
			logging.info("deleting unknown alert for " + client.regid)
			dbAlert.delete()
		
