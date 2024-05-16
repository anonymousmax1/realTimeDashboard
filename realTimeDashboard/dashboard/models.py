from django.db import models

# Create your models here.
class Data(models.Model):
    label = models.CharField(max_length=50)
    value = models.FloatField()