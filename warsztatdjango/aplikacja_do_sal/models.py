from django.db import models
from django.utils import timezone

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector_available = models.BooleanField(default=False)

class RoomReservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ('room_id', 'date')