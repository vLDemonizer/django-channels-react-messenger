from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.urls import path

from rest_framework import routers

from chat import views

router = routers.SimpleRouter()
router.register(r'chats', views.ChatViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('accounts/create/', views.UserView.as_view(), name='create-user'),
    path('create-chat/', views.createChat, name='create'),
    path('', views.IndexView.as_view(), name='home'),
] + router.urls