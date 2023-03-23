from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    sharif = models.CharField(max_length=100)    
    telefon = models.CharField(max_length=200)  
    lavozim = models.CharField(max_length=100, default='talaba')  
    parol = models.CharField(max_length=100)
  

