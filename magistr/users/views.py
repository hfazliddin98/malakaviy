from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.paginator import Paginator
from .models import User





def home(request):    
    return render(request, 'asosiy/home.html')


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


def royhat(request):
    habar = ''
    if request.method == 'POST':
        username = request.POST['username']
        familya = request.POST['familya']
        ism = request.POST['ism']
        sharif = request.POST['sharif']                
        telefon = request.POST['telefon']        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username):
            habar = 'Bunday ID mavjud'        
        elif User.objects.filter(telefon=telefon):
            habar = 'Bumday telefon nomer mavjud'
        elif len(password1) < 8 or password1 == familya or password1 == ism:
            habar = 'Parol 8 tadan kam bolmasligi kerak'
        elif password1 != password2:
            habar = 'Tasdiqlash parolini to`gri kiritish'
        else:                                
            user = get_user_model().objects.create(username = username, last_name = familya, first_name = ism, password=make_password(password1), sharif=sharif, telefon = telefon, parol= password2)
            user.is_active = False
            user.is_staff = False
            return redirect('/kirish')
    
    return render(request, 'royhat/royhat.html', {'habar':habar})