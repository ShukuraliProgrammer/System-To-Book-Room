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

    class Meta:
        model = RoomBooking
        fields = ("resident", "start", "end")

    # def create(self, validated_data):
    #     print(validated_data)
    #     return validated_data