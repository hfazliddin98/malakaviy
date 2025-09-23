import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from users.choices import RoleChoice



class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    sharif = models.CharField(max_length=100, verbose_name="Sharif")     
    rol = models.CharField(max_length=20, choices=RoleChoice.choices, default=RoleChoice.TALABA, verbose_name="Rol")
    parol = models.CharField(max_length=100, verbose_name="Parol", blank=True, null=True)
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
  

