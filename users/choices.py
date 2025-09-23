from django.db import models


class RoleChoice(models.TextChoices):
    ADMIN = ("Admin", "Admin")
    TALABA = ("Talaba", "Talaba")
