from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from address.serializers import AddressSerializer
from status.serializers import StatusSerializer
from .models import Post, PostStatus
from address.models import Address
from status.models import Status


class PostSerializer(ModelSerializer):
    address = AddressSerializer(read_only=True)
    current_status = StatusSerializer(read_only=True)
    address_id = PrimaryKeyRelatedField(queryset=Address.objects.all(), source='address', write_only=True)
    current_status_id = PrimaryKeyRelatedField(queryset=Status.objects.all(), source='current_status', write_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "address",
            "address_id",
            "current_status",
            "current_status_id",
            "created_at",
            "updated_at",
        ]


class PostStatusSerializer(ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = PostStatus
        fields = ['status', 'updated_at', 'created_at']


class PostDetailSerializer(ModelSerializer):
    statuses = PostStatusSerializer(source='poststatus_set', many=True)
    address = AddressSerializer()
    current_status = StatusSerializer()

    class Meta:
        model = Post
        fields = ['user', 'current_status', 'address', 'created_at', 'updated_at', 'statuses']
