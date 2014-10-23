import os

useDatabase = True
from CurrencyFeed import settings
if settings.LOCAL == True:
	from filescan import fs_definitions
	percentStoreDir = "./percentages"
else:
	percentStoreDir = os.environ['OPENSHIFT_DATA_DIR'] + "/percentages"
lockfile = percentStoreDir + "/.lock"
