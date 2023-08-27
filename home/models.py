import os
from django.db import models

from django.core.exceptions import ValidationError

# Create your models here.
class NewData(models.Model):
    label = models.CharField(max_length=50, null=False, unique=True)
    density = models.FloatField(null=False)
    data = models.FileField(null=False)

    def __str__(self):
        return self.label
    
class Unit(models.Model):
    unit = models.CharField(max_length=30)

    def __str__(self):
        return self.unit

class PipeData(models.Model):
    diameter = models.FloatField(null=False)
    length = models.FloatField(null=False)
    fluid_data = models.ForeignKey(NewData, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.fluid_data.label
