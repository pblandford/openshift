import os

periods = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"]
samples = [10,20,30,40,50,60,70,80,90,100]
currencies = ["USD", "EUR", "NZD", "AUD", "GBP", "CAD", "CHF", "JPY" ]

from CurrencyFeed import settings
if settings.LOCAL == True:
	ramdir = "/opt/MT4/ramdisk-test"
else:
	ramdir = os.environ['OPENSHIFT_DATA_DIR'] + "/ramdisk"
percentdir = ramdir + "/percentages"


