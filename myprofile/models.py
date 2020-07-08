from django.db import models
from django.urls import reverse
from django.utils import timezone

class Event(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    start = models.CharField(max_length=45,help_text="Start time format: YYYY-MM-DDThh:mi:se+05:30 ex:2020-07-18T22:25:11+05:30")
    end = models.CharField(max_length=45,help_text="End time format: YYYY-MM-DDThh:mi:se+05:30 ex:2020-07-18T22:25:11+05:30")

    def get_absolute_url(self):
        return reverse('event-update', kwargs={'pk': self.pk})

class CreatedEvent(models.Model):
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
    htmlLink = models.CharField(max_length=400, null=True, blank=True)
    hangoutLink = models.CharField(max_length=400, null=True, blank=True)

class Attendee(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email
