import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        user = self.request.user
        chat = user.chat_set.all()
        if not chat:
            context['chat'] = 0
        else:
            context['chat'] = chat[0].id
        return context


def createChat(request):
    data = request.POST
    receiver = User.objects.get(pk=int(data['receiver']))
    sender = User.objects.get(pk=int(data['sender']))
    chat_name = receiver.username + sender.username
    chat_name_flip = sender.username + receiver.username

    chat = models.Chat.objects.filter(Q(name=chat_name) | Q(name=chat_name_flip))
    if not chat:
        chat = models.Chat.objects.create(name=chat_name)
        chat.save()
        chat.users.add(receiver, sender)
        chat.save()
    else:
        chat = chat[0]
        
    if not chat.users.all():
        chat.users.add(receiver, sender)
        chat.save()
        
    return JsonResponse(data=serializers.ChatSerializer(chat).data)


class ChatViewSet(ModelViewSet):
    queryset = models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer

    def get_queryset(self):
        return self.request.user.chat_set.all().order_by('-pk')
        


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().exclude(username=self.request.user.username))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/form.html'
    success_url = reverse_lazy('home')