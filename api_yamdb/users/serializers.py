from rest_framework import serializers

import re

from .models import CustomUser


class ConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Нельзя использовать "me"')
        pattern = re.compile(r'^[\w.@+-]+\Z')
        if not pattern.match(value):
            raise serializers.ValidationError('Ошибка паттерна')
        return value


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'bio', 'email',
                  'role']
        lookup_field = 'username'


class CustomUserPATCHSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', ]
        lookup_field = 'username'


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
