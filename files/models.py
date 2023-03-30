from django.db import models


class Fayl(models.Model):
    ism = models.CharField(max_length=100)
    familya = models.CharField(max_length=100)
    fan = models.CharField(max_length=100)
    pasport = models.FileField(upload_to='pasportlar/')
    diplom = models.FileField(upload_to='diplomlar/')
    ariza = models.FileField(upload_to='ariza/')
    malumotnoma = models.FileField(upload_to='malumotnoma/')
    anketa = models.FileField(upload_to='minimum anketa/')
    kochirma = models.FileField(upload_to='kengash ko`chirmasi/')
    yollanma = models.FileField(upload_to='yo`lanma xat/')
    royhat = models.FileField(upload_to='ilmiy ishlar ro`yati/')
    sana = models.DateTimeField(auto_now_add=True)
    
    
    

class Namuna(models.Model):
    diplom = models.FileField(upload_to='namuna/')
    ariza = models.FileField(upload_to='namuna/')
    malumotnoma = models.FileField(upload_to='namuna/')
    anketa = models.FileField(upload_to='namuna/')
    kochirma = models.FileField(upload_to='namuna/')
    royhat = models.FileField(upload_to='namuna/')
    sana = models.DateTimeField(auto_now_add=True)
    
class Sana(models.Model):
    yil = models.IntegerField()
    oy = models.IntegerField()
    kun = models.IntegerField()
    sana = models.DateTimeField(auto_now_add=True)