from django.db import models
from datetime import datetime

class Event(models.Model):
    event_type = models.CharField(max_length=80, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    note = models.CharField(max_length=800)
    baby = models.ForeignKey(
        'babies.Baby',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Event: {}'.format(self.event_type)
