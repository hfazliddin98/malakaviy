from django.contrib import admin
from django.urls import path
from .views import fayl, namuna, yuklash, test_deadline


urlpatterns = [    
   path('fayl/', fayl, name='fayl'), 
   path('yuklash/', yuklash, name='yuklash'),  # Yangi yuklash URL
   path('namuna/',namuna, name='namuna'),
   path('test-deadline/', test_deadline, name='test_deadline'),  # Test sahifasi
   # path('namuna/<int:pk>',namunalar, name='link'),       
]