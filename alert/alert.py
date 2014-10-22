import httplib
from datetime import datetime

from .models import Alert
from . import gcmSend
from filescan import percentmap

def checkAlerts(percentMap):
	alerts = Alert.objects.all()
	print(alerts)

	for alert in alerts:
		pair = percentmap.getPair(percentMap, alert.period, alert.sample, alert.threshold)
		if pair != alert.lastpair:
			alert.lastpair = pair
			alert.lastalert = datetime.now()
			alert.save()

			gcmSend.sendAlert(alert.regid, alert.period, alert.sample, alert.threshold, pair)