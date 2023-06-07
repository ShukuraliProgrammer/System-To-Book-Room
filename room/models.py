from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Room(TimeStampModel):
    class RoomType(models.TextChoices):
        FOCUS = _("focus")
        TEAM = _("team")
        CONFERENCE = _("conference")

    name = models.CharField(max_length=120, verbose_name=_("Name"))
    type = models.CharField(max_length=60, choices=RoomType.choices, default=RoomType.FOCUS, verbose_name=_("Type"))
    capacity = models.IntegerField(verbose_name=_("Capacity"))

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return self.name


class Resident(models.Model):
    name = models.CharField(max_length=120, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class RoomBooking(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name="room_bookings", null=True,
                                 blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_bookings")
    start = models.DateTimeField()
    end = models.DateTimeField()
    booked = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Room Book")
        verbose_name_plural = _("Room Books")

        constraints = [
            models.CheckConstraint(
                check=~Q(start__gte=models.F('end')),
                name='start_before_end'
            ),
            models.CheckConstraint(
                check=~Q(
                    RoomBooking.objects.filter(
                        Q(start__lt=models.F('end'), end__gt=models.F('start')) |
                        Q(start__gte=models.F('start'), end__lte=models.F('end')) |
                        Q(start__lte=models.F('start'), end__gte=models.F('end'))
                    ).exists()
                ),
                name='no_overlapping_bookings'
            )
        ]

    def __str__(self):
        return self.room.name
