from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from address.serializers import AddressSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailAddressSerializer(ModelSerializer):
    addresses = AddressSerializer(source='address_set', many=True)

    class Meta:
        model = User
        fields = ['addresses']