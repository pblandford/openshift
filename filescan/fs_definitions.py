
USE_LOCAL=False
if USE_LOCAL:
	uploadServer = "192.168.0.101:8000"
else:
	uploadServer = "currencyfeed-philblandford.rhcloud.com"
uploadPath = "/percentages/upload"
uploadKey  = "oiroiwejroiej"

from CurrencyFeed import cf_definitions
mapFile = cf_definitions.ramdir + "/percentages.json"

class PercentSet(object):
	currency = ""
	percentages = []

	def __init__(self, currency):
		self.currency = currency
		self.percentages = []

	def __str__(self):
		return self.currency + " " + str(self.percentages)
