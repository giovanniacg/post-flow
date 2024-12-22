from django.db import models
from simple_history.models import HistoricalRecords

class Status(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name
