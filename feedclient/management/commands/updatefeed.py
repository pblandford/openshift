from django.core.management.base import BaseCommand, CommandError

from feedclient import feedclient
from filescan import percentmap
from percentages import store, pc_definitions
from alert import alert

class Command(BaseCommand):

    def handle(self, *args, **options):
			feedclient.update()
			percentMap = percentmap.createPercentMap()

			alert.checkAlerts(percentMap)

			if (pc_definitions.useDatabase == True):
				store.insertPercentMapToDb(percentMap)
			else:
				store.insertPercentMapToDir(percentMap)
