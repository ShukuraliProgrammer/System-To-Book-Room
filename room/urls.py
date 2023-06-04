from django.urls import path
from .views import RoomListApiView, RoomDetailApiView

urlpatterns = [
    path("rooms/", RoomListApiView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailApiView.as_view(), name="room-detail"),
]