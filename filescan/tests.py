from django.test import TestCase
from . import percentmap
from . import tasks
from jsonpickle import encode
from alert.models import Alert

# Create your tests here.

regid = "APA91bFxrh_A2xh2Fooed5T2PQkVb8CNCj0FJgv-SE5ARgW7CbfjMFAOxyfVnjdeE4Y21Qt0R4DXS18-O_qHLx_336ppoluwLWCjqqeeTEjQZF_nkaajgLGHM5TIpQyx7GvAhh2b-KoKmWEkTB5q_HlFWwBkwnLOU2dWxCfUY-0CwFPdfvqMiByuJpkz-nnNVH9NK8bvTPta"

class FileScanTestCase(TestCase):
	percentMap = None

	def setUp(self):
		self.percentMap = percentmap.createPercentMap()
		Alert.objects.create(regid=regid, period="M1", sample=60, threshold=0.5)
		Alert.objects.create(regid=regid, period="M15", sample=30, threshold=1.0)


	def test_scantask(self):
		tasks.scantask()

	def test_getPair(self):
		pair = percentmap.getPair(self.percentMap, "H1", 10, 0.5)
		print pair

