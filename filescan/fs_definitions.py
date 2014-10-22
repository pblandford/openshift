
uploadServer = "currencyfeed-philblandford.rhcloud.com"
uploadPath = "/percentages/upload"
uploadKey  = "oiroiwejroiej"

percentDir = "/opt/MT4/ramdisk/percentages"
percentDirOld = "/opt/MT4/ramdisk/percentages.old"

class PercentSet(object):
	currency = ""
	percentages = []

	def __init__(self, currency):
		self.currency = currency
		self.percentages = []

	def __str__(self):
		return self.currency + " " + str(self.percentages)
