from django.db import models

class MeasurementUnit(models.Model):
    name = models.CharField(max_length=55, unique=True)
    volume_in_ml = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
