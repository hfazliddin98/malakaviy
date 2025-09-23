from django.contrib import admin
from .models import Fayl, Namuna, Sana, Deadline, FanYonalishi


@admin.register(Fayl)
class FaylAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'telefon', 'get_fan_yonalishi', 'formatted_sana')
    list_filter = ('fan_yonalishi', 'sana')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telefon')
    ordering = ('-sana',)
    readonly_fields = ('sana',)
    
    def get_user_name(self, obj):
        """Foydalanuvchi ismini ko'rsatish"""
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username
    get_user_name.short_description = 'Foydalanuvchi'
    get_user_name.admin_order_field = 'user__first_name'
    
    def get_fan_yonalishi(self, obj):
        """Fan yo'nalishini ko'rsatish"""
        return obj.fan_yonalishi.name if obj.fan_yonalishi else 'Belgilanmagan'
    get_fan_yonalishi.short_description = 'Fan yo\'nalishi'
    get_fan_yonalishi.admin_order_field = 'fan_yonalishi__name'
    
    def formatted_sana(self, obj):
        """Sana va vaqtni soatlarigacha aniqlikda ko'rsatish"""
        return obj.sana.strftime('%d.%m.%Y %H:%M')
    formatted_sana.short_description = 'Topshirilgan sana va vaqt'
    formatted_sana.admin_order_field = 'sana'


@admin.register(Namuna)
class NamunaAdmin(admin.ModelAdmin):
    list_display = ('id', 'formatted_sana')
    ordering = ('-sana',)
    
    def formatted_sana(self, obj):
        return obj.sana.strftime('%d.%m.%Y %H:%M')
    formatted_sana.short_description = 'Yuklangan sana va vaqt'


@admin.register(Sana)
class SanaAdmin(admin.ModelAdmin):
    list_display = ('yil', 'oy', 'kun', 'formatted_sana')
    ordering = ('-sana',)
    
    def formatted_sana(self, obj):
        return obj.sana.strftime('%d.%m.%Y %H:%M')
    formatted_sana.short_description = 'Yaratilgan sana va vaqt'


@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'formatted_deadline', 'faol', 'formatted_yaratilgan')
    list_filter = ('faol', 'yaratilgan')
    search_fields = ('nomi',)
    ordering = ('-yaratilgan',)
    readonly_fields = ('yaratilgan', 'yangilangan')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('nomi', 'deadline_sana', 'faol')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('yaratilgan', 'yangilangan'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_deadline(self, obj):
        return obj.deadline_sana.strftime('%d.%m.%Y %H:%M')
    formatted_deadline.short_description = 'Deadline'
    formatted_deadline.admin_order_field = 'deadline_sana'
    
    def formatted_yaratilgan(self, obj):
        return obj.yaratilgan.strftime('%d.%m.%Y %H:%M')
    formatted_yaratilgan.short_description = 'Yaratilgan'


@admin.register(FanYonalishi)
class FanYonalishiAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_belgilangan_sana')
    list_filter = ('belgilangan_sana',)
    search_fields = ('name',)
    ordering = ('-belgilangan_sana',)
    readonly_fields = ('belgilangan_sana',)
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name',)
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('belgilangan_sana',),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_belgilangan_sana(self, obj):
        return obj.belgilangan_sana.strftime('%d.%m.%Y %H:%M')
    formatted_belgilangan_sana.short_description = 'Belgilangan sana'
    formatted_belgilangan_sana.admin_order_field = 'belgilangan_sana'