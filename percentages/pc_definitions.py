import os

useDatabase = False
from CurrencyFeed import settings
if settings.LOCAL == True:
	from filescan import fs_definitions
	percentStoreDir = "./.mapcache"
else:
	percentStoreDir = os.environ['OPENSHIFT_DATA_DIR'] + "/percentages"
lockfile = percentStoreDir + "/.lock"
