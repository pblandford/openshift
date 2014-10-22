
uploadServer = "192.168.0.101:8000"
uploadPath = "/percentages/upload"
uploadKey  = "oiroiwejroiej"

class PercentSet(object):
	currency = ""
	percentages = []

	def __init__(self, currency):
		self.currency = currency
		self.percentages = []

	def __str__(self):
		return self.currency + " " + str(self.percentages)
