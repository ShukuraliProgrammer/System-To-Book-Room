from django.db.models import Q
from rest_framework import serializers
from .models import Room, RoomBooking, Resident


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
    start = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    end = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    class Meta:
        model = RoomBooking
        fields = ("resident", "start", "end")

    def create(self, validated_data):
        room = 1
        book = RoomBooking.objects.filter(
            Q(room_id=room),
            Q(start__lt=validated_data["end"], end__gt=validated_data["start"]) |
            Q(start__gte=validated_data["start"], end__lte=validated_data["end"]) |
            Q(start__lte=validated_data["start"], end__gte=validated_data["end"])
        ).exists()
        if book:
            raise serializers.ValidationError("This time is not suitable")
        return validated_data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["start"] = instance.start.strftime('%d-%m-%Y %H:%M:%S')
        data["end"] = instance.end.strftime('%d-%m-%Y %H:%M:%S')
        return data