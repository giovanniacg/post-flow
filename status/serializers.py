from rest_framework.serializers import ModelSerializer
from .models import Status


class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"