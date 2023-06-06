from django.urls import path
from .views import RoomListApiView, RoomDetailApiView, RoomBookingListApiView, RoomBookCreateApiView

urlpatterns = [
    path("rooms/", RoomListApiView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailApiView.as_view(), name="room-detail"),
    path("rooms/<int:pk>/availability/",  RoomBookingListApiView.as_view(), name="room-booking-list"),
    path("rooms/<int:pk>/book/", RoomBookCreateApiView.as_view(), name="create-room=book")
]