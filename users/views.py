from email import errors
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from files.models import Deadline
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import User
from users.choices import RoleChoice
from users.forms import LoginForm, RoyxatForm
from files.models import Fayl, Sana, Namuna





def home(request):  
    """Bosh sahifa - roliga qarab ma'lumotlarni ko'rsatish"""
    if request.user.is_authenticated:
        if request.user.rol == RoleChoice.ADMIN or request.user.is_superuser:
            from django.core.paginator import Paginator
            from files.models import FanYonalishi
            
            fayllar = Fayl.objects.all().order_by('-sana')
            
            # Pagination qo'shish
            paginator = Paginator(fayllar, 10)  # Har sahifada 10 ta fayl
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            
            # Fan yo'nalishlari
            fan_yonalishlari = FanYonalishi.objects.all()
            
            context = {
                'data': fayllar,
                'page': page,
                'fan_yonalishlari': fan_yonalishlari,
                'jami_fayllar': fayllar.count(),
                'jami_fanlar': fan_yonalishlari.count(),
                'sahifalar_soni': paginator.num_pages,
                'joriy_sahifa': page.number,
            }
            return render(request, 'admin/home.html', context)
        elif request.user.rol == RoleChoice.TALABA:    
            fayllar = Fayl.objects.filter(
                user=request.user
            ).order_by('-sana')

            context = {
                'data': fayllar,
            }
            return render(request, 'talaba/home.html', context)
    else:
        namuna = Namuna.objects.all()
        print(f"DEBUG: Namuna soni: {namuna.count()}")  # Debug uchun
        # Fan yo'nalishlari ro'yxatini olish
        from files.models import FanYonalishi
        fan_yonalishlari = FanYonalishi.objects.all()
        print(f"DEBUG: Fan yo'nalishlari soni: {fan_yonalishlari.count()}")  # Debug uchun
        context = {
            'namunalar': namuna,
            'fan_yonalishlari': fan_yonalishlari,
        }
        return render(request, 'asosiy/home.html', context)
# def home(request):
#     """Bosh sahifa - roliga qarab ma'lumotlarni ko'rsatish"""
    
#     # Foydalanuvchi ro'yxatdan o'tmagan bo'lsa
#     if not request.user.is_authenticated:
#         namuna = Namuna.objects.all()
#         # Fan yo'nalishlari ro'yxatini olish
#         from files.models import FanYonalishi
#         fan_yonalishlari = FanYonalishi.objects.all()
#         context = {
#             'namunalar': namuna,
#             'fan_yonalishlari': fan_yonalishlari,
#         }
#         return render(request, 'asosiy/home.html', context)
    
#     # Admin yoki superuser uchun - barcha fayllarni ko'rsatish
#     if request.user.is_superuser or (hasattr(request.user, 'rol') and request.user.rol == 'Admin'):
#         fayllar = Fayl.objects.all().order_by('-sana')
#     else:
#         # Oddiy foydalanuvchi uchun - faqat o'z fayllarini ko'rsatish
#         fayllar = Fayl.objects.filter(
#             user=request.user
#         ).order_by('-sana')
    
#     page = Paginator(fayllar, 10)  # 10 ta element
#     page_list = request.GET.get('page')
#     page = page.get_page(page_list)
#     namuna = Namuna.objects.all()
    
#     # Fan yo'nalishlari ro'yxatini olish
#     from files.models import FanYonalishi
#     fan_yonalishlari = FanYonalishi.objects.all()
    
#     context = {
#         'data': fayllar,
#         'namunalar': namuna,
#         'page': page,
#         'user_role': getattr(request.user, 'rol', None) if request.user.is_authenticated else None,
#         'fan_yonalishlari': fan_yonalishlari,
#     }
#     return render(request, 'asosiy/home.html', context)  
    

def kirish(request):
    """Tizimga kirish"""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            
            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home') 
            else:
                return redirect('kirish')
            
    return render(request, 'royhat/kirish.html')



def royhat(request):
    """Ro'yxatdan o'tish"""
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RoyxatForm()
        if request.method == 'POST':
            form = RoyxatForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    return redirect('kirish')
                except Exception as e:
                    return redirect('royhat')
        
        context = {
            'form': form,
        }
        return render(request, 'royhat/royhat.html', context)
    


@login_required
def javob(request, pk):
    """Fayl tafsilotlari"""
    fayl = get_object_or_404(Fayl, id=pk)
    context = {
        'javob': fayl,
    }
    return render(request, 'asosiy/hujjatlar.html', context)

