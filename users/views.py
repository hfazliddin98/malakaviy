from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt, csrf_protect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator
from .models import User
from files.models import Fayl, Sana, Namuna





@csrf_exempt
def home(request):  
    fayllar = Fayl.objects.all() 
    page = Paginator(fayllar, 5) 
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    namuna = Namuna.objects.all()  
    context = {
        'data':fayllar,
        'namunalar':namuna,
        'page':page,        
    }
    return render(request, 'asosiy/home.html', context)  
    


@csrf_exempt
def kirish(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.save()
            return redirect('/')
        else:
            messages.warning(request, 'xato')
            return redirect('/kirish')

    return render(request, 'royhat/kirish.html')


@csrf_exempt
def royhat(request):
    habar = ''
    if request.method == 'POST':
        username = request.POST['username']
        familya = request.POST['familya']
        ism = request.POST['ism']
        sharif = request.POST['sharif']                
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            habar = 'Bunday ID mavjud'         
        elif len(password1) < 8 or password1 == familya or password1 == ism:
            habar = 'Parol 8 tadan kam bolmasligi kerak'
        elif password1 != password2:
            habar = 'Tasdiqlash parolini to`gri kiritish'
        else:                                
            user = get_user_model().objects.create(username = username, last_name = familya, first_name = ism, password=make_password(password1), sharif=sharif, parol= password2)
            user.is_active = False
            user.is_staff = False
            return redirect('/kirish')
    
    return render(request, 'royhat/royhat.html', {'habar':habar})



@csrf_exempt
def javob(request, pk):
    fayl = Fayl.objects.get(id=pk)
    contex = {
        'javob':fayl,
    }
    return render(request, 'asosiy/hujjatlar.html', contex)

