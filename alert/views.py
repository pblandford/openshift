from django.http import HttpResponse

from jsonpickle import encode

from .models import Alert

def add(request, period, sample, threshold):

	regid = request.POST['regid']

	alert = Alert(regid = regid, period = period, sample = int(sample), 
		threshold = float(threshold))
	alert.save()

	return HttpResponse("OK", content_type="text/plain")

def delete(request, period, sample, threshold):

	regid = request.POST['regid']

	alerts = Alert.objects.filter(regid=regid, period=period, sample=int(sample), threshold=float(threshold))
	for a in alerts:
		a.delete()

	return HttpResponse("OK", content_type="text/plain")
