from rest_framework import serializers

from .models import User
from .exceptions import PasswordsNotMatch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeat_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('repeat_password'):
            raise PasswordsNotMatch()

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user = User.objects.create_user(**validated_data)
        return user
