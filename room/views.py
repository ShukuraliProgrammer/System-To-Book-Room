from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RoomListSerializer
from .models import Room
from .paginations import CustomPagination


class RoomListApiView(ListAPIView):
    serializer_class = RoomListSerializer
    queryset = Room.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ("type", )
    search_fields=["name", "id"]

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
            return Response({"error": "topilmadi"})

