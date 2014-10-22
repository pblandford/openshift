from django.db import models

# Create your models here.
class Percentage(models.Model):
    currency = models.CharField(max_length=3)
    percentage = models.FloatField(blank=True, null=True)
    sample = models.IntegerField()
    number = models.IntegerField()
    period = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        managed = True
        db_table = 'percentage'

