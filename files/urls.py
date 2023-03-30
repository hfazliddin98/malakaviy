from django.contrib import admin
from django.urls import path
from .views import fayl, namuna


urlpatterns = [    
   path('fayl/', fayl, name='fayl'), 
   path('',namuna, name='namuna')       
]