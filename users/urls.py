from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from  .views import  home, kirish, royhat, javob


urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('royhat/', royhat, name='royhat'),    
    path('yuklash/<int:pk>', javob, name='link'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),       
]
 