import httplib
import logging
from datetime import datetime

from .models import Alert, Client
from . import gcmSend
from filescan import percentmap

def checkAlerts(percentMap):
	alerts = Alert.objects.all()

	for alert in alerts:
		pair = percentmap.getPair(percentMap, alert.period, alert.sample, alert.threshold)
		if pair == None:
			continue
		if pair != alert.lastpair:
			alert.lastpair = pair
			alert.lastalert = datetime.now()
			alert.save()

			try:
				gcmSend.sendAlert(alert.client.regid, alert.period, alert.sample, alert.threshold, pair)
			except gcmSend.NotRegisteredException:
				logging.error("Received NotRegisteredException, removing client " + alert.client.regid)
				Alert.objects.filter(client=client).delete()
				Client.objects.get(id=alert.client_id).delete()

			except Exception as e:
				logging.error("could not send alert for " + str(alert.client), exc_info=e)
