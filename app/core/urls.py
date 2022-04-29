"""react URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework import routers
from .views import (registeration_view, assets_listView, fav_coin_list, fav_view)
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()

app_name = 'core'
urlpatterns = [
    path('register', registeration_view, name="register"),
    path('login', obtain_auth_token, name="login"),
    path('assets-list', assets_listView, name="assets"),
    path('fav-coin-list', fav_coin_list),
    path('fav_view', fav_view, name="fav-view"),
]
