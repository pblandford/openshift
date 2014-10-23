from django.shortcuts import render
from django.http import HttpResponse

import logging
import jsonpickle
from filescan import filescan
from . import store

from CurrencyFeed.models import Currency
from alert import alert

# Create your views here.
def receive(request, period, sample):

	percentSets = store.getPercentSetFromDir(period, int(sample))

	json = jsonpickle.encode(percentSets)
	return HttpResponse(json, content_type="application/json")

def upload(request):

	logging.debug("upload: " + str(len(request.body)) + " bytes")
	percentMap = jsonpickle.decode(request.body)

	alert.checkAlerts(percentMap)

	store.insertPercentMapToDir(percentMap)

	return HttpResponse("OK", content_type="text/plain")


