from django.db import models
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


