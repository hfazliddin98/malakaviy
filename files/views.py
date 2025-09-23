from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.conf import settings
from .models import Fayl, Namuna, Sana, Deadline, FanYonalishi


def namuna(request):
    """Namuna fayllarini ko'rsatish"""
    link = Namuna.objects.all()
    context = {
        'link': link,
    }
    return render(request, 'asosiy/namunalar.html', context)

@login_required
def javob(request, pk):
    """Fayl tafsilotlarini ko'rsatish"""
    fayl = get_object_or_404(Fayl, id=pk)
    context = {
        'javob': fayl,
    }
    return render(request, 'asosiy/hujjatlar.html', context)


def sana(request):
    """Sanalarni ko'rsatish"""
    vaqt = Sana.objects.all()
    context = {
        'vaqt': vaqt,
    }
    return render(request, 'asosiy/fayl.html', context)


def fayl(request):
    """Yangi fayl yuklash"""
    if request.method == 'POST':
        try:
            # Ma'lumotlarni olish
            telefon = request.POST.get('telefon', '').strip()
            fan_yonalishi_id = request.POST.get('fan_yonalishi')
            
            # Fan yo'nalishini olish
            if fan_yonalishi_id:
                try:
                    fan_yonalishi = FanYonalishi.objects.get(id=fan_yonalishi_id)
                except FanYonalishi.DoesNotExist:
                    fan_yonalishi = None
            else:
                fan_yonalishi = None
            
            # Majburiy maydonlarni tekshirish
            if not telefon or not fan_yonalishi:
                messages.error(request, "Barcha majburiy maydonlarni to'ldiring!")
                return render(request, 'asosiy/baza.html', {
                    'fan_yonalishlari': FanYonalishi.objects.all()
                })
            
            # Fayllarni olish
            required_files = ['pasport', 'diplom', 'ariza', 'malumotnoma', 'anketa', 'kochirma', 'royhat']
            files_data = {}
            
            for file_field in required_files:
                if file_field in request.FILES:
                    files_data[file_field] = request.FILES[file_field]
                else:
                    messages.error(request, f"{file_field.title()} fayli yuklanmagan!")
                    return render(request, 'asosiy/baza.html', {
                        'fan_yonalishlari': FanYonalishi.objects.all()
                    })
            
            # Fayl yaratish
            fayl = Fayl.objects.create(
                user=request.user if request.user.is_authenticated else None,
                telefon=telefon,
                fan_yonalishi=fan_yonalishi,
                **files_data
            )
            
            messages.success(request, 'Hujjatlar muvaffaqiyatli yuklandi!')
            return redirect('home')
            
        except ValidationError as e:
            messages.error(request, f"Validatsiya xatosi: {e}")
            return render(request, 'asosiy/baza.html', {
                'fan_yonalishlari': FanYonalishi.objects.all()
            })
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return render(request, 'asosiy/baza.html', {
                'fan_yonalishlari': FanYonalishi.objects.all()
            })
    
    return render(request, 'asosiy/baza.html', {
        'fan_yonalishlari': FanYonalishi.objects.all()
    })


@login_required
def yuklash(request):
    """Fayl yuklash sahifasi - deadline bilan tekshirish"""
    from django.utils import timezone
    
    # Deadline ni olish
    deadline = Deadline.get_active_deadline()
    
    # Deadline vaqti borligini tekshirish
    can_upload_by_deadline = False
    if deadline and deadline.faol:
        can_upload_by_deadline = timezone.now() <= deadline.deadline_sana
    
    # Admin yoki superuser uchun har doim ruxsat
    if request.user.is_superuser or (hasattr(request.user, 'rol') and request.user.rol == 'Admin'):
        can_upload = True
    else:
        # Oddiy foydalanuvchi uchun deadline tekshiruvi
        can_upload = can_upload_by_deadline
    
    if request.method == 'POST':
        if not can_upload:
            messages.error(request, 'Hujjat yuklash muddati tugagan!')
            return redirect('home')
            
        try:
            # Ma'lumotlarni olish
            telefon = request.POST.get('telefon', '').strip()
            
            # Fan yo'nalishini formadan olish
            fan_yonalishi_id = request.POST.get('fan_yonalishi')
            if fan_yonalishi_id:
                try:
                    fan_yonalishi = FanYonalishi.objects.get(id=fan_yonalishi_id)
                except FanYonalishi.DoesNotExist:
                    fan_yonalishi = None
            else:
                fan_yonalishi = None
            
            # Majburiy maydonlarni tekshirish
            if not telefon:
                messages.error(request, "Telefon raqamini to'ldiring!")
                return render(request, 'asosiy/yuklash_form.html', {
                    'deadline': deadline,
                    'can_upload': can_upload,
                    'can_upload_by_deadline': can_upload_by_deadline,
                    'fan_yonalishlari': FanYonalishi.objects.all(),
                })
            
            # Fan yo'nalishi tanlanganligini tekshirish
            if not fan_yonalishi:
                messages.error(request, "Fan yo'nalishi tanlanmagan! Iltimos, fan yo'nalishini tanlang.")
                return render(request, 'asosiy/yuklash_form.html', {
                    'deadline': deadline,
                    'can_upload': can_upload,
                    'can_upload_by_deadline': can_upload_by_deadline,
                    'fan_yonalishlari': FanYonalishi.objects.all(),
                })
            
            # Fayllarni olish
            required_files = ['pasport', 'diplom', 'ariza', 'malumotnoma', 'anketa', 'kochirma', 'royhat']
            files_data = {}
            
            for file_field in required_files:
                if file_field in request.FILES:
                    files_data[file_field] = request.FILES[file_field]
                else:
                    messages.error(request, f"{file_field.title()} fayli yuklanmagan!")
                    return render(request, 'asosiy/yuklash_form.html', {
                        'deadline': deadline,
                        'can_upload': can_upload,
                        'can_upload_by_deadline': can_upload_by_deadline,
                        'fan_yonalishlari': FanYonalishi.objects.all(),
                    })
            
            # Fayl yaratish
            fayl = Fayl.objects.create(
                user=request.user,
                telefon=telefon,
                fan_yonalishi=fan_yonalishi,
                **files_data
            )
            
            messages.success(request, 'Hujjatlar muvaffaqiyatli yuklandi!')
            return redirect('home')
            
        except ValidationError as e:
            messages.error(request, f"Validatsiya xatosi: {e}")
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
    
    # Barcha FanYonalishi larini olish
    fan_yonalishlari = FanYonalishi.objects.all()
    
    context = {
        'deadline': deadline,
        'can_upload': can_upload,
        'can_upload_by_deadline': can_upload_by_deadline,
        'fan_yonalishlari': fan_yonalishlari,
    }
    
    return render(request, 'asosiy/yuklash_form.html', context)


def test_deadline(request):
    """Deadline test sahifasi - development uchun"""
    if not settings.DEBUG:
        # Production da bu sahifaga ruxsat yo'q
        return HttpResponse("Bu sahifa faqat development rejimida ishlaydi", status=403)
    
    # Deadline ma'lumotlarini olish
    deadline = Deadline.get_active_deadline()
    
    context = {
        'deadline': deadline,
        'TIME_ZONE': settings.TIME_ZONE,
    }
    
    return render(request, 'test_deadline.html', context)
