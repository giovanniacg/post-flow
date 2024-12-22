from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Customize the response to indicate whether a new address was created or the existing one was updated.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        new_address = serializer.save(user=request.user)

        if new_address != instance:
            message = "A new address was created because the current one is linked to posts."
            status_code = status.HTTP_201_CREATED
        else:
            message = "The address was updated successfully."
            status_code = status.HTTP_200_OK

        return Response(
            {"message": message, "address": AddressSerializer(new_address).data},
            status=status_code,
        )