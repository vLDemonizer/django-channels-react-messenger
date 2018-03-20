from django.contrib.auth.models import User

from . import models

from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
        depth = 1


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Chat
        fields = ('receiver', 'sender', 'messages', 'id')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'