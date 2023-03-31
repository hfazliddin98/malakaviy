from django.contrib import admin
from django.urls import path
from  .views import  home, kirish, royhat, javob


urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('royhat/', royhat, name='royhat'),    
    path('yuklash/<int:pk>', javob, name='link'),       
]
 