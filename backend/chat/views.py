import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user.id
        context['chat'] = models.Chat.objects.filter(Q(receiver=user) | Q(sender=user))[0]
        return context


def createChat(request):
    data = request.POST
    receiver = User.objects.get(pk=data['receiver'])
    sender = User.objects.get(pk=data['sender'])
    chat, created = models.Chat.objects.get_or_create(
        receiver=receiver,
        sender=sender
    )
    return JsonResponse(data=serializers.ChatSerializer(chat).data)


class ChatViewSet(ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

    def get_queryset(self):
        return models.Chat.objects.all().order_by('-pk')


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.all().exclude(username=self.request.user.username)