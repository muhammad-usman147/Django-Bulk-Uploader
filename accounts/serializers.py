from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from .models import Profile


USER = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = USER
        fields = ('id', 'email', 'name', 'password')


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = USER
        fields = ['username', 'email', 'password']


class SignupSerializer(serializers.ModelSerializer):
    user = UserSerializers(many=False)

    class Meta:
        model = Profile
        fields = ['user', 'company', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = USER(**user_data)
        user.set_password(user_data.get('password'))
        user.save()
        Profile.objects.create(**validated_data, user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}

