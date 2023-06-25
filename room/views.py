from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework import status
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, time

from .serializers import RoomListSerializer, RoomBookingListSerializer, RoomBookingCreateSerializer
from .models import Room, RoomBooking
from .paginations import CustomPagination


class RoomListApiView(ListAPIView):
    serializer_class = RoomListSerializer
    queryset = Room.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ("type",)
    search_fields = ["name", "id"]

    def get(self, request, *args, **kwargs):
        search_param = self.request.query_params.get("search")
        type_param = self.request.query_params.get("type")

        if search_param:
            queryset = self.get_queryset().filter(name__contains=search_param)
        else:
            queryset = self.get_queryset()

        if type_param:
            queryset = queryset.filter(type=type_param)

        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializers = self.get_serializer(paginated_queryset, many=True)
        response = paginator.paginated_response(data=serializers.data)
        return Response(response)


class RoomDetailApiView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer

    def get(self, *args, **kwargs):
        try:
            obj = self.get_object()
            serializers = self.get_serializer(obj)
            return Response(serializers.data)
        except Exception as e:
            print(e)
            return Response({"error": "topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class RoomBookingListApiView(RetrieveAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingListSerializer

    def get(self, request, *args, **kwargs):
        room_id = self.kwargs.get('pk')
        desired_date_str = request.GET.get('date')
        if not desired_date_str:
            desired_date_str = datetime.today().date().strftime('%d-%m-%Y')

        desired_date = datetime.strptime(str(desired_date_str), '%d-%m-%Y').date()

        start_of_day = datetime.combine(desired_date, time.min)
        end_of_day = datetime.combine(desired_date, time.max)

        overlapping_bookings = RoomBooking.objects.filter(
            room_id=room_id,
            start__lt=end_of_day,
            end__gt=start_of_day
        )

        available_slots = []
        previous_booking_end = start_of_day

        for booking in overlapping_bookings:
            if previous_booking_end.strftime('%d-%m-%Y %H:%M:%S') < booking.start.strftime('%d-%m-%Y %H:%M:%S'):
                available_slots.append({
                    'start': previous_booking_end.strftime('%d-%m-%Y %H:%M:%S'),
                    'end': booking.start.strftime('%d-%m-%Y %H:%M:%S')
                })

            previous_booking_end = booking.end

        if previous_booking_end.strftime('%d-%m-%Y %H:%M:%S') < end_of_day.strftime('%d-%m-%Y %H:%M:%S'):
            available_slots.append({
                'start': previous_booking_end.strftime('%d-%m-%Y %H:%M:%S'),
                'end': end_of_day.strftime('%d-%m-%Y %H:%M:%S')
            })

        return Response(available_slots, status=status.HTTP_200_OK)


class RoomBookCreateApiView(CreateAPIView):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data={"message": "xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["room_id"] = self.kwargs.get("pk")
        return context
