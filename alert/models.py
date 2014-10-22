from django.db import models

# Create your models here.

class Alert(models.Model):
    regid = models.CharField(max_length=4096)
    period = models.TextField() # This field type is a guess.
    sample = models.IntegerField()
    threshold = models.FloatField()
    lastpair = models.CharField(max_length=7, null=True)
    lastalert = models.DateField(null=True)
    class Meta:
        managed = True
        db_table = 'alert'

    def __str__(self):
      return self.regid + ", " + self.period + ", " + str(self.sample) + ", " \
        + str(self.threshold) + ", " + str(self.lastpair)  + ", " + str(self.lastalert)

