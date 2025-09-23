from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


# Fan yo'nalishlari ro'yxati
FANLAR_CHOICES = [
    ('uzbek_tili', "O'zbek tili"),
    ('til_nazariyasi', 'Til nazariyasi. Amaliy va kompyuter lingvistikasi'),
    ('talim_tarbiya', "Ta'lim va tarbiya nazariyasi va metodikasi(ijtimoiy-gumanitar fanlar)"),
    ('ingliz_tili', 'Chet tili (Ingliz tili)'),
    ('nemis_tili', 'Chet tili (Nemis tili)'),
]


def validate_file_size(value):
    """Fayl hajmini tekshirish - maksimal 4MB"""
    filesize = value.size
    if filesize > 4 * 1024 * 1024:  # 4MB
        raise ValidationError("Fayl hajmi 4MB dan katta bo'lmasligi kerak!")
    return value


class FanYonalishi(models.Model):
    """Fan yo'nalishi"""
    
    name = models.CharField(
        max_length=200,
        verbose_name="To'liq nomi",
        blank=True
    )
    belgilangan_sana = models.DateTimeField(auto_now_add=True, verbose_name="Belgilangan sana")
    
    class Meta:
        verbose_name = "Fan yo'nalishi"
        verbose_name_plural = "Fan yo'nalishlari"
        
    def save(self, *args, **kwargs):
        """Modelni saqlash"""
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name if self.name else f"FanYonalishi #{self.pk}"


class Fayl(models.Model):
    # Telefon raqam uchun validator
    phone_regex = RegexValidator(
        regex=r'^\+998[0-9]{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
    )
    
    # Fayl kengaytmalari validatori
    doc_validator = FileExtensionValidator(
        allowed_extensions=['pdf', 'doc', 'docx', 'wps']
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Foydalanuvchi",
        related_name="fayllar"
    )
    telefon = models.CharField(
        validators=[phone_regex], 
        max_length=13,
        verbose_name="Telefon raqam"
    )
    fan_yonalishi = models.ForeignKey(
        FanYonalishi,
        on_delete=models.CASCADE,
        verbose_name="Fan yo'nalishi",
        related_name="fayllar"
    )
    pasport = models.FileField(
        upload_to='pasportlar/',
        validators=[validate_file_size],
        verbose_name="Pasport nusxasi"
    )
    diplom = models.FileField(
        upload_to='diplomlar/',
        validators=[doc_validator, validate_file_size],
        verbose_name="Diplomlar"
    )
    ariza = models.FileField(
        upload_to='ariza/',
        blank=True,
        validators=[doc_validator, validate_file_size],
        verbose_name="Ariza yoki yo'llanma xat"
    )
    malumotnoma = models.FileField(
        upload_to='malumotnoma/',
        validators=[doc_validator, validate_file_size],
        verbose_name="Ma'lumotnoma"
    )
    anketa = models.FileField(
        upload_to='minimum_anketa/',
        validators=[doc_validator, validate_file_size],
        verbose_name="Minimum anketasi"
    )
    kochirma = models.FileField(
        upload_to='kengash_kochirmasi/',
        validators=[doc_validator, validate_file_size],
        verbose_name="Kengash qarori ko'chirmasi"
    )
    royhat = models.FileField(
        upload_to='ilmiy_ishlar_royxati/',
        validators=[doc_validator, validate_file_size],
        verbose_name="Ilmiy ishlar ro'yxati"
    )
    sana = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan sana")
    
    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"
        ordering = ['-sana']
    
    def __str__(self):
        user_name = f"{self.user.first_name} {self.user.last_name}" if self.user.first_name else self.user.username
        fan_name = self.fan_yonalishi.name if self.fan_yonalishi else 'Fan yo\'nalishi belgilanmagan'
        return f"{user_name} - {fan_name}"
    
    
    

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


class Deadline(models.Model):
    """Ariza yuborish uchun deadline"""
    nomi = models.CharField(max_length=200, verbose_name="Deadline nomi", default="Ariza yuborish muddati")
    deadline_sana = models.DateTimeField(verbose_name="Tugash sana va vaqti")
    faol = models.BooleanField(default=True, verbose_name="Faol")
    yaratilgan = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    yangilangan = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Deadline"
        verbose_name_plural = "Deadlinelar"
        ordering = ['-yaratilgan']
    
    def __str__(self):
        return f"{self.nomi} - {self.deadline_sana.strftime('%d.%m.%Y %H:%M')}"
    
    @classmethod
    def get_active_deadline(cls):
        """Faol deadline ni olish"""
        return cls.objects.filter(faol=True).first()