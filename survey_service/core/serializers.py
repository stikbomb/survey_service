""" Сериализаторы для работы с входом в систему и объектом пользователя. """
from django.contrib.auth import authenticate, models
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """ Сериализатор для логина. """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели пользователя. """
    class Meta:
        model = models.User
        fields = (
            'id',
            'last_login',
            'username',
            'is_superuser',
            'password'
        )
        read_only_fields = ('last_login', 'is_superuser')
        extra_kwargs = {
            'password': {'required': True, 'write_only': True}
        }
