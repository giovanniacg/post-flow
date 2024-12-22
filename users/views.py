from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserDetailAddressSerializer
from .permissions import IsOwnerOrPostOnly


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrPostOnly]

    @extend_schema(
        responses=UserDetailAddressSerializer,
        description="Retrieve all addresses of a user.",
        summary="User addresses"
    )
    @action(detail=True, methods=['get'], permission_classes=[IsOwnerOrPostOnly])
    def addresses(self, request, pk=None):
        user = self.get_object()
        addresses = user.useraddress_set.all()
        serializer = UserDetailAddressSerializer(addresses, many=True)
        return Response(serializer.data)
