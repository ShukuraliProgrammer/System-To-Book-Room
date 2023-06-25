from django.test import TestCase
from django.urls import reverse
from room.models import Room, RoomBooking, Resident
from datetime import datetime, timedelta


# Create your tests here.

class TestRoomViews(TestCase):
    def create_room(self):
        room = Room.objects.create(
            name="Test", type=Room.RoomType.FOCUS, capacity=2
        )
        return room

    def create_room_booking(self):
        resident = Resident.objects.create(name="Test")
        room_booking = RoomBooking.objects.create(
            resident=resident, room=self.create_room(), start=datetime.now(), end=datetime.now() + timedelta(hours=3)
        )
        return room_booking

    def test_room_list_view(self):
        url = reverse("room-list")
        self.create_room()

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(resp.json()["results"][0].keys()), sorted(["id", "name", "type", "capacity"]))
        self.assertEqual(resp.json()["count"], 1)

    def test_room_detail_view(self):
        room = self.create_room()
        url = reverse("room-detail", kwargs={"pk": room.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(sorted(resp.json().keys()), sorted(["id", "name", "type", "capacity"]))

    def test_room_booking_list_view(self):
        room = self.create_room()
        url = reverse("room-booking-list", kwargs={"pk": room.id})
        self.create_room_booking()
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
