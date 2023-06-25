from django.db.models import Q
from django.db import IntegrityError
from rest_framework import serializers
from .models import Room, RoomBooking, Resident
from django.db import transaction
from rest_framework import status
from room.exceptions import InvalidRoomBookException


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "type", "capacity")


class RoomBookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = ("start", "end")


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ("name",)


class RoomBookingCreateSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer(write_only=True)
    start = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'])
    end = serializers.DateTimeField(input_formats=['%d-%m-%Y %H:%M:%S'])

    class Meta:
        model = RoomBooking
        fields = ("resident", "start", "end")

    def create(self, validated_data):
        # room = 1
        # book = RoomBooking.objects.filter(
        #     Q(room_id=room),
        #     Q(start__lt=validated_data["end"], end__gt=validated_data["start"]) |
        #     Q(start__gte=validated_data["start"], end__lte=validated_data["end"]) |
        #     Q(start__lte=validated_data["start"], end__gte=validated_data["end"])
        # ).exists()
        # if book:
        #     raise serializers.ValidationError("This time is not suitable")
        #

        with transaction.atomic():
            try:
                queryset = RoomBooking.objects.filter(
                    Q(start__lt=validated_data.get("end"), end__gt=validated_data.get("start")) |
                    Q(start__gte=validated_data.get("start"), end__lte=validated_data.get("end")) |
                    Q(start__lte=validated_data.get("start"), end__gte=validated_data.get("end"))
                ).exists()
                res = Resident.objects.create(**validated_data.pop("resident"))
                room = Room.objects.filter(id=self.context['room_id']).first()

                if queryset:
                    raise InvalidRoomBookException("uzr, siz tanlagan vaqtda xona band")

                room_booking = RoomBooking.objects.create(
                    resident=res, room=room, start=validated_data["start"], end=validated_data["end"]
                )
            except IntegrityError as e:
                if 'start_before_end' in str(e):
                    raise serializers.ValidationError("Start before End")
                elif 'no_overlapping_bookings' in str(e):
                    raise serializers.ValidationError("This room is booked")
                else:
                    raise e
            return room_booking
