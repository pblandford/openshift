from percentages.models import Percentage
from CurrencyFeed import cf_definitions
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		self.initPercentageTable()

	def initPercentageTable(self):

		Percentage.objects.all().delete()

		insertList = []

		for c in cf_definitions.currencies:
			for p in cf_definitions.periods:
				for s in cf_definitions.samples:
					for i in range(s):
						percentage = Percentage(currency=c, period=p, sample=s, number=i, percentage=0.0)
						insertList.append(percentage)

		Percentage.objects.bulk_create(insertList)

