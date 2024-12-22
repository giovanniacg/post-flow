from rest_framework.viewsets import ModelViewSet
from .permissions import IsAdminOrReadOnly
from .models import Status
from .serializers import StatusSerializer


class StatusViewSet(ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    permission_classes = [IsAdminOrReadOnly]
