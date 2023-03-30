from django.contrib import admin
from django.urls import path
from  .views import  home, kirish, royhat, yuklash, javob


urlpatterns = [
    path('/', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('royhat/', royhat, name='royhat'),
    path('', yuklash, name='yuklash'),
    path('yuklash/<int:pk>', javob, name='link'),       
]
 