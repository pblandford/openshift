from django.test import TestCase
import unittest
from . import store
from .models import Percentage
from filescan import percentmap

# Create your tests here.

class PercentagesTestCase(TestCase):
	percentMap = None

	def setUp(self):
		self.percentMap = percentmap.createPercentMap()

	@unittest.skip
	def test_insertToDb(self):
		store.insertPercentMap(self.percentMap)

		percentages = Percentage.objects.all()

		print percentages

	def test_insertToDir(self):
		store.insertPercentMapToDir(self.percentMap)

	def test_getPercentSetFromDir(self):
		store.insertPercentMapToDir(self.percentMap)
		percentSet = store.getPercentSetFromDir("M1", 30)
		print(percentSet)
