from django.contrib import admin
from django.urls import path
from .views import fayl, yuklash

urlpatterns = [
    path('', fayl, name='fayl'),
    path('yuklash/', yuklash, name='yuklash'),   
]