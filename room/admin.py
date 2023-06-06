from django.contrib import admin
from .models import Room, Resident, RoomBooking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "type")


@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ("room", "resident", "start", "end", "booked")
