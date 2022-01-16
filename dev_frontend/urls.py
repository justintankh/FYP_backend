from django.urls import path
from django.shortcuts import render
from .views import index


urlpatterns = [
    path('', index),
    path('signup', index),
    path('login', index),
    path('basket/<str:code>', index),
]
