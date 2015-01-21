import os

gcmHost = "android.googleapis.com"
#gcmHost = "https://googleapis.l.google.com"
gcmPath = "/gcm/send"
gcmKey = "AIzaSyBHKZHknfNzOxsr51VW7jqKMY9kMUpE2mA"

from CurrencyFeed import settings
if settings.LOCAL == False:
	adnetFile = os.environ['OPENSHIFT_DATA_DIR'] + "/ADNET"
else:
	adnetFile = "./adnet"
