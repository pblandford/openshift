from django.http import HttpResponse
from django.core import exceptions

from jsonpickle import encode

from .models import Alert, Client

import logging

def add(request, period, sample, threshold):

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

	return HttpResponse("OK", content_type="text/plain")

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
